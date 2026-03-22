# -*- coding: utf-8 -*-
import base64, json

with open('D:/tmp/Todo008/FRI logo.jpg', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()

with open('D:/tmp/Todo008/personnel.json', 'r', encoding='utf-8') as f:
    personnel = json.load(f)

personnel_js = json.dumps(personnel, ensure_ascii=False)

dept_categories = {
    '長官及行政單位': ['所長室', '副所長室', '主任秘書室', '秘書室', '人事室', '主計室', '政風室'],
    '研究單位': ['水產養殖組', '海洋漁業組', '技術服務組', '水產加工組'],
    '分中心': ['淡水養殖研究中心', '海水養殖研究中心', '沿近海漁業生物研究中心', '東港養殖研究中心', '東部漁業生物研究中心', '澎湖漁業生物研究中心']
}
categories_js = json.dumps(dept_categories, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>水試所業務交辦小助手</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

:root {{
  --primary: #0097a7;
  --primary-light: #4dd0e1;
  --primary-dark: #006978;
  --accent: #ff7043;
  --accent-light: #ff9e80;
  --success: #66bb6a;
  --warning: #ffa726;
  --danger: #ef5350;
  --info: #42a5f5;
  --bg: #f0f7fa;
  --card-bg: #ffffff;
  --text: #263238;
  --text-light: #607d8b;
  --border: #e0e8ec;
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 30px rgba(0,0,0,0.12);
  --radius: 12px;
  --radius-sm: 8px;
}}

* {{ margin:0; padding:0; box-sizing:border-box; }}

body {{
  font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}}

/* ===== LOGIN SCREEN ===== */
.login-screen {{
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, #004d56 0%, #00838f 30%, #0097a7 60%, #4dd0e1 100%);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}}

.login-screen.hidden {{ display: none; }}

.login-card {{
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  width: 100%;
  max-width: 460px;
  overflow: hidden;
  animation: loginFadeIn 0.6s ease;
}}

@keyframes loginFadeIn {{
  from {{ opacity: 0; transform: translateY(30px) scale(0.95); }}
  to {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

.login-header {{
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
  padding: 32px 24px;
  text-align: center;
  color: white;
}}

.login-header img {{
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: white;
  padding: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  margin-bottom: 12px;
}}

.login-header h1 {{
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}}

.login-header p {{
  font-size: 13px;
  opacity: 0.85;
}}

.login-body {{
  padding: 28px 32px 32px;
}}

.login-body .form-group {{
  margin-bottom: 16px;
}}

.login-body .form-group label {{
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-light);
  margin-bottom: 6px;
}}

.login-body .form-group select,
.login-body .form-group input {{
  width: 100%;
  padding: 12px 16px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s;
  background: #fafcfd;
}}

.login-body .form-group select:focus,
.login-body .form-group input:focus {{
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0,151,167,0.1);
  background: white;
}}

.role-selector {{
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}}

.role-btn {{
  flex: 1;
  padding: 12px;
  border: 2px solid var(--border);
  border-radius: var(--radius-sm);
  background: white;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s;
  font-family: inherit;
}}

.role-btn:hover {{
  border-color: var(--primary-light);
}}

.role-btn.active {{
  border-color: var(--primary);
  background: #e0f7fa;
}}

.role-btn .role-icon {{
  font-size: 24px;
  display: block;
  margin-bottom: 4px;
}}

.role-btn .role-name {{
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
}}

.role-btn .role-desc {{
  font-size: 11px;
  color: var(--text-light);
  margin-top: 2px;
}}

.login-btn {{
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 16px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(0,151,167,0.3);
  margin-top: 8px;
}}

.login-btn:hover {{
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,151,167,0.4);
}}

.login-error {{
  color: var(--danger);
  font-size: 13px;
  text-align: center;
  margin-top: 10px;
  min-height: 20px;
}}

.login-footer {{
  text-align: center;
  padding: 0 32px 20px;
  font-size: 12px;
  color: var(--text-light);
}}

/* ===== USER INFO BAR ===== */
.user-bar {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
}}

.user-avatar {{
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  border: 2px solid rgba(255,255,255,0.4);
}}

.user-info {{
  display: flex;
  flex-direction: column;
  line-height: 1.3;
}}

.user-name-display {{
  font-size: 14px;
  font-weight: 600;
}}

.user-role-display {{
  font-size: 11px;
  opacity: 0.8;
}}

.logout-btn {{
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  color: white;
  padding: 6px 14px;
  border-radius: 16px;
  cursor: pointer;
  font-size: 12px;
  font-family: inherit;
  transition: all 0.2s;
}}

.logout-btn:hover {{
  background: rgba(239,83,80,0.8);
}}

/* ===== CHANGE PASSWORD MODAL ===== */
.pwd-modal {{
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 250;
  justify-content: center;
  align-items: center;
}}

.pwd-modal.active {{ display: flex; }}

.pwd-modal-box {{
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  width: 400px;
  max-width: 90%;
  padding: 28px;
  animation: slideDown 0.3s ease;
}}

.pwd-modal-box h3 {{
  font-size: 16px;
  color: var(--primary-dark);
  margin-bottom: 16px;
}}

/* ===== MAIN APP STYLES ===== */
.app-container {{ display: none; }}
.app-container.visible {{ display: block; }}

.header {{
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 50%, var(--primary-light) 100%);
  color: white;
  padding: 0;
  box-shadow: 0 4px 20px rgba(0,151,167,0.3);
  position: sticky;
  top: 0;
  z-index: 100;
}}

.header-inner {{
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 12px 24px;
  gap: 16px;
}}

.logo-container {{
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}}

.logo-img {{
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: white;
  padding: 3px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}}

.header-title h1 {{ font-size: 22px; font-weight: 700; letter-spacing: 1px; text-shadow: 0 1px 3px rgba(0,0,0,0.2); }}
.header-title p {{ font-size: 12px; opacity: 0.85; font-weight: 300; }}

.header-right {{
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
}}

.header-nav {{
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}}

.nav-btn {{
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  font-family: inherit;
  transition: all 0.2s;
  white-space: nowrap;
}}

.nav-btn:hover, .nav-btn.active {{
  background: rgba(255,255,255,0.95);
  color: var(--primary-dark);
  font-weight: 500;
}}

.nav-btn.hidden {{ display: none; }}

.stats-bar {{
  background: white;
  border-bottom: 1px solid var(--border);
  padding: 12px 24px;
}}

.stats-inner {{
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  align-items: center;
}}

.stat-item {{ display: flex; align-items: center; gap: 8px; }}
.stat-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
.stat-label {{ font-size: 13px; color: var(--text-light); }}
.stat-num {{ font-size: 18px; font-weight: 700; }}

.main-container {{ max-width: 1400px; margin: 0 auto; padding: 20px 24px; }}

.view {{ display: none; }}
.view.active {{ display: block; }}

.form-card {{
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 28px;
  margin-bottom: 20px;
}}

.form-card h2 {{
  font-size: 18px;
  color: var(--primary-dark);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--primary-light);
  display: flex;
  align-items: center;
  gap: 8px;
}}

.form-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}}

.form-group {{ display: flex; flex-direction: column; gap: 6px; }}
.form-group.full-width {{ grid-column: 1 / -1; }}
.form-group label {{ font-size: 13px; font-weight: 500; color: var(--text-light); }}
.form-group label .required {{ color: var(--danger); }}

.form-group input,
.form-group select,
.form-group textarea {{
  padding: 10px 14px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
  background: #fafcfd;
}}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {{
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0,151,167,0.1);
  background: white;
}}

.form-group textarea {{ resize: vertical; min-height: 80px; }}

.form-actions {{ display: flex; gap: 10px; margin-top: 20px; justify-content: flex-end; }}

.btn {{
  padding: 10px 24px; border: none; border-radius: var(--radius-sm);
  font-size: 14px; font-weight: 500; font-family: inherit; cursor: pointer;
  transition: all 0.2s; display: inline-flex; align-items: center; gap: 6px;
}}

