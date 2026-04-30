#!/usr/bin/env python3
"""科研日记模板生成+Markdown格式
根据输入的实验信息和日期范围，生成结构化的科研日记Markdown文件
"""

import os
import sys
from datetime import datetime, timedelta


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def main():
    print("=" * 60)
    print("  科研日记模板生成+Markdown格式")
    print("=" * 60)
    print()

    project_name = get_input("项目名称", "MyProject")
    start_date = get_input("起始日期(YYYY-MM-DD)", datetime.now().strftime("%Y-%m-%d"))
    num_days = get_input("天数", "7", int)
    output_file = get_input("输出Markdown路径", "research_diary.md")
    sections = get_input("日记模块(逗号分隔: aim/method/result/next/issue)", "aim,method,result,next,issue")

    print()
    print(f"项目:      {project_name}")
    print(f"起始日期:  {start_date}")
    print(f"天数:      {num_days}")
    print(f"输出:      {output_file}")
    print()

    section_labels = {
        "aim": "Aim / 目标",
        "method": "Method / 方法",
        "result": "Result / 结果",
        "next": "Next steps / 下一步",
        "issue": "Issues / 问题与思考",
    }

    section_list = [s.strip() for s in sections.split(",") if s.strip()]
    valid_sections = [s for s in section_list if s in section_labels]

    if not valid_sections:
        print("[WARN] 无有效模块，使用默认模块")
        valid_sections = ["aim", "method", "result", "next", "issue"]

    try:
        dt = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        print(f"[ERROR] 日期格式错误: {start_date}, 请使用YYYY-MM-DD")
        sys.exit(1)

    # Generate diary
    lines = []
    lines.append(f"# Research Diary: {project_name}")
    lines.append("")
    lines.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Date range: {start_date} ~ {(dt + timedelta(days=num_days-1)).strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i in range(num_days):
        current = dt + timedelta(days=i)
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday = weekday_names[current.weekday()]

        lines.append(f"## {current.strftime('%Y-%m-%d')} ({weekday})")
        lines.append("")

        for sec in valid_sections:
            label = section_labels.get(sec, sec)
            lines.append(f"### {label}")
            lines.append("")
            lines.append(f"<!-- Enter {sec} notes here -->")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Table of contents
    toc_lines = [
        "# Table of Contents",
        "",
    ]
    for i in range(num_days):
        current = dt + timedelta(days=i)
        weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekday = weekday_names[current.weekday()]
        toc_lines.append(f"- [{current.strftime('%Y-%m-%d')} ({weekday})](#{current.strftime('%Y-%m-%d').replace('-', '')}-{weekday.lower()})")
    toc_lines.append("")

    # Write output
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(toc_lines))
            f.write("\n".join(lines))
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  项目名称:      {project_name}")
    print(f"  日记天数:      {num_days}")
    print(f"  模块:          {', '.join(valid_sections)}")
    print(f"  输出文件:      {output_file}")
    print("=" * 60)
    print()
    print("[Done] research_diary_generator completed successfully!")


if __name__ == "__main__":
    main()
