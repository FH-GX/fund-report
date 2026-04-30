#!/usr/bin/env python3
"""彻底清理所有报告：删除残缺导航栏 + 正文重复日期"""
import os, re

GHP_DIR = r"C:\Users\admin\github-pages"
TODAY = "20260430"

def clean_report(fname, report_date):
    fpath = os.path.join(GHP_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1. 删除正文里所有分散的日期碎片（</div>后面的残缺导航片段）
    # 这些是 <span class="sep">|</span> <span style="color:#00c853">X月X日...</span> </div> 的模式
    content = re.sub(r'\n    <span class="sep">\|</span>\n    <span style="color:#00c853">[^<]+</span>\n</div>', '', content)
    # 清理可能遗留的空行
    content = re.sub(r'\n\n\n+', '\n\n', content)

    # 2. 替换 body 后的整个导航区域为干净版本
    # 先找到 body 标签位置
    body_match = re.search(r'<body>\n?', content)
    if body_match:
        body_end = body_match.end()

        # 提取 </head> 到 <body> 之间的内容（应该为空或只有空白）
        head_end = content.rfind('</head>', 0, body_match.start())
        between = content[head_end+7:body_match.start()]
        # 清理中间可能残留的空 style
        between = re.sub(r'<style>\s*</style>', '', between)
        between = between.strip()
        if between:
            between = '\n' + between

        # 新的干净导航栏
        dates_map = {
            "20260426": ("4月26日", "report_20260426.html"),
            "20260427": ("4月27日", "report_20260427.html"),
            "20260428": ("4月28日", "report_20260428.html"),
            "20260429": ("4月29日", "report_20260429.html"),
            "20260430": ("4月30日", "report_20260430.html"),
        }
        sorted_dates = sorted(dates_map.items(), key=lambda x: x[0], reverse=True)
        options = []
        for i, (d, (label, fname_opt)) in enumerate(sorted_dates):
            is_today = (d == TODAY)
            options.append(f'            <option value="{fname_opt}">{label}{" (今日)" if is_today else ""}</option>')
        options_html = "\n".join(options)

        # 判断当前报告是否"今日"
        is_today_report = (report_date == TODAY)
        date_label = dates_map.get(report_date, ("?", ""))[0]
        today_mark = f'（今日）' if is_today_report else ''

        new_nav = f"""<style>
.history-bar {{ background: #1a1a2e; padding: 10px 20px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; font-size: 13px; color: #8b8ba7; }}
.history-bar a {{ color: #8b8ba7; text-decoration: none; padding: 2px 10px; border-radius: 10px; }}
.history-bar a:hover {{ background: rgba(255,255,255,0.1); color: #fff; }}
.history-bar .sep {{ color: #444; }}
.history-bar .select-wrap {{ display: flex; align-items: center; gap: 8px; }}
</style>
<div class="history-bar">
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
    <span style="color:#00c853">{date_label}{today_mark}</span>
</div>
"""
        # 替换从 <body> 到第一个 <div class="container"> 之间的所有内容
        container_pos = content.find('<div class="container">', body_end)
        if container_pos > 0:
            content = content[:body_match.start()] + '<body>' + between + '\n' + new_nav + content[container_pos:]

    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

# 处理所有报告
reports = [
    ("report_20260426.html", "20260426"),
    ("report_20260427.html", "20260427"),
    ("report_20260428.html", "20260428"),
    ("report_20260429.html", "20260429"),
    ("report_20260430.html", "20260430"),
]

for fname, rdate in reports:
    changed = clean_report(fname, rdate)
    print(f"[{'OK' if changed else 'SKIP'}] {fname}")

print("\n完成！所有报告导航栏已统一")