.btn-primary {{
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white; box-shadow: 0 2px 8px rgba(0,151,167,0.3);
}}
.btn-primary:hover {{ transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,151,167,0.4); }}
.btn-secondary {{ background: #eceff1; color: var(--text); }}
.btn-secondary:hover {{ background: #cfd8dc; }}
.btn-success {{ background: var(--success); color: white; }}
.btn-warning {{ background: var(--warning); color: white; }}
.btn-danger {{ background: var(--danger); color: white; }}
.btn-info {{ background: var(--info); color: white; }}
.btn-sm {{ padding: 6px 14px; font-size: 12px; }}

.assignee-selector {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-start; }}
.dept-select-wrapper, .people-select-wrapper {{ flex: 1; min-width: 200px; }}
.add-assignee-btn {{ margin-top: 22px; }}

.selected-assignees {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}

.assignee-tag {{
  background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
  color: var(--primary-dark); padding: 5px 12px; border-radius: 16px; font-size: 13px;
  display: flex; align-items: center; gap: 6px; animation: fadeIn 0.3s ease;
}}

.assignee-tag .remove-btn {{
  cursor: pointer; font-weight: bold; width: 18px; height: 18px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%; background: rgba(0,0,0,0.1); font-size: 11px;
}}
.assignee-tag .remove-btn:hover {{ background: var(--danger); color: white; }}

.priority-badge {{ padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; display: inline-block; }}
.priority-urgent {{ background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }}
.priority-high {{ background: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }}
.priority-medium {{ background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }}
.priority-low {{ background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }}

.status-badge {{ padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; display: inline-block; }}
.status-pending {{ background: #fce4ec; color: #c62828; }}
.status-progress {{ background: #e3f2fd; color: #1565c0; }}
.status-review {{ background: #fff8e1; color: #f57f17; }}
.status-done {{ background: #e8f5e9; color: #2e7d32; }}
.status-cancelled {{ background: #eceff1; color: #546e7a; }}

.task-filters {{
  background: var(--card-bg); border-radius: var(--radius); box-shadow: var(--shadow);
  padding: 16px 20px; margin-bottom: 16px; display: flex; gap: 12px; flex-wrap: wrap; align-items: center;
}}

.task-filters input, .task-filters select {{
  padding: 8px 14px; border: 1.5px solid var(--border); border-radius: var(--radius-sm);
  font-size: 13px; font-family: inherit; background: #fafcfd;
}}
.task-filters input {{ flex: 1; min-width: 200px; }}

.task-list {{ display: flex; flex-direction: column; gap: 12px; }}

.task-card {{
  background: var(--card-bg); border-radius: var(--radius); box-shadow: var(--shadow);
  padding: 20px; transition: all 0.2s; border-left: 4px solid var(--primary); cursor: pointer;
}}
.task-card:hover {{ box-shadow: var(--shadow-lg); transform: translateY(-2px); }}
.task-card.priority-urgent-card {{ border-left-color: #c62828; }}
.task-card.priority-high-card {{ border-left-color: #e65100; }}
.task-card.priority-medium-card {{ border-left-color: #1565c0; }}
.task-card.priority-low-card {{ border-left-color: #2e7d32; }}

.task-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; gap: 12px; }}
.task-id {{ font-size: 12px; color: var(--primary); font-weight: 500; background: #e0f7fa; padding: 2px 8px; border-radius: 4px; }}
.task-title {{ font-size: 16px; font-weight: 600; color: var(--text); flex: 1; }}
.task-meta {{ display: flex; gap: 16px; flex-wrap: wrap; font-size: 13px; color: var(--text-light); margin-top: 8px; }}
.task-meta span {{ display: flex; align-items: center; gap: 4px; }}
.task-assignees {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }}
.task-assignee-chip {{ background: #f5f5f5; padding: 2px 10px; border-radius: 12px; font-size: 12px; color: var(--text); }}

.task-progress-bar {{ margin-top: 12px; height: 6px; background: #e0e8ec; border-radius: 3px; overflow: hidden; }}
.task-progress-fill {{ height: 100%; border-radius: 3px; transition: width 0.5s ease; background: linear-gradient(90deg, var(--primary-light), var(--primary)); }}

.modal-overlay {{
  display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); z-index: 200;
  justify-content: center; align-items: flex-start; padding: 40px 20px; overflow-y: auto;
}}
.modal-overlay.active {{ display: flex; }}

.modal {{
  background: white; border-radius: var(--radius); box-shadow: var(--shadow-lg);
  width: 100%; max-width: 800px; animation: slideDown 0.3s ease;
}}
.modal-header {{
  padding: 20px 24px; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
}}
.modal-header h2 {{ font-size: 18px; color: var(--primary-dark); }}
.modal-close {{
  width: 32px; height: 32px; border: none; background: #eceff1; border-radius: 50%;
  cursor: pointer; font-size: 18px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;
}}
.modal-close:hover {{ background: var(--danger); color: white; }}
.modal-body {{ padding: 24px; max-height: 70vh; overflow-y: auto; }}

.detail-section {{ margin-bottom: 20px; }}
.detail-section h3 {{
  font-size: 14px; font-weight: 600; color: var(--primary-dark);
  margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid var(--border);
}}
.detail-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
.detail-item {{ display: flex; flex-direction: column; gap: 2px; }}
.detail-label {{ font-size: 12px; color: var(--text-light); }}
.detail-value {{ font-size: 14px; font-weight: 500; }}

.progress-log {{ margin-top: 16px; }}
.log-entry {{
  padding: 12px 16px; background: #fafcfd; border-radius: var(--radius-sm);
  margin-bottom: 8px; border-left: 3px solid var(--primary-light);
}}
.log-entry .log-time {{ font-size: 11px; color: var(--text-light); }}
.log-entry .log-author {{ font-size: 12px; font-weight: 500; color: var(--primary-dark); }}
.log-entry .log-content {{ font-size: 13px; margin-top: 4px; color: var(--text); }}

.add-progress {{ display: flex; gap: 8px; margin-top: 12px; }}
.add-progress textarea {{
  flex: 1; padding: 10px; border: 1.5px solid var(--border); border-radius: var(--radius-sm);
  font-size: 13px; font-family: inherit; resize: vertical; min-height: 60px;
}}
.add-progress textarea:focus {{ outline: none; border-color: var(--primary); }}

.dashboard-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
.dash-card {{ background: var(--card-bg); border-radius: var(--radius); box-shadow: var(--shadow); padding: 24px; }}
.dash-card h3 {{ font-size: 15px; color: var(--primary-dark); margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}

.overdue-item {{
  padding: 10px; background: #fff3e0; border-radius: var(--radius-sm);
  margin-bottom: 8px; border-left: 3px solid var(--warning);
}}
.overdue-item .task-name {{ font-weight: 500; font-size: 14px; }}
.overdue-item .overdue-info {{ font-size: 12px; color: var(--danger); margin-top: 2px; }}

.chart-bar {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }}
.chart-bar-label {{ width: 80px; font-size: 12px; text-align: right; color: var(--text-light); }}
.chart-bar-track {{ flex: 1; height: 24px; background: #eceff1; border-radius: 12px; overflow: hidden; }}
.chart-bar-fill {{
  height: 100%; border-radius: 12px; display: flex; align-items: center; padding-left: 10px;
  font-size: 12px; color: white; font-weight: 500; transition: width 0.5s ease;
}}

.empty-state {{ text-align: center; padding: 60px 20px; color: var(--text-light); }}
.empty-state .icon {{ font-size: 48px; margin-bottom: 16px; }}
.empty-state p {{ font-size: 15px; }}
.no-data {{ text-align: center; padding: 40px; color: var(--text-light); font-size: 14px; }}

/* User Management Table */
.user-table {{
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}}
.user-table th, .user-table td {{
  padding: 10px 14px;
  text-align: left;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}}
.user-table th {{
  background: #f5f7fa;
  font-weight: 600;
  color: var(--primary-dark);
  position: sticky;
  top: 0;
}}
.user-table tr:hover {{
  background: #f0f7fa;
}}

.role-tag {{
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  display: inline-block;
}}
.role-admin {{ background: #f3e5f5; color: #7b1fa2; }}
.role-manager {{ background: #e3f2fd; color: #1565c0; }}
.role-executor {{ background: #e8f5e9; color: #2e7d32; }}

.user-table-wrapper {{
  max-height: 500px;
  overflow-y: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(-5px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes slideDown {{
  from {{ opacity: 0; transform: translateY(-20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.toast-container {{
  position: fixed; top: 80px; right: 20px; z-index: 300;
  display: flex; flex-direction: column; gap: 8px;
}}
.toast {{
  padding: 12px 20px; border-radius: var(--radius-sm); color: white; font-size: 14px;
  box-shadow: var(--shadow-lg); animation: slideIn 0.3s ease; min-width: 260px;
}}
.toast-success {{ background: var(--success); }}
.toast-error {{ background: var(--danger); }}
.toast-info {{ background: var(--info); }}

@keyframes slideIn {{
  from {{ opacity: 0; transform: translateX(50px); }}
  to {{ opacity: 1; transform: translateX(0); }}
}}

@media (max-width: 768px) {{
  .header-inner {{ flex-direction: column; gap: 10px; }}
  .header-nav {{ justify-content: center; }}
  .header-right {{ flex-direction: column; }}
  .logo-img {{ width: 44px; height: 44px; }}
  .header-title h1 {{ font-size: 18px; }}
  .form-grid {{ grid-template-columns: 1fr; }}
  .detail-grid {{ grid-template-columns: 1fr; }}
  .task-header {{ flex-direction: column; }}
  .stats-inner {{ justify-content: center; }}
  .user-bar {{ flex-wrap: wrap; justify-content: center; }}
}}

@media print {{
  .header, .stats-bar, .task-filters, .form-actions, .nav-btn, .btn, .login-screen {{ display: none !important; }}
  .task-card {{ break-inside: avoid; box-shadow: none; border: 1px solid #ddd; }}
}}
</style>
</head>
<body>

<!-- ===== LOGIN SCREEN ===== -->
<div class="login-screen" id="loginScreen">
  <div class="login-card">
    <div class="login-header">
      <img src="data:image/jpeg;base64,{logo_b64}" alt="水試所">
      <h1>&#x1F41F; 水試所業務交辦小助手</h1>
      <p>農業部水產試驗所 Fisheries Research Institute</p>
    </div>
    <div class="login-body">
      <div class="form-group">
        <label>選擇登入角色</label>
        <div class="role-selector">
          <button type="button" class="role-btn active" onclick="selectRole('manager', this)">
            <span class="role-icon">&#x1f4cb;</span>
            <span class="role-name">交辦人</span>
            <span class="role-desc">建立與管理交辦事項</span>
          </button>
          <button type="button" class="role-btn" onclick="selectRole('executor', this)">
            <span class="role-icon">&#x1f4dd;</span>
            <span class="role-name">執行人</span>
            <span class="role-desc">查看與回報執行進度</span>
          </button>
          <button type="button" class="role-btn" onclick="selectRole('admin', this)">
            <span class="role-icon">&#x2699;&#xfe0f;</span>
            <span class="role-name">管理員</span>
            <span class="role-desc">系統與帳號管理</span>
          </button>
        </div>
      </div>
      <div class="form-group">
        <label>選擇單位</label>
        <select id="loginDept" onchange="onLoginDeptChange()">
          <option value="">請選擇單位</option>
        </select>
      </div>
      <div class="form-group">
        <label>選擇人員</label>
        <select id="loginPerson">
          <option value="">請先選擇單位</option>
        </select>
      </div>
      <div class="form-group">
        <label>密碼</label>
        <input type="password" id="loginPassword" placeholder="請輸入密碼（預設：1234）" onkeydown="if(event.key==='Enter')doLogin()">
      </div>
      <button class="login-btn" onclick="doLogin()">&#x1f512; 登入系統</button>
      <div class="login-error" id="loginError"></div>
    </div>
    <div class="login-footer">
      首次登入預設密碼為 <strong>1234</strong>，請登入後立即修改密碼
    </div>
  </div>
</div>

<!-- ===== MAIN APP ===== -->
<div class="app-container" id="appContainer">
  <div class="header">
    <div class="header-inner">
      <div class="logo-container">
        <img src="data:image/jpeg;base64,{logo_b64}" alt="水試所" class="logo-img">
        <div class="header-title">
          <h1>&#x1F41F; 水試所業務交辦小助手</h1>
          <p>農業部水產試驗所 Fisheries Research Institute</p>
        </div>
      </div>
      <div class="header-right">
        <div class="header-nav">
          <button class="nav-btn active" onclick="switchView('dashboard', this)" data-view="dashboard">&#x1f4ca; 儀表板</button>
          <button class="nav-btn" onclick="switchView('create', this)" data-view="create" id="navCreate">&#x2795; 新增交辦</button>
          <button class="nav-btn" onclick="switchView('list', this)" data-view="list">&#x1f4cb; 交辦清單</button>
          <button class="nav-btn" onclick="switchView('mytasks', this)" data-view="mytasks" id="navMyTasks">&#x1f4cc; 我的任務</button>
          <button class="nav-btn" onclick="switchView('search', this)" data-view="search">&#x1f50d; 查詢追蹤</button>
          <button class="nav-btn" onclick="switchView('users', this)" data-view="users" id="navUsers">&#x1f465; 帳號管理</button>
          <button class="nav-btn" onclick="exportData()">&#x1f4e5; 匯出</button>
          <button class="nav-btn" onclick="document.getElementById('importFile').click()">&#x1f4e4; 匯入</button>
          <input type="file" id="importFile" accept=".json" style="display:none" onchange="importData(event)">
        </div>
        <div class="user-bar">
          <div class="user-avatar" id="userAvatar">&#x1f464;</div>
          <div class="user-info">
            <span class="user-name-display" id="userNameDisplay"></span>
            <span class="user-role-display" id="userRoleDisplay"></span>
          </div>
          <button class="logout-btn" onclick="showChangePwd()">&#x1f511; 改密碼</button>
          <button class="logout-btn" onclick="doLogout()">&#x1f6aa; 登出</button>
        </div>
      </div>
    </div>
  </div>

  <div class="stats-bar">
    <div class="stats-inner">
      <div class="stat-item"><div class="stat-dot" style="background:var(--primary)"></div><span class="stat-label">全部</span><span class="stat-num" id="stat-total">0</span></div>
      <div class="stat-item"><div class="stat-dot" style="background:#c62828"></div><span class="stat-label">待辦中</span><span class="stat-num" id="stat-pending">0</span></div>
      <div class="stat-item"><div class="stat-dot" style="background:#1565c0"></div><span class="stat-label">執行中</span><span class="stat-num" id="stat-progress">0</span></div>
      <div class="stat-item"><div class="stat-dot" style="background:#f57f17"></div><span class="stat-label">待審核</span><span class="stat-num" id="stat-review">0</span></div>
      <div class="stat-item"><div class="stat-dot" style="background:#2e7d32"></div><span class="stat-label">已完成</span><span class="stat-num" id="stat-done">0</span></div>
      <div class="stat-item"><div class="stat-dot" style="background:var(--danger)"></div><span class="stat-label">已逾期</span><span class="stat-num" id="stat-overdue">0</span></div>
    </div>
  </div>

  <div class="toast-container" id="toastContainer"></div>

  <div class="main-container">
    <!-- Dashboard -->
    <div class="view active" id="view-dashboard">
      <div class="dashboard-grid">
        <div class="dash-card"><h3>&#x1f4ca; 狀態分布</h3><div id="statusChart"></div></div>
        <div class="dash-card"><h3>&#x1f525; 重要程度分布</h3><div id="priorityChart"></div></div>
        <div class="dash-card" style="grid-column:1/-1"><h3>&#x26a0;&#xfe0f; 即將到期 / 逾期項目</h3><div id="overdueList"></div></div>
        <div class="dash-card" style="grid-column:1/-1"><h3>&#x1f4c5; 最近交辦事項</h3><div id="recentTasks"></div></div>
      </div>
    </div>

    <!-- Create -->
    <div class="view" id="view-create">
      <div class="form-card">
        <h2>&#x1f4dd; 新增交辦事項</h2>
        <form id="taskForm" onsubmit="return createTask(event)">
          <div class="form-grid">
            <div class="form-group"><label>交辦事項名稱 <span class="required">*</span></label><input type="text" id="taskTitle" required placeholder="請輸入交辦事項名稱"></div>
            <div class="form-group"><label>重要程度 <span class="required">*</span></label><select id="taskPriority" required><option value="">請選擇</option><option value="urgent">&#x1f534; 緊急</option><option value="high">&#x1f7e0; 高</option><option value="medium">&#x1f535; 中</option><option value="low">&#x1f7e2; 低</option></select></div>
            <div class="form-group"><label>交辦日期 <span class="required">*</span></label><input type="date" id="taskStartDate" required></div>
            <div class="form-group"><label>預定完成日期 <span class="required">*</span></label><input type="date" id="taskDueDate" required></div>
            <div class="form-group"><label>交辦人</label><input type="text" id="taskAssigner" placeholder="交辦人姓名" readonly></div>
            <div class="form-group"><label>類別標籤</label><select id="taskCategory"><option value="">請選擇</option><option value="公文處理">公文處理</option><option value="研究計畫">研究計畫</option><option value="行政事務">行政事務</option><option value="會議決議">會議決議</option><option value="專案執行">專案執行</option><option value="採購事項">採購事項</option><option value="報告撰寫">報告撰寫</option><option value="資料彙整">資料彙整</option><option value="其他">其他</option></select></div>
            <div class="form-group full-width"><label>工作內容摘要 <span class="required">*</span></label><textarea id="taskDescription" required placeholder="請詳細描述交辦工作內容..."></textarea></div>
            <div class="form-group full-width">
              <label>指定單位與人員 <span class="required">*</span></label>
              <div class="assignee-selector">
                <div class="dept-select-wrapper"><label style="font-size:12px">選擇單位</label><select id="deptSelect" onchange="onDeptChange()"><option value="">請選擇單位</option></select></div>
                <div class="people-select-wrapper"><label style="font-size:12px">選擇人員</label><select id="personSelect"><option value="">請先選擇單位</option></select></div>
                <button type="button" class="btn btn-primary btn-sm add-assignee-btn" onclick="addAssignee()">+ 新增</button>
              </div>
              <div class="selected-assignees" id="selectedAssignees"></div>
            </div>
            <div class="form-group full-width"><label>附註說明</label><textarea id="taskNotes" placeholder="其他注意事項或備註..." rows="2"></textarea></div>
          </div>
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" onclick="resetForm()">清除</button>
            <button type="submit" class="btn btn-primary">&#x2714; 建立交辦事項</button>
          </div>
        </form>
      </div>
    </div>

    <!-- List -->
    <div class="view" id="view-list">
      <div class="task-filters">
        <input type="text" id="filterKeyword" placeholder="&#x1f50d; 搜尋交辦事項（ID、名稱、人員...）" oninput="renderTaskList()">
        <select id="filterStatus" onchange="renderTaskList()"><option value="">全部狀態</option><option value="pending">待辦中</option><option value="progress">執行中</option><option value="review">待審核</option><option value="done">已完成</option><option value="cancelled">已取消</option></select>
        <select id="filterPriority" onchange="renderTaskList()"><option value="">全部重要程度</option><option value="urgent">緊急</option><option value="high">高</option><option value="medium">中</option><option value="low">低</option></select>
        <select id="filterDept" onchange="renderTaskList()"><option value="">全部單位</option></select>
        <select id="filterSort" onchange="renderTaskList()"><option value="newest">最新建立</option><option value="oldest">最早建立</option><option value="due-asc">到期日（近→遠）</option><option value="due-desc">到期日（遠→近）</option><option value="priority">重要程度</option></select>
      </div>
      <div class="task-list" id="taskList"></div>
    </div>

    <!-- My Tasks (Executor view) -->
    <div class="view" id="view-mytasks">
      <div class="form-card">
        <h2>&#x1f4cc; 我的交辦任務</h2>
        <p style="color:var(--text-light);font-size:14px;margin-top:-12px;margin-bottom:16px">以下為指派給您的交辦事項，您可以更新執行進度</p>
      </div>
      <div class="task-list" id="myTaskList"></div>
    </div>

    <!-- Search -->
    <div class="view" id="view-search">
      <div class="form-card">
        <h2>&#x1f50d; 查詢追蹤交辦事項</h2>
        <div class="form-grid">
          <div class="form-group"><label>交辦事項 ID</label><input type="text" id="searchId" placeholder="例如: FRI-20260322-001" oninput="searchTask()"></div>
          <div class="form-group"><label>被交辦人員</label><input type="text" id="searchPerson" placeholder="輸入人員姓名" oninput="searchTask()"></div>
        </div>
      </div>
      <div class="task-list" id="searchResults"></div>
    </div>

    <!-- User Management -->
    <div class="view" id="view-users">
      <div class="form-card">
        <h2>&#x1f465; 帳號管理</h2>
        <div class="form-grid" style="margin-bottom:16px">
          <div class="form-group">
            <label>搜尋帳號</label>
            <input type="text" id="userSearchInput" placeholder="輸入姓名、單位或 Email..." oninput="renderUserTable()">
          </div>
          <div class="form-group">
            <label>篩選角色</label>
            <select id="userFilterRole" onchange="renderUserTable()">
              <option value="">全部角色</option>
              <option value="admin">管理員</option>
              <option value="manager">交辦人</option>
              <option value="executor">執行人</option>
            </select>
          </div>
        </div>
        <div class="user-table-wrapper">
          <table class="user-table">
            <thead>
              <tr>
                <th>姓名</th>
                <th>單位</th>
                <th>Email</th>
                <th>角色</th>
                <th>帳號狀態</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody id="userTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Task Detail Modal -->
<div class="modal-overlay" id="taskModal">
  <div class="modal">
    <div class="modal-header">
      <h2 id="modalTitle">交辦事項詳情</h2>
      <button class="modal-close" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>

<!-- Change Password Modal -->
<div class="pwd-modal" id="pwdModal">
  <div class="pwd-modal-box">
    <h3>&#x1f511; 修改密碼</h3>
    <div class="form-group" style="margin-bottom:12px">
      <label>目前密碼</label>
      <input type="password" id="pwdOld" placeholder="請輸入目前密碼" style="width:100%;padding:10px 14px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-family:inherit">
    </div>
    <div class="form-group" style="margin-bottom:12px">
      <label>新密碼</label>
      <input type="password" id="pwdNew" placeholder="請輸入新密碼" style="width:100%;padding:10px 14px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-family:inherit">
    </div>
    <div class="form-group" style="margin-bottom:16px">
      <label>確認新密碼</label>
      <input type="password" id="pwdConfirm" placeholder="再次輸入新密碼" style="width:100%;padding:10px 14px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-family:inherit">
    </div>
    <div style="display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-secondary" onclick="closePwdModal()">取消</button>
      <button class="btn btn-primary" onclick="changePassword()">確認修改</button>
    </div>
  </div>
</div>

<script>
const PERSONNEL = {personnel_js};
const DEPT_CATEGORIES = {categories_js};

const PRIORITY_MAP = {{
  urgent: {{ label: '緊急', class: 'priority-urgent', order: 0 }},
  high:   {{ label: '高',   class: 'priority-high',   order: 1 }},
  medium: {{ label: '中',   class: 'priority-medium',  order: 2 }},
  low:    {{ label: '低',   class: 'priority-low',     order: 3 }}
}};

const STATUS_MAP = {{
  pending:   {{ label: '待辦中', class: 'status-pending' }},
  progress:  {{ label: '執行中', class: 'status-progress' }},
  review:    {{ label: '待審核', class: 'status-review' }},
  done:      {{ label: '已完成', class: 'status-done' }},
  cancelled: {{ label: '已取消', class: 'status-cancelled' }}
}};

const ROLE_MAP = {{
  admin:    {{ label: '管理員', class: 'role-admin', icon: '&#x2699;&#xfe0f;' }},
  manager:  {{ label: '交辦人', class: 'role-manager', icon: '&#x1f4cb;' }},
  executor: {{ label: '執行人', class: 'role-executor', icon: '&#x1f4dd;' }}
}};

let tasks = JSON.parse(localStorage.getItem('fri_tasks') || '[]');
let users = JSON.parse(localStorage.getItem('fri_users') || '{{}}');
let currentUser = JSON.parse(sessionStorage.getItem('fri_session') || 'null');
let currentAssignees = [];
let editingTaskId = null;
let selectedRole = 'manager';

// ===== USER MANAGEMENT =====
function initUsers() {{
  if (Object.keys(users).length === 0) {{
    // 唯一預設管理員：曾振德（主任秘書室）
    const defaultAdmin = 'cttseng@mail.tfrin.gov.tw';
    for (const [dept, people] of Object.entries(PERSONNEL)) {{
      for (const p of people) {{
        const key = p.email.trim().toLowerCase();
        let role = 'executor';
        if (key === defaultAdmin) role = 'admin';
        users[key] = {{
          name: p.name.trim(),
          email: p.email.trim(),
          dept: dept,
          password: '1234',
          role: role,
          active: true,
          createdAt: new Date().toISOString()
        }};
      }}
    }}
    saveUsers();
  }}
}}

function saveUsers() {{ localStorage.setItem('fri_users', JSON.stringify(users)); }}
function saveTasks() {{ localStorage.setItem('fri_tasks', JSON.stringify(tasks)); }}

// ===== LOGIN =====
function initLoginDepts() {{
  const sel = document.getElementById('loginDept');
  for (const [cat, depts] of Object.entries(DEPT_CATEGORIES)) {{
    const g = document.createElement('optgroup');
    g.label = cat;
    for (const d of depts) {{
      if (PERSONNEL[d]) {{
        const o = document.createElement('option');
        o.value = d; o.textContent = d;
        g.appendChild(o);
      }}
    }}
    sel.appendChild(g);
  }}
}}

function onLoginDeptChange() {{
  const dept = document.getElementById('loginDept').value;
  const ps = document.getElementById('loginPerson');
  ps.innerHTML = '<option value="">請選擇人員</option>';
  if (dept && PERSONNEL[dept]) {{
    PERSONNEL[dept].forEach(p => {{
      const o = document.createElement('option');
      o.value = p.email.trim().toLowerCase();
      o.textContent = p.name;
      ps.appendChild(o);
    }});
  }}
}}

function selectRole(role, btn) {{
  selectedRole = role;
  document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}}

function doLogin() {{
  const dept = document.getElementById('loginDept').value;
  const email = document.getElementById('loginPerson').value;
  const pwd = document.getElementById('loginPassword').value;
  const errEl = document.getElementById('loginError');

  if (!dept || !email) {{
    errEl.textContent = '請選擇單位及人員';
    return;
  }}
  if (!pwd) {{
    errEl.textContent = '請輸入密碼';
    return;
  }}

  const userKey = email.trim().toLowerCase();
  const user = users[userKey];

  if (!user) {{
    errEl.textContent = '帳號不存在，請聯繫管理員';
    return;
  }}

  if (!user.active) {{
    errEl.textContent = '此帳號已被停用，請聯繫管理員';
    return;
  }}

  if (user.password !== pwd) {{
    errEl.textContent = '密碼錯誤，請重新輸入';
    return;
  }}

  // Check role permission
  if (selectedRole === 'admin' && user.role !== 'admin') {{
    errEl.textContent = '此帳號無管理員權限';
    return;
  }}

  if (selectedRole === 'manager' && user.role === 'executor') {{
    // Allow executor to upgrade login if they try manager, but show warning
    // Actually let's just restrict: only manager/admin can log in as manager
    errEl.textContent = '此帳號無交辦人權限，請聯繫管理員升級角色';
    return;
  }}

  // Login success
  currentUser = {{
    email: user.email,
    name: user.name,
    dept: user.dept || dept,
    role: selectedRole === 'admin' ? 'admin' : user.role,
    loginRole: selectedRole
  }};

  sessionStorage.setItem('fri_session', JSON.stringify(currentUser));
  errEl.textContent = '';
  enterApp();
}}

function enterApp() {{
  document.getElementById('loginScreen').classList.add('hidden');
  document.getElementById('appContainer').classList.add('visible');

  // Update header
  document.getElementById('userNameDisplay').textContent = currentUser.name + '（' + currentUser.dept + '）';
  const ri = ROLE_MAP[currentUser.loginRole] || ROLE_MAP.executor;
  document.getElementById('userRoleDisplay').textContent = ri.label;
  document.getElementById('userAvatar').innerHTML = ri.icon;

  // Role-based nav visibility
  const isManager = currentUser.loginRole === 'manager' || currentUser.loginRole === 'admin';
  const isAdmin = currentUser.loginRole === 'admin';

  document.getElementById('navCreate').classList.toggle('hidden', !isManager);
  document.getElementById('navUsers').classList.toggle('hidden', !isAdmin);
  document.getElementById('navMyTasks').classList.toggle('hidden', isManager && !isAdmin);

  // Auto-fill assigner
  document.getElementById('taskAssigner').value = currentUser.name;

  initDeptSelects();
  resetForm();
  updateStats();
  renderDashboard();
}}

function doLogout() {{
  sessionStorage.removeItem('fri_session');
  currentUser = null;
  document.getElementById('loginScreen').classList.remove('hidden');
  document.getElementById('appContainer').classList.remove('visible');
  document.getElementById('loginPassword').value = '';
  document.getElementById('loginError').textContent = '';
}}

// ===== CHANGE PASSWORD =====
function showChangePwd() {{
  document.getElementById('pwdModal').classList.add('active');
  document.getElementById('pwdOld').value = '';
  document.getElementById('pwdNew').value = '';
  document.getElementById('pwdConfirm').value = '';
}}

function closePwdModal() {{ document.getElementById('pwdModal').classList.remove('active'); }}

function changePassword() {{
  const old = document.getElementById('pwdOld').value;
  const newP = document.getElementById('pwdNew').value;
  const confirm = document.getElementById('pwdConfirm').value;

  if (!old || !newP || !confirm) {{ showToast('請填寫所有欄位', 'error'); return; }}

  const key = currentUser.email.trim().toLowerCase();
  if (users[key].password !== old) {{ showToast('目前密碼錯誤', 'error'); return; }}
  if (newP.length < 4) {{ showToast('新密碼至少 4 個字元', 'error'); return; }}
  if (newP !== confirm) {{ showToast('兩次新密碼不一致', 'error'); return; }}

  users[key].password = newP;
  saveUsers();
  closePwdModal();
  showToast('密碼已修改成功');
}}

// ===== HELPER =====
function generateId() {{
  const d = new Date();
  const ds = d.getFullYear().toString() + (d.getMonth()+1).toString().padStart(2,'0') + d.getDate().toString().padStart(2,'0');
  const existing = tasks.filter(t => t.id && t.id.includes(ds));
  return 'FRI-' + ds + '-' + (existing.length + 1).toString().padStart(3,'0');
}}

function showToast(msg, type='success') {{
  const c = document.getElementById('toastContainer');
  const t = document.createElement('div');
  t.className = 'toast toast-' + type;
  t.textContent = msg;
  c.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}}

function escapeHtml(s) {{
  if (!s) return '';
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function getDaysLeft(d) {{
  const today = new Date(); today.setHours(0,0,0,0);
  const due = new Date(d); due.setHours(0,0,0,0);
  return Math.floor((due - today) / 86400000);
}}

function canManage() {{
  return currentUser && (currentUser.loginRole === 'manager' || currentUser.loginRole === 'admin');
}}

function isAdmin() {{
  return currentUser && currentUser.loginRole === 'admin';
}}

// ===== DEPT SELECTS =====
function initDeptSelects() {{
  const ds = document.getElementById('deptSelect');
  const fd = document.getElementById('filterDept');
  ds.innerHTML = '<option value="">請選擇單位</option>';
  fd.innerHTML = '<option value="">全部單位</option>';
  for (const [cat, depts] of Object.entries(DEPT_CATEGORIES)) {{
    const g1 = document.createElement('optgroup'); g1.label = cat;
    const g2 = document.createElement('optgroup'); g2.label = cat;
    for (const dept of depts) {{
      if (PERSONNEL[dept]) {{
        const o1 = document.createElement('option'); o1.value = dept; o1.textContent = dept;
        g1.appendChild(o1);
        g2.appendChild(o1.cloneNode(true));
      }}
    }}
    ds.appendChild(g1);
    fd.appendChild(g2);
  }}
}}

function onDeptChange() {{
  const dept = document.getElementById('deptSelect').value;
  const ps = document.getElementById('personSelect');
  ps.innerHTML = '<option value="">請選擇人員</option>';
  if (dept && PERSONNEL[dept]) {{
    PERSONNEL[dept].forEach(p => {{
      const o = document.createElement('option');
      o.value = JSON.stringify(p);
      o.textContent = p.name + ' (' + p.email + ')';
      ps.appendChild(o);
    }});
  }}
}}

function addAssignee() {{
  const dept = document.getElementById('deptSelect').value;
  const pv = document.getElementById('personSelect').value;
  if (!dept || !pv) {{ showToast('請先選擇單位和人員', 'error'); return; }}
  const person = JSON.parse(pv);
  if (currentAssignees.find(a => a.email === person.email)) {{ showToast('此人員已在名單中', 'error'); return; }}
  currentAssignees.push({{ ...person, dept }});
  renderAssignees();
}}

function removeAssignee(i) {{ currentAssignees.splice(i, 1); renderAssignees(); }}

function renderAssignees() {{
  document.getElementById('selectedAssignees').innerHTML = currentAssignees.map((a, i) =>
    '<div class="assignee-tag"><span>' + escapeHtml(a.dept) + ' - ' + escapeHtml(a.name) + '</span><span class="remove-btn" onclick="removeAssignee(' + i + ')">&times;</span></div>'
  ).join('');
}}

// ===== TASK CRUD =====
function createTask(e) {{
  e.preventDefault();
  if (!canManage()) {{ showToast('您沒有建立交辦事項的權限', 'error'); return false; }}
  if (currentAssignees.length === 0) {{ showToast('請至少指定一位交辦人員', 'error'); return false; }}
  const task = {{
    id: editingTaskId || generateId(),
    title: document.getElementById('taskTitle').value,
    priority: document.getElementById('taskPriority').value,
    startDate: document.getElementById('taskStartDate').value,
    dueDate: document.getElementById('taskDueDate').value,
    assigner: document.getElementById('taskAssigner').value,
    assignerEmail: currentUser.email,
    category: document.getElementById('taskCategory').value,
    description: document.getElementById('taskDescription').value,
    notes: document.getElementById('taskNotes').value,
    assignees: [...currentAssignees],
    status: 'pending', progress: 0, progressLog: [],
    createdAt: editingTaskId ? (tasks.find(t=>t.id===editingTaskId)||{{}}).createdAt || new Date().toISOString() : new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }};
  if (editingTaskId) {{
    const idx = tasks.findIndex(t => t.id === editingTaskId);
    if (idx >= 0) {{ task.status = tasks[idx].status; task.progress = tasks[idx].progress; task.progressLog = tasks[idx].progressLog; tasks[idx] = task; }}
    editingTaskId = null;
    showToast('交辦事項已更新');
  }} else {{
    tasks.unshift(task);
    showToast('交辦事項已建立！ID: ' + task.id);
  }}
  saveTasks(); resetForm(); updateStats();
  return false;
}}

function resetForm() {{
  document.getElementById('taskForm').reset();
  document.getElementById('taskStartDate').value = new Date().toISOString().split('T')[0];
  if (currentUser) document.getElementById('taskAssigner').value = currentUser.name;
  currentAssignees = []; renderAssignees(); editingTaskId = null;
}}

// ===== VIEWS =====
function switchView(view, btn) {{
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById('view-' + view).classList.add('active');
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  if (view === 'list') renderTaskList();
  if (view === 'dashboard') renderDashboard();
  if (view === 'mytasks') renderMyTasks();
  if (view === 'users') renderUserTable();
}}

function updateStats() {{
  const visibleTasks = getVisibleTasks();
  document.getElementById('stat-total').textContent = visibleTasks.length;
  document.getElementById('stat-pending').textContent = visibleTasks.filter(x => x.status === 'pending').length;
  document.getElementById('stat-progress').textContent = visibleTasks.filter(x => x.status === 'progress').length;
  document.getElementById('stat-review').textContent = visibleTasks.filter(x => x.status === 'review').length;
  document.getElementById('stat-done').textContent = visibleTasks.filter(x => x.status === 'done').length;
  document.getElementById('stat-overdue').textContent = visibleTasks.filter(x => x.status !== 'done' && x.status !== 'cancelled' && getDaysLeft(x.dueDate) < 0).length;
}}

function getVisibleTasks() {{
  if (!currentUser) return [];
  if (canManage()) return tasks;
  return tasks.filter(t => t.assignees.some(a => a.email.trim().toLowerCase() === currentUser.email.trim().toLowerCase()));
}}

function renderTaskCard(task) {{
  const dl = getDaysLeft(task.dueDate);
  const overdue = dl < 0 && task.status !== 'done' && task.status !== 'cancelled';
  const pi = PRIORITY_MAP[task.priority] || PRIORITY_MAP.medium;
  const si = STATUS_MAP[task.status] || STATUS_MAP.pending;
  let dueBadge = '';
  if (task.status === 'done') dueBadge = '<span style="color:var(--success)">&#x2714; 已完成</span>';
  else if (overdue) dueBadge = '<span style="color:var(--danger);font-weight:600">&#x26a0; 逾期 ' + Math.abs(dl) + ' 天</span>';
  else if (dl <= 3) dueBadge = '<span style="color:var(--warning)">&#x23f0; 剩餘 ' + dl + ' 天</span>';
  else dueBadge = '<span>剩餘 ' + dl + ' 天</span>';

  return '<div class="task-card priority-' + task.priority + '-card" onclick="showTaskDetail(\\''+task.id+'\\')"><div class="task-header"><div style="display:flex;flex-direction:column;gap:6px;flex:1"><div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><span class="task-id">' + task.id + '</span><span class="priority-badge ' + pi.class + '">' + pi.label + '</span><span class="status-badge ' + si.class + '">' + si.label + '</span>' + (task.category ? '<span style="font-size:12px;background:#f3e5f5;color:#7b1fa2;padding:2px 8px;border-radius:12px">' + escapeHtml(task.category) + '</span>' : '') + '</div><div class="task-title">' + escapeHtml(task.title) + '</div></div></div><div class="task-meta"><span>&#x1f4c5; 交辦: ' + task.startDate + '</span><span>&#x1f3af; 期限: ' + task.dueDate + '</span>' + dueBadge + (task.assigner ? '<span>&#x1f464; 交辦人: ' + escapeHtml(task.assigner) + '</span>' : '') + '</div><div class="task-assignees">' + task.assignees.map(a => '<span class="task-assignee-chip">' + escapeHtml(a.dept) + ' - ' + escapeHtml(a.name) + '</span>').join('') + '</div><div class="task-progress-bar"><div class="task-progress-fill" style="width:' + task.progress + '%;' + (task.status==='done'?'background:var(--success)':'') + '"></div></div><div style="font-size:12px;color:var(--text-light);margin-top:4px;text-align:right">進度: ' + task.progress + '%</div></div>';
}}

function renderTaskList() {{
  const kw = document.getElementById('filterKeyword').value.toLowerCase();
  const st = document.getElementById('filterStatus').value;
  const pr = document.getElementById('filterPriority').value;
  const dp = document.getElementById('filterDept').value;
  const so = document.getElementById('filterSort').value;
  let f = getVisibleTasks().filter(t => {{
    if (st && t.status !== st) return false;
    if (pr && t.priority !== pr) return false;
    if (dp && !t.assignees.some(a => a.dept === dp)) return false;
    if (kw) {{
      const s = (t.id+' '+t.title+' '+t.description+' '+t.assignees.map(a=>a.name+' '+a.dept).join(' ')+' '+(t.assigner||'')+' '+(t.category||'')).toLowerCase();
      if (!s.includes(kw)) return false;
    }}
    return true;
  }});
  f.sort((a,b) => {{
    switch(so) {{
      case 'newest': return new Date(b.createdAt)-new Date(a.createdAt);
      case 'oldest': return new Date(a.createdAt)-new Date(b.createdAt);
      case 'due-asc': return new Date(a.dueDate)-new Date(b.dueDate);
      case 'due-desc': return new Date(b.dueDate)-new Date(a.dueDate);
      case 'priority': return (PRIORITY_MAP[a.priority]?.order||2)-(PRIORITY_MAP[b.priority]?.order||2);
      default: return 0;
    }}
  }});
  const c = document.getElementById('taskList');
  c.innerHTML = f.length === 0 ? '<div class="empty-state"><div class="icon">&#x1f4cb;</div><p>目前沒有符合條件的交辦事項</p></div>' : f.map(renderTaskCard).join('');
}}

function renderMyTasks() {{
  if (!currentUser) return;
  const myEmail = currentUser.email.trim().toLowerCase();
  const myTasks = tasks.filter(t => t.assignees.some(a => a.email.trim().toLowerCase() === myEmail))
    .sort((a,b) => {{
      if (a.status === 'done' && b.status !== 'done') return 1;
      if (a.status !== 'done' && b.status === 'done') return -1;
      return new Date(a.dueDate) - new Date(b.dueDate);
    }});
  const c = document.getElementById('myTaskList');
  c.innerHTML = myTasks.length === 0 ? '<div class="empty-state"><div class="icon">&#x1f4cc;</div><p>目前沒有指派給您的交辦事項</p></div>' : myTasks.map(renderTaskCard).join('');
}}

function searchTask() {{
  const id = document.getElementById('searchId').value.trim().toUpperCase();
  const person = document.getElementById('searchPerson').value.trim();
  const c = document.getElementById('searchResults');
  if (!id && !person) {{ c.innerHTML = '<div class="empty-state"><div class="icon">&#x1f50d;</div><p>請輸入 ID 或人員姓名進行查詢</p></div>'; return; }}
  let r = getVisibleTasks().filter(t => {{
    if (id && !t.id.toUpperCase().includes(id)) return false;
    if (person && !t.assignees.some(a => a.name.includes(person))) return false;
    return true;
  }});
  c.innerHTML = r.length === 0 ? '<div class="empty-state"><div class="icon">&#x1f50d;</div><p>找不到符合條件的交辦事項</p></div>' : r.map(renderTaskCard).join('');
}}

// ===== TASK DETAIL MODAL =====
function showTaskDetail(taskId) {{
  const task = tasks.find(t => t.id === taskId);
  if (!task) return;
  const pi = PRIORITY_MAP[task.priority] || PRIORITY_MAP.medium;
  const si = STATUS_MAP[task.status] || STATUS_MAP.pending;
  const dl = getDaysLeft(task.dueDate);
  const overdue = dl < 0 && task.status !== 'done' && task.status !== 'cancelled';
  const isMyTask = task.assignees.some(a => a.email.trim().toLowerCase() === currentUser.email.trim().toLowerCase());
  const canEdit = canManage() || (task.assignerEmail && task.assignerEmail.trim().toLowerCase() === currentUser.email.trim().toLowerCase());

  document.getElementById('modalTitle').textContent = task.id + ' - ' + task.title;

  let h = '<div class="detail-section"><h3>&#x1f4cb; 基本資訊</h3><div class="detail-grid">' +
    '<div class="detail-item"><span class="detail-label">交辦事項 ID</span><span class="detail-value">' + task.id + '</span></div>' +
    '<div class="detail-item"><span class="detail-label">重要程度</span><span class="detail-value"><span class="priority-badge ' + pi.class + '">' + pi.label + '</span></span></div>' +
    '<div class="detail-item"><span class="detail-label">目前狀態</span><span class="detail-value"><span class="status-badge ' + si.class + '">' + si.label + '</span>' + (overdue ? ' <span style="color:var(--danger);font-size:12px;font-weight:600">（逾期 ' + Math.abs(dl) + ' 天）</span>' : '') + '</span></div>' +
    '<div class="detail-item"><span class="detail-label">交辦日期</span><span class="detail-value">' + task.startDate + '</span></div>' +
    '<div class="detail-item"><span class="detail-label">預定完成日期</span><span class="detail-value">' + task.dueDate + '</span></div>' +
    '<div class="detail-item"><span class="detail-label">交辦人</span><span class="detail-value">' + escapeHtml(task.assigner || '-') + '</span></div>' +
    '<div class="detail-item"><span class="detail-label">類別</span><span class="detail-value">' + escapeHtml(task.category || '-') + '</span></div>' +
    '<div class="detail-item"><span class="detail-label">完成進度</span><span class="detail-value">' + task.progress + '%</span></div>' +
    '</div></div>';

  h += '<div class="detail-section"><h3>&#x1f4dd; 工作內容摘要</h3><p style="font-size:14px;line-height:1.6;white-space:pre-wrap">' + escapeHtml(task.description) + '</p>' +
    (task.notes ? '<p style="font-size:13px;color:var(--text-light);margin-top:8px;padding:8px;background:#fafcfd;border-radius:6px"><strong>附註：</strong>' + escapeHtml(task.notes) + '</p>' : '') + '</div>';

  h += '<div class="detail-section"><h3>&#x1f465; 指定交辦人員</h3><div class="task-assignees" style="margin-top:0">' +
    task.assignees.map(a => '<span class="task-assignee-chip" style="padding:6px 14px;font-size:13px">' + escapeHtml(a.dept) + ' - ' + escapeHtml(a.name) + '<br><span style="font-size:11px;color:var(--text-light)">' + escapeHtml(a.email) + '</span></span>').join('') + '</div></div>';

  // Status update - available to both manager and assigned executor
  if (canEdit || isMyTask) {{
    h += '<div class="detail-section"><h3>&#x2699;&#xfe0f; 更新狀態與進度</h3><div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end">';
    if (canEdit) {{
      h += '<div class="form-group" style="min-width:140px"><label>狀態</label><select id="modalStatus" style="padding:8px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-family:inherit">' +
        Object.entries(STATUS_MAP).map(([k,v]) => '<option value="' + k + '"' + (k===task.status?' selected':'') + '>' + v.label + '</option>').join('') +
        '</select></div>';
    }} else {{
      // Executor can only change to progress or review
      h += '<div class="form-group" style="min-width:140px"><label>狀態</label><select id="modalStatus" style="padding:8px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-family:inherit">' +
        '<option value="pending"' + (task.status==='pending'?' selected':'') + '>待辦中</option>' +
        '<option value="progress"' + (task.status==='progress'?' selected':'') + '>執行中</option>' +
        '<option value="review"' + (task.status==='review'?' selected':'') + '>待審核</option>' +
        '</select></div>';
    }}
    h += '<div class="form-group" style="min-width:120px"><label>完成度 %</label><input type="number" id="modalProgress" min="0" max="100" value="' + task.progress + '" style="padding:8px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-family:inherit"></div>' +
      '<button class="btn btn-primary btn-sm" onclick="updateTaskStatus(\\''+task.id+'\\')">更新</button></div></div>';
  }}

  // Progress log - viewable by all, writable by manager and assigned executor
  h += '<div class="detail-section"><h3>&#x1f4ac; 執行進度紀錄</h3><div class="progress-log">';
  if (task.progressLog && task.progressLog.length > 0) {{
    h += task.progressLog.slice().reverse().map(log => '<div class="log-entry"><div style="display:flex;justify-content:space-between"><span class="log-author">' + escapeHtml(log.author||'系統') + '</span><span class="log-time">' + log.time + '</span></div><div class="log-content">' + escapeHtml(log.content) + '</div></div>').join('');
  }} else {{ h += '<div class="no-data">尚無進度紀錄</div>'; }}

  if (canEdit || isMyTask) {{
    h += '</div><div class="add-progress"><div style="flex:1;display:flex;flex-direction:column;gap:6px">' +
      '<input type="text" id="logAuthor" value="' + escapeHtml(currentUser.name) + '" readonly style="padding:8px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-family:inherit;background:#f0f0f0">' +
      '<textarea id="logContent" placeholder="請輸入最新執行進度..."></textarea></div>' +
      '<button class="btn btn-primary" onclick="addProgressLog(\\''+task.id+'\\')" style="align-self:flex-end">新增紀錄</button></div>';
  }} else {{
    h += '</div>';
  }}
  h += '</div>';

  // Action buttons - only for managers
  if (canEdit) {{
    h += '<div style="display:flex;gap:8px;margin-top:20px;justify-content:flex-end;flex-wrap:wrap">' +
      '<button class="btn btn-info btn-sm" onclick="editTask(\\''+task.id+'\\')">&#x270f;&#xfe0f; 編輯</button>' +
      '<button class="btn btn-warning btn-sm" onclick="duplicateTask(\\''+task.id+'\\')">&#x1f4cb; 複製</button>' +
      '<button class="btn btn-danger btn-sm" onclick="deleteTask(\\''+task.id+'\\')">&#x1f5d1;&#xfe0f; 刪除</button></div>';
  }}

  document.getElementById('modalBody').innerHTML = h;
  document.getElementById('taskModal').classList.add('active');
}}

function closeModal() {{ document.getElementById('taskModal').classList.remove('active'); }}

function updateTaskStatus(taskId) {{
  const task = tasks.find(t => t.id === taskId);
  if (!task) return;
  const ns = document.getElementById('modalStatus').value;
  const np = parseInt(document.getElementById('modalProgress').value) || 0;
  const os = task.status;
  task.status = ns;
  task.progress = Math.min(100, Math.max(0, np));
  if (ns === 'done') task.progress = 100;
  task.updatedAt = new Date().toISOString();
  if (os !== ns) {{
    task.progressLog.push({{ time: new Date().toLocaleString('zh-TW'), author: currentUser.name, content: '狀態更新: ' + STATUS_MAP[os].label + ' → ' + STATUS_MAP[ns].label }});
  }}
  saveTasks(); updateStats(); showToast('狀態已更新');
  showTaskDetail(taskId);
}}

function addProgressLog(taskId) {{
  const task = tasks.find(t => t.id === taskId);
  if (!task) return;
  const content = document.getElementById('logContent').value.trim();
  if (!content) {{ showToast('請輸入進度內容', 'error'); return; }}
  task.progressLog.push({{ time: new Date().toLocaleString('zh-TW'), author: currentUser.name, content }});
  task.updatedAt = new Date().toISOString();
  saveTasks(); showToast('進度紀錄已新增');
  showTaskDetail(taskId);
}}

function editTask(taskId) {{
  if (!canManage()) {{ showToast('您沒有編輯權限', 'error'); return; }}
  const task = tasks.find(t => t.id === taskId);
  if (!task) return;
  closeModal();
  editingTaskId = taskId;
  document.getElementById('taskTitle').value = task.title;
  document.getElementById('taskPriority').value = task.priority;
  document.getElementById('taskStartDate').value = task.startDate;
  document.getElementById('taskDueDate').value = task.dueDate;
  document.getElementById('taskAssigner').value = task.assigner || '';
  document.getElementById('taskCategory').value = task.category || '';
  document.getElementById('taskDescription').value = task.description;
  document.getElementById('taskNotes').value = task.notes || '';
  currentAssignees = [...task.assignees];
  renderAssignees();
  switchView('create');
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('navCreate').classList.add('active');
}}

function duplicateTask(taskId) {{
  const task = tasks.find(t => t.id === taskId);
  if (!task) return;
  const nt = {{ ...JSON.parse(JSON.stringify(task)), id: generateId(), status: 'pending', progress: 0, progressLog: [], createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() }};
  tasks.unshift(nt); saveTasks(); updateStats(); closeModal();
  showToast('交辦事項已複製！新 ID: ' + nt.id);
}}

function deleteTask(taskId) {{
  if (!confirm('確定要刪除此交辦事項嗎？此操作無法復原。')) return;
  tasks = tasks.filter(t => t.id !== taskId);
  saveTasks(); updateStats(); closeModal(); renderTaskList();
  showToast('交辦事項已刪除', 'info');
}}

// ===== DASHBOARD =====
function renderDashboard() {{
  const vt = getVisibleTasks();
  const sc = {{ pending: vt.filter(t=>t.status==='pending').length, progress: vt.filter(t=>t.status==='progress').length, review: vt.filter(t=>t.status==='review').length, done: vt.filter(t=>t.status==='done').length, cancelled: vt.filter(t=>t.status==='cancelled').length }};
  const total = vt.length || 1;
  const sColors = {{ pending:'#ef5350', progress:'#42a5f5', review:'#ffa726', done:'#66bb6a', cancelled:'#90a4ae' }};
  document.getElementById('statusChart').innerHTML = Object.entries(sc).map(([k,v]) => '<div class="chart-bar"><span class="chart-bar-label">' + STATUS_MAP[k].label + '</span><div class="chart-bar-track"><div class="chart-bar-fill" style="width:' + (v/total*100) + '%;background:' + sColors[k] + '">' + v + '</div></div></div>').join('');

  const pc = {{ urgent: vt.filter(t=>t.priority==='urgent').length, high: vt.filter(t=>t.priority==='high').length, medium: vt.filter(t=>t.priority==='medium').length, low: vt.filter(t=>t.priority==='low').length }};
  const pColors = {{ urgent:'#c62828', high:'#e65100', medium:'#1565c0', low:'#2e7d32' }};
  document.getElementById('priorityChart').innerHTML = Object.entries(pc).map(([k,v]) => '<div class="chart-bar"><span class="chart-bar-label">' + PRIORITY_MAP[k].label + '</span><div class="chart-bar-track"><div class="chart-bar-fill" style="width:' + (v/total*100) + '%;background:' + pColors[k] + '">' + v + '</div></div></div>').join('');

  const oi = vt.filter(t => t.status !== 'done' && t.status !== 'cancelled').map(t => ({{ ...t, daysLeft: getDaysLeft(t.dueDate) }})).filter(t => t.daysLeft <= 7).sort((a,b) => a.daysLeft - b.daysLeft);
  document.getElementById('overdueList').innerHTML = oi.length === 0 ? '<div class="no-data">&#x2705; 目前沒有逾期或即將到期的項目</div>' : oi.map(t => '<div class="overdue-item" onclick="showTaskDetail(\\''+t.id+'\\')" style="cursor:pointer"><div class="task-name">' + escapeHtml(t.title) + ' <span class="task-id">' + t.id + '</span></div><div class="overdue-info">' + (t.daysLeft < 0 ? '&#x26a0; 已逾期 ' + Math.abs(t.daysLeft) + ' 天' : '&#x23f0; 剩餘 ' + t.daysLeft + ' 天（' + t.dueDate + '）') + '</div></div>').join('');

  const recent = vt.slice(0, 5);
  document.getElementById('recentTasks').innerHTML = recent.length === 0 ? '<div class="no-data">目前尚無交辦事項，請點選「新增交辦」開始建立。</div>' : recent.map(renderTaskCard).join('');
}}

// ===== USER MANAGEMENT =====
function renderUserTable() {{
  if (!isAdmin()) return;
  const kw = (document.getElementById('userSearchInput')?.value || '').toLowerCase();
  const roleFilter = document.getElementById('userFilterRole')?.value || '';

  let userList = Object.values(users).filter(u => {{
    if (roleFilter && u.role !== roleFilter) return false;
    if (kw) {{
      const s = (u.name + ' ' + u.dept + ' ' + u.email).toLowerCase();
      if (!s.includes(kw)) return false;
    }}
    return true;
  }});

  userList.sort((a,b) => a.dept.localeCompare(b.dept) || a.name.localeCompare(b.name));

  const tbody = document.getElementById('userTableBody');
  tbody.innerHTML = userList.map(u => {{
    const ri = ROLE_MAP[u.role] || ROLE_MAP.executor;
    const key = u.email.trim().toLowerCase();
    return '<tr>' +
      '<td><strong>' + escapeHtml(u.name) + '</strong></td>' +
      '<td>' + escapeHtml(u.dept) + '</td>' +
      '<td style="font-size:12px">' + escapeHtml(u.email) + '</td>' +
      '<td><span class="role-tag ' + ri.class + '">' + ri.label + '</span></td>' +
      '<td>' + (u.active ? '<span style="color:var(--success)">&#x2705; 啟用</span>' : '<span style="color:var(--danger)">&#x26d4; 停用</span>') + '</td>' +
      '<td><div style="display:flex;gap:4px;flex-wrap:wrap">' +
        '<button class="btn btn-info btn-sm" onclick="setUserRole(\\'' + key + '\\', \\'admin\\')">管理員</button>' +
        '<button class="btn btn-primary btn-sm" onclick="setUserRole(\\'' + key + '\\', \\'manager\\')">交辦人</button>' +
        '<button class="btn btn-success btn-sm" onclick="setUserRole(\\'' + key + '\\', \\'executor\\')">執行人</button>' +
        '<button class="btn btn-' + (u.active ? 'danger' : 'warning') + ' btn-sm" onclick="toggleUserActive(\\'' + key + '\\')">' + (u.active ? '停用' : '啟用') + '</button>' +
        '<button class="btn btn-secondary btn-sm" onclick="resetUserPwd(\\'' + key + '\\')">重設密碼</button>' +
      '</div></td></tr>';
  }}).join('');
}}

function setUserRole(email, role) {{
  if (!isAdmin()) return;
  if (users[email]) {{
    users[email].role = role;
    saveUsers();
    renderUserTable();
    showToast(users[email].name + ' 的角色已設為 ' + ROLE_MAP[role].label);
  }}
}}

function toggleUserActive(email) {{
  if (!isAdmin()) return;
  if (users[email]) {{
    users[email].active = !users[email].active;
    saveUsers();
    renderUserTable();
    showToast(users[email].name + ' 帳號已' + (users[email].active ? '啟用' : '停用'));
  }}
}}

function resetUserPwd(email) {{
  if (!isAdmin()) return;
  if (users[email] && confirm('確定要重設 ' + users[email].name + ' 的密碼為 1234？')) {{
    users[email].password = '1234';
    saveUsers();
    showToast(users[email].name + ' 的密碼已重設為 1234');
  }}
}}

// ===== IMPORT/EXPORT =====
function exportData() {{
  const data = {{ tasks, users, exportDate: new Date().toISOString() }};
  const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = '水試所交辦事項_' + new Date().toISOString().split('T')[0] + '.json';
  a.click();
  showToast('資料已匯出');
}}

function importData(e) {{
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(ev) {{
    try {{
      const data = JSON.parse(ev.target.result);
      if (confirm('匯入將覆蓋現有資料，確定繼續？')) {{
        if (Array.isArray(data)) {{
          tasks = data;
        }} else if (data.tasks) {{
          tasks = data.tasks;
          if (data.users) {{ users = data.users; saveUsers(); }}
        }}
        saveTasks(); updateStats(); renderDashboard();
        showToast('資料已匯入，共 ' + tasks.length + ' 筆');
      }}
    }} catch(err) {{ showToast('檔案解析失敗', 'error'); }}
  }};
  reader.readAsText(file);
  e.target.value = '';
}}

// ===== EVENT LISTENERS =====
document.getElementById('taskModal').addEventListener('click', function(e) {{ if (e.target === this) closeModal(); }});
document.getElementById('pwdModal').addEventListener('click', function(e) {{ if (e.target === this) closePwdModal(); }});
document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') {{ closeModal(); closePwdModal(); }} }});

// ===== INIT =====
initUsers();
initLoginDepts();

// Check for existing session
if (currentUser) {{
  const userKey = currentUser.email.trim().toLowerCase();
  if (users[userKey] && users[userKey].active) {{
    enterApp();
  }} else {{
    sessionStorage.removeItem('fri_session');
    currentUser = null;
  }}
}}
</script>
</body>
</html>'''

with open('D:/tmp/Todo008/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done!')
