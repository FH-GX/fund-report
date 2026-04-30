#!/usr/bin/env python3
"""修复所有历史报告的导航栏：删除旧CSS样式 + 插入新导航栏"""
import os, re

GHP_DIR = r"C:\Users\admin\github-pages"
TODAY = "20260430"  # 当前日期（手动指定）
REPORTS = sorted([f for f in os.listdir(GHP_DIR) if f.startswith("report_") and f.endswith(".html")])

# 扫描所有报告，生成日期列表
dates = []
for f in REPORTS:
    d = f.replace("report_", "").replace(".html", "")
    y, m, day = d[:4], d[4:6], d[6:]
    m_int = str(int(m))
    day_int = str(int(day))
    dates.append((d, f"{m_int}月{day_int}日", f))

# 生成下拉选项（最新在前）
options_html = "\n".join(
    f'            <option value="{fname}">{label}{(" (今日)" if i == 0 else "")}</option>'
    for i, (d, label, fname) in enumerate(sorted(dates, reverse=True))
)

# 新导航栏的 style
nav_style = """<style>
.history-bar { background: #1a1a2e; padding: 10px 20px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; font-size: 13px; color: #8b8ba7; }
.history-bar a { color: #8b8ba7; text-decoration: none; padding: 2px 10px; border-radius: 10px; }
.history-bar a:hover { background: rgba(255,255,255,0.1); color: #fff; }
.history-bar .sep { color: #444; }
.history-bar .select-wrap { display: flex; align-items: center; gap: 8px; }
</style>"""

for d, label, fname in dates:
    fpath = os.path.join(GHP_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 删除旧的 history-bar CSS 样式（旧的浅色文字链接样式）
    # 删除从 .history-bar { 到下一个空行或 } 之间的旧样式
    old_style_pattern = r'\.history-bar \{[^}]+\}\n'
    content = re.sub(old_style_pattern, '', content)
    # 清理多余空行
    content = re.sub(r'\n\n\n+', '\n\n', content)

    # 2. 替换或删除旧的导航栏 HTML
    # 旧的导航栏可能在 <div class="history-bar"> 或其他位置
    # 先删掉所有旧的 history-bar div
    content = re.sub(r'<div class="history-bar">.*?</div>\n', '', content, flags=re.DOTALL)

    # 3. 生成新导航栏（不是今日的报告不标记"今日"）
    is_today = (d == TODAY)
    today_label = f'<span style="color:#00c853">{label}{"（今日）" if is_today else ""}</span>'

    nav_html = f"""<div class="history-bar">
    <a href="index.html">🏠 返回首页</a>
    <span class="sep">|</span>
    <div class="select-wrap">
        <label style="color:#666">📅</label>
        <select id="dateSelect" onchange="location=this.value" style="background:#1a1a2e;color:#8b8ba7;border:1px solid #333;border-radius:8px;padding:4px 8px;font-size:13px;cursor:pointer">
            <option value="">-- 选择日期 --</option>
{options_html}
        </select>
    </div>
    <span class="sep">|</span>
    {today_label}
</div>"""

    # 4. 插入到 body 标签后（最新报告的 style + nav 在 body 后）
    content = content.replace("<body>", "<body>\n" + nav_style + "\n" + nav_html + "\n", 1)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] {fname} - {label}")

print("\n全部完成！所有报告导航栏已统一为深色新样式")
