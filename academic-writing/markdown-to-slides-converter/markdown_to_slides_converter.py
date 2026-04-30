#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown到reveal.js幻灯片转换"""
import os, sys, re

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

REVEAL_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/theme/{theme}.css">
  <style>
    .reveal h1 {{ font-size: 1.8em; }}
    .reveal h2 {{ font-size: 1.4em; }}
    .reveal section {{ text-align: left; }}
    .reveal img {{ max-height: 500px; }}
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
{slides}
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js"></script>
  <script>
    Reveal.initialize({{
      hash: true,
      slideNumber: true,
      transition: '{transition}',
      width: "90%",
      margin: 0.04
    }});
  </script>
</body>
</html>
"""

def markdown_to_slides(md_path, output_file=None, theme="simple", transition="slide", title=None):
    """将Markdown文件转换为reveal.js HTML幻灯片"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 用 --- 或 <hr> 分隔幻灯片
    slide_separator = re.compile(r'\n---\n|\n<hr>\s*\n|\n\*\*\*\n')
    raw_slides = slide_separator.split(content)

    slides_html = []
    for slide in raw_slides:
        slide = slide.strip()
        if not slide:
            continue

        # 处理Markdown内容
        html_lines = []
        for line in slide.split('\n'):
            # H1 -> section header
            if line.startswith('# '):
                html_lines.append(f'<h2>{line[2:].strip()}</h2>')
            elif line.startswith('## '):
                html_lines.append(f'<h3>{line[3:].strip()}</h3>')
            elif line.startswith('### '):
                html_lines.append(f'<h4>{line[4:].strip()}</h4>')
            # 列表
            elif line.startswith('- ') or line.startswith('* '):
                if not any(l.strip().startswith('<ul>') for l in html_lines[-3:] if html_lines):
                    html_lines.append('<ul>')
                html_lines.append(f'<li>{line[2:].strip()}</li>')
            # 图片
            elif re.match(r'!\[', line):
                img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
                if img_match:
                    alt, src = img_match.group(1), img_match.group(2)
                    html_lines.append(f'<img src="{src}" alt="{alt}">')
            # 普通段落
            elif line.strip():
                # 粗体
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                # 斜体
                line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
                # 代码
                line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
                html_lines.append(f'<p>{line}</p>')

        # 关闭未关闭的ul
        if any('<li>' in l for l in html_lines) and not any('</ul>' in l for l in html_lines):
            html_lines.append('</ul>')

        slide_html = '\n'.join(html_lines)
        slides_html.append(f'<section>\n{slide_html}\n</section>')

    if not slides_html:
        print("[ERROR] No slide content found in Markdown file")
        return

    # 生成HTML
    slide_title = title or os.path.splitext(os.path.basename(md_path))[0]
    html = REVEAL_TEMPLATE.format(
        title=slide_title,
        theme=theme,
        transition=transition,
        slides='\n'.join(slides_html)
    )

    out_path = output_file or os.path.splitext(md_path)[0] + "_slides.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Markdown to slides conversion complete")
    print(f"  Input: {md_path}")
    print(f"  Slides: {len(slides_html)}")
    print(f"  Theme: {theme}")
    print(f"  Transition: {transition}")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  Markdown到reveal.js幻灯片转换")
    print("=" * 60)
    md_path = get_input("Markdown文件路径", "slides.md")
    output = get_input("输出HTML路径", "")
    theme = get_input("主题(simple/white/black/league/sky/serif)", "simple")
    transition = get_input("转场效果(slide/fade/convex/zoom)", "slide")
    title = get_input("幻灯片标题", "")
    markdown_to_slides(md_path, output or None, theme, transition, title or None)

if __name__ == "__main__":
    main()
