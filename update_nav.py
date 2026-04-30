#!/usr/bin/env python3
"""更新所有报告的历史导航栏（加上日期下拉选择）"""
import os, re

GHP_DIR = r"C:\Users\admin\github-pages"
REPORTS = sorted([f for f in os.listdir(GHP_DIR) if f.startswith("report_") and f.endswith(".html")])

dates = []
for f in REPORTS:
    d = f.replace("report_", "").replace(".html", "")
    y, m, day = d[:4], d[4:6], d[6:]
    m_int = str(int(m))
    day_int = str(int(day))
    dates.append((d, f"{y}-{m}-{day}", f"{m_int}月{day_int}日", f))

# 生成下拉选项 HTML（最新在前，用降序排列）
options_html = "\n".join(
    f'            <option value="{fname}">{display} {("(今日)" if i == 0 else "")}</option>'
    for i, (d, display, label, fname) in enumerate(sorted(dates, reverse=True))
)

# 下拉 JS
select_js = f"""    <select id="dateSelect" onchange="location=this.value" style="background:#1a1a2e;color:#8b8ba7;border:1px solid #333;border-radius:8px;padding:4px 8px;font-size:13px;cursor:pointer">
        <option value="">-- 选择日期 --</option>
{options_html}
    </select>"""

# 完整导航栏 HTML
nav_style = """<style>
.history-bar { background: #1a1a2e; padding: 10px 20px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; font-size: 13px; color: #8b8ba7; }
.history-bar a { color: #8b8ba7; text-decoration: none; padding: 2px 10px; border-radius: 10px; }
.history-bar a:hover { background: rgba(255,255,255,0.1); color: #fff; }
.history-bar .sep { color: #444; }
.history-bar .select-wrap { display: flex; align-items: center; gap: 8px; }
</style>"""

for d, display, label, fname in dates:
    fpath = os.path.join(GHP_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 找到当前日期label
    current_label = next((l for _, _, l, _ in dates if l == label), "")

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
    <span style="color:#00c853">{label}（今日）</span>
</div>"""

    # 替换现有导航栏或 body 后
    if 'class="history-bar"' in content:
        # 替换整块（从 <div class="history-bar"> 到下一个 </div>）
        content = re.sub(r'<div class="history-bar">.*?</div>\n', nav_html + "\n", content, flags=re.DOTALL)
    else:
        content = content.replace("<body>", "<body>\n" + nav_style + "\n" + nav_html + "\n", 1)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] {fname}")

print("全部完成")
