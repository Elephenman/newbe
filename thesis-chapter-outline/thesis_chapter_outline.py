#!/usr/bin/env python3
"""学位论文章节大纲生成+进度追踪
根据论文类型生成标准章节结构，支持进度追踪
"""

import os
import sys
from datetime import datetime


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


# Standard chapter templates
THESIS_TEMPLATES = {
    "master": [
        ("第1章 绪论", ["1.1 研究背景与意义", "1.2 国内外研究现状", "1.3 研究内容与方法", "1.4 论文结构安排"]),
        ("第2章 理论基础", ["2.1 相关理论", "2.2 关键技术", "2.3 本章小结"]),
        ("第3章 方法与实现", ["3.1 系统架构设计", "3.2 核心算法", "3.3 实现细节", "3.4 本章小结"]),
        ("第4章 实验与分析", ["4.1 实验环境", "4.2 实验设计", "4.3 结果分析", "4.4 本章小结"]),
        ("第5章 总结与展望", ["5.1 工作总结", "5.2 不足与展望"]),
    ],
    "phd": [
        ("第1章 绪论", ["1.1 研究背景与意义", "1.2 国内外研究现状", "1.3 研究目标与内容", "1.4 研究方法与技术路线", "1.5 论文创新点", "1.6 论文结构安排"]),
        ("第2章 理论基础与文献综述", ["2.1 相关理论基础", "2.2 关键技术综述", "2.3 现有方法分析", "2.4 本章小结"]),
        ("第3章 [研究内容一]", ["3.1 问题定义", "3.2 方法设计", "3.3 实验验证", "3.4 结果分析", "3.5 本章小结"]),
        ("第4章 [研究内容二]", ["4.1 问题定义", "4.2 方法设计", "4.3 实验验证", "4.4 结果分析", "4.5 本章小结"]),
        ("第5章 [研究内容三]", ["5.1 问题定义", "5.2 方法设计", "5.3 实验验证", "5.4 结果分析", "5.5 本章小结"]),
        ("第6章 总结与展望", ["6.1 论文工作总结", "6.2 主要创新点", "6.3 不足与未来展望"]),
    ],
    "bioinfo": [
        ("第1章 绪论", ["1.1 研究背景", "1.2 生物信息学问题", "1.3 研究目标", "1.4 论文结构"]),
        ("第2章 数据与方法", ["2.1 数据来源与预处理", "2.2 分析流程", "2.3 统计方法", "2.4 生物信息学工具"]),
        ("第3章 [分析一]", ["3.1 数据描述", "3.2 分析方法", "3.3 结果", "3.4 讨论"]),
        ("第4章 [分析二]", ["4.1 数据描述", "4.2 分析方法", "4.3 结果", "4.4 讨论"]),
        ("第5章 整合分析", ["5.1 多组学整合", "5.2 生物学解释", "5.3 验证"]),
        ("第6章 总结与展望", ["6.1 主要发现", "6.2 生物学意义", "6.3 局限性", "6.4 未来方向"]),
    ],
}


def main():
    print("=" * 60)
    print("  学位论文章节大纲生成+进度追踪")
    print("=" * 60)
    print()

    thesis_type = get_input("论文类型(master/phd/bioinfo)", "master")
    title = get_input("论文标题", "My Thesis")
    author = get_input("作者", "Author")
    output_file = get_input("输出Markdown路径", "thesis_outline.md")

    print()
    print(f"类型:   {thesis_type}")
    print(f"标题:   {title}")
    print(f"输出:   {output_file}")
    print()

    chapters = THESIS_TEMPLATES.get(thesis_type, THESIS_TEMPLATES["master"])

    # Generate outline
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- 作者: {author}")
    lines.append(f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 目录")
    lines.append("")

    for chapter, sections in chapters:
        lines.append(f"- [{chapter}](#{chapter.replace(' ', '-')})")
        for sec in sections:
            lines.append(f"  - [{sec}](#{sec.replace(' ', '-')})")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Progress tracking table
    lines.append("## 进度追踪")
    lines.append("")
    lines.append("| 章节 | 状态 | 完成日期 | 备注 |")
    lines.append("|------|------|----------|------|")
    for chapter, sections in chapters:
        lines.append(f"| {chapter} | 未开始 | | |")
        for sec in sections:
            lines.append(f"| {sec} | 未开始 | | |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed outline
    for chapter, sections in chapters:
        lines.append(f"## {chapter}")
        lines.append("")
        for sec in sections:
            lines.append(f"### {sec}")
            lines.append("")
            lines.append("<!-- 在此添加内容要点 -->")
            lines.append("")

        lines.append("### 写作检查清单")
        lines.append("")
        checklist_items = [
            "逻辑连贯性",
            "图表引用完整",
            "参考文献完整",
            "格式规范",
            "语言润色"
        ]
        for item in checklist_items:
            lines.append(f"- [ ] {item}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Write output
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    total_sections = sum(len(s) for _, s in chapters)
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  论文类型:      {thesis_type}")
    print(f"  章节数:        {len(chapters)}")
    print(f"  小节数:        {total_sections}")
    print(f"  输出文件:      {output_file}")
    print("=" * 60)
    print()
    print("[Done] thesis_chapter_outline completed successfully!")


if __name__ == "__main__":
    main()
