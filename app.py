"""
臺灣魚鄉好風情 — Flask + SQLite Backend
Run:  python app.py
Open: http://localhost:5000
"""

import os
import sqlite3
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from flask import (Flask, request, jsonify, send_from_directory,
                   send_file, abort, make_response)
from PIL import Image, ExifTags

# ─────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent          # 專案根目錄
DB_PATH   = BASE_DIR / "database.db"      # SQLite 資料庫
PHOTO_DIR = BASE_DIR / "photos"           # 照片存放資料夾
PHOTO_DIR.mkdir(exist_ok=True)

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
MAX_THUMB_W = 600    # 縮圖最大寬度 (px)

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")

# ══════════════════════════════════════════════
#  CORS helper (no external package needed)
# ══════════════════════════════════════════════
@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE,OPTIONS"
    return resp

@app.route("/api/<path:p>", methods=["OPTIONS"])
def options_handler(p):
    return "", 204

# ══════════════════════════════════════════════
#  DATABASE SETUP
# ══════════════════════════════════════════════
def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                username  TEXT    UNIQUE NOT NULL,
                password  TEXT    NOT NULL,
                fullname  TEXT    NOT NULL,
                email     TEXT    UNIQUE NOT NULL,
                created   TEXT    DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS photos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                filename    TEXT    NOT NULL,
                stored_name TEXT    NOT NULL,
                latitude    REAL,
                longitude   REAL,
                description TEXT    DEFAULT '',
                filesize    INTEGER DEFAULT 0,
                uploaded    TEXT    DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_photos_user ON photos(user_id);
            CREATE INDEX IF NOT EXISTS idx_photos_geo  ON photos(latitude, longitude);
        """)
    print(f"✅ 資料庫就緒：{DB_PATH}")

# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════
def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def extract_gps(path: Path):
    """Return (lat, lon) from EXIF or (None, None)."""
    try:
        img = Image.open(path)
        exif_raw = img._getexif()
        if not exif_raw:
            return None, None
        exif = {ExifTags.TAGS.get(k, k): v for k, v in exif_raw.items()}
        gps_info = exif.get("GPSInfo")
        if not gps_info:
            return None, None
        gps = {ExifTags.GPSTAGS.get(k, k): v for k, v in gps_info.items()}

        def dms(v):
            return float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600

        lat = dms(gps["GPSLatitude"])
        lon = dms(gps["GPSLongitude"])
        if gps.get("GPSLatitudeRef")  == "S": lat = -lat
        if gps.get("GPSLongitudeRef") == "W": lon = -lon
        return round(lat, 6), round(lon, 6)
    except Exception:
        return None, None

def make_thumbnail(src: Path, dest: Path, max_w=MAX_THUMB_W):
    """Save a JPEG thumbnail; preserves aspect ratio."""
    img = Image.open(src)
    # Auto-rotate by EXIF orientation
    try:
        for tag, val in (img._getexif() or {}).items():
            if ExifTags.TAGS.get(tag) == "Orientation":
                rotations = {3: 180, 6: 270, 8: 90}
                if val in rotations:
                    img = img.rotate(rotations[val], expand=True)
                break
    except Exception:
        pass
    img = img.convert("RGB")
    ratio = min(1.0, max_w / max(img.width, 1))
    new_w = max(1, int(img.width  * ratio))
    new_h = max(1, int(img.height * ratio))
    img = img.resize((new_w, new_h), Image.LANCZOS)
    img.save(dest, "JPEG", quality=82, optimize=True)

def ok(data=None, **kw):
    resp = {"success": True}
    if data is not None:
        resp["data"] = data
    resp.update(kw)
    return jsonify(resp)

def err(msg, code=400):
    return jsonify({"success": False, "message": msg}), code

def row_to_dict(row):
    return dict(row) if row else None

# ══════════════════════════════════════════════
#  AUTH ENDPOINTS
# ══════════════════════════════════════════════
@app.route("/api/register", methods=["POST"])
def register():
    d = request.get_json(force=True) or {}
    username = (d.get("username") or "").strip()
    password = d.get("password") or ""
    fullname = (d.get("fullname") or "").strip()
    email    = (d.get("email")    or "").strip()

    # Validation
    if not all([username, password, fullname, email]):
        return err("所有欄位均為必填")
    if not re.match(r"^[A-Za-z0-9_]{3,20}$", username):
        return err("帳號需為 3–20 位英數字或底線")
    if len(password) < 6:
        return err("密碼至少需 6 個字元")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return err("請輸入有效的電子郵件格式")
    if not any("\u4e00" <= c <= "\u9fff" for c in fullname):
        return err("請輸入中文姓名")

    try:
        with get_db() as db:
            db.execute(
                "INSERT INTO users (username,password,fullname,email) VALUES (?,?,?,?)",
                (username, hash_pw(password), fullname, email)
            )
        return ok(message="註冊成功！")
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return err("此帳號已存在，請更換帳號名稱")
        return err("此電子郵件已被使用")

@app.route("/api/login", methods=["POST"])
def login():
    d = request.get_json(force=True) or {}
    username = (d.get("username") or "").strip()
    password = d.get("password") or ""

    if not username or not password:
        return err("請輸入帳號與密碼")

    with get_db() as db:
        row = db.execute(
            "SELECT id,username,fullname,email FROM users WHERE username=? AND password=?",
            (username, hash_pw(password))
        ).fetchone()

    if not row:
        return err("帳號或密碼錯誤")

    return ok(data=dict(row))

# ══════════════════════════════════════════════
#  PHOTO ENDPOINTS
# ══════════════════════════════════════════════
@app.route("/api/photos/upload", methods=["POST"])
def upload_photos():
    user_id = request.form.get("user_id", type=int)
    desc    = (request.form.get("description") or "").strip()
    files   = request.files.getlist("photos")

    if not user_id:
        return err("未提供使用者 ID", 401)
    if not files:
        return err("請至少上傳一張照片")

    # Verify user exists
    with get_db() as db:
        u = db.execute("SELECT id,fullname FROM users WHERE id=?", (user_id,)).fetchone()
    if not u:
        return err("使用者不存在", 401)

    saved = []
    errors = []

    for f in files:
        orig_name = f.filename or "photo.jpg"
        ext = Path(orig_name).suffix.lower()
        if ext not in ALLOWED_EXT:
            errors.append(f"{orig_name}: 不支援的檔案格式")
            continue

        # Unique stored filename
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:21]
        stored = f"u{user_id}_{ts}{ext}"
        raw_path   = PHOTO_DIR / f"raw_{stored}"
        thumb_path = PHOTO_DIR / stored

        try:
            f.save(str(raw_path))
            lat, lon = extract_gps(raw_path)
            make_thumbnail(raw_path, thumb_path)
            raw_path.unlink(missing_ok=True)   # remove raw after thumbnail

            fsize = thumb_path.stat().st_size

            with get_db() as db:
                cur = db.execute(
                    """INSERT INTO photos
                       (user_id, filename, stored_name, latitude, longitude, description, filesize)
                       VALUES (?,?,?,?,?,?,?)""",
                    (user_id, orig_name, stored, lat, lon, desc, fsize)
                )
                photo_id = cur.lastrowid
                row = db.execute(
                    """SELECT p.*, u.fullname FROM photos p
                       JOIN users u ON p.user_id=u.id WHERE p.id=?""",
                    (photo_id,)
                ).fetchone()

            saved.append(dict(row))
        except Exception as e:
            if raw_path.exists():  raw_path.unlink(missing_ok=True)
            errors.append(f"{orig_name}: {e}")

    return ok(data=saved, errors=errors,
              message=f"成功上傳 {len(saved)} 張，失敗 {len(errors)} 張")

@app.route("/api/photos", methods=["GET"])
def get_photos():
    user_id = request.args.get("user_id", type=int)
    view    = request.args.get("view", "mine")   # mine | all

    with get_db() as db:
        if view == "all":
            rows = db.execute(
                """SELECT p.*, u.fullname FROM photos p
                   JOIN users u ON p.user_id=u.id
                   ORDER BY p.uploaded DESC"""
            ).fetchall()
        else:
            if not user_id:
                return err("未提供使用者 ID", 400)
            rows = db.execute(
                """SELECT p.*, u.fullname FROM photos p
                   JOIN users u ON p.user_id=u.id
                   WHERE p.user_id=? ORDER BY p.uploaded DESC""",
                (user_id,)
            ).fetchall()

    return ok(data=[dict(r) for r in rows])

@app.route("/api/photos/<int:photo_id>", methods=["DELETE"])
def delete_photo(photo_id):
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return err("未提供使用者 ID", 401)

    with get_db() as db:
        row = db.execute(
            "SELECT stored_name FROM photos WHERE id=? AND user_id=?",
            (photo_id, user_id)
        ).fetchone()
        if not row:
            return err("照片不存在或無權限刪除", 403)

        db.execute("DELETE FROM photos WHERE id=?", (photo_id,))

    # Delete file
    thumb = PHOTO_DIR / row["stored_name"]
    thumb.unlink(missing_ok=True)

    return ok(message="已刪除")

@app.route("/photos/<filename>")
def serve_photo(filename):
    """Serve photo files directly."""
    safe = Path(filename).name  # prevent path traversal
    path = PHOTO_DIR / safe
    if not path.exists():
        abort(404)
    return send_from_directory(str(PHOTO_DIR), safe)

# ══════════════════════════════════════════════
#  DB STATS ENDPOINT (for admin info)
# ══════════════════════════════════════════════
@app.route("/api/stats", methods=["GET"])
def stats():
    with get_db() as db:
        users  = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        photos = db.execute("SELECT COUNT(*) FROM photos").fetchone()[0]
        gps    = db.execute("SELECT COUNT(*) FROM photos WHERE latitude IS NOT NULL").fetchone()[0]
        size   = db.execute("SELECT COALESCE(SUM(filesize),0) FROM photos").fetchone()[0]
    return ok(data={
        "users": users,
        "photos": photos,
        "photos_with_gps": gps,
        "total_size_kb": round(size / 1024, 1),
        "db_path": str(DB_PATH),
        "photos_dir": str(PHOTO_DIR)
    })

# ══════════════════════════════════════════════
#  SERVE FRONTEND
# ══════════════════════════════════════════════
@app.route("/")
def index():
    return send_from_directory(str(BASE_DIR), "index.html")

# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════
if __name__ == "__main__":
    init_db()
    print("=" * 55)
    print("  臺灣魚鄉好風情 — 伺服器啟動")
    print(f"  網址：http://localhost:5000")
    print(f"  資料庫：{DB_PATH}")
    print(f"  照片目錄：{PHOTO_DIR}")
    print("=" * 55)
    app.run(host="0.0.0.0", port=5000, debug=False)
