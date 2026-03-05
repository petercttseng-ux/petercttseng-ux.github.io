# 🐟 臺灣魚鄉好風情

**農業部水產試驗所 × 養殖地區照片地圖系統**

---

## 專案目錄結構

```
taiwan_fish_village/
├── app.py              ← Flask 後端（API + SQLite）
├── index.html          ← 前端網頁（Leaflet 地圖）
├── requirements.txt    ← Python 套件清單
├── README.md           ← 本說明文件
├── database.db         ← SQLite 資料庫（執行後自動建立）
└── photos/             ← 照片存放目錄（執行後自動建立）
    ├── u1_20241201_....jpg
    └── ...
```

---

## 安裝與啟動

```bash
# 1. 安裝套件
pip install -r requirements.txt

# 2. 啟動伺服器
python app.py

# 3. 開啟瀏覽器
# http://localhost:5000
```

---

## 資料庫結構（SQLite）

**`database.db`** 包含兩張資料表：

### users（使用者）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER PK | 自動編號 |
| username | TEXT UNIQUE | 帳號（英數字） |
| password | TEXT | SHA-256 雜湊 |
| fullname | TEXT | 中文姓名 |
| email | TEXT UNIQUE | 電子郵件 |
| created | TEXT | 建立時間 |

### photos（照片）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER PK | 自動編號 |
| user_id | INTEGER FK | 關聯使用者 |
| filename | TEXT | 原始檔名 |
| stored_name | TEXT | 伺服器儲存檔名 |
| latitude | REAL | 緯度（GPS） |
| longitude | REAL | 經度（GPS） |
| description | TEXT | 照片描述 |
| filesize | INTEGER | 縮圖大小（bytes） |
| uploaded | TEXT | 上傳時間 |

---

## API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/register` | 使用者註冊 |
| POST | `/api/login` | 使用者登入 |
| POST | `/api/photos/upload` | 多張照片上傳（multipart） |
| GET  | `/api/photos` | 取得照片清單 |
| DELETE | `/api/photos/<id>` | 刪除照片 |
| GET  | `/api/stats` | 資料庫統計資訊 |
| GET  | `/photos/<filename>` | 取得照片檔案 |
