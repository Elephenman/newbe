#!/usr/bin/env python3
"""项目时间线甘特图+里程碑标注
读取任务时间线数据，生成甘特图和里程碑标记
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


def parse_timeline(filepath):
    """解析时间线CSV文件: Task,Start,End,Milestone,Category"""
    tasks = []
    with open(filepath, 'r', encoding='utf-8') as f:
        header = f.readline()  # skip header
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(',') if ',' in line else line.split('\t')
            if len(parts) >= 4:
                task = parts[0].strip()
                start = parts[1].strip()
                end = parts[2].strip()
                is_milestone = len(parts) > 3 and parts[3].strip().lower() in ('yes', 'y', '1', 'true')
                category = parts[4].strip() if len(parts) > 4 else "default"
                tasks.append({
                    'task': task,
                    'start': start,
                    'end': end,
                    'milestone': is_milestone,
                    'category': category
                })
    return tasks


def main():
    print("=" * 60)
    print("  项目时间线甘特图+里程碑标注")
    print("=" * 60)
    print()

    input_file = get_input("时间线CSV路径(Task,Start,End,Milestone,Category)", "timeline.csv")
    output_file = get_input("输出图片路径", "gantt_chart.png")
    title = get_input("图表标题", "Project Timeline")

    print()
    print(f"输入:    {input_file}")
    print(f"输出:    {output_file}")
    print(f"标题:    {title}")
    print()

    if not os.path.exists(input_file):
        # Create a template file for the user
        print(f"[WARN] 文件不存在: {input_file}")
        print("创建模板文件...")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("Task,Start,End,Milestone,Category\n")
            f.write("Project Planning,2024-01-01,2024-01-15,no,Planning\n")
            f.write("Data Collection,2024-01-10,2024-02-15,no,Data\n")
            f.write("Data Milestone,2024-02-15,2024-02-15,yes,Data\n")
            f.write("Analysis,2024-02-01,2024-03-15,no,Analysis\n")
            f.write("Writing,2024-03-01,2024-04-01,no,Writing\n")
            f.write("Submission,2024-04-01,2024-04-01,yes,Writing\n")
        print(f"模板文件创建: {input_file}")

    tasks = parse_timeline(input_file)
    if not tasks:
        print("[ERROR] 未解析到有效任务")
        sys.exit(1)

    print(f"[Processing] 找到 {len(tasks)} 个任务")

    # Parse dates
    date_format = "%Y-%m-%d"
    for t in tasks:
        try:
            t['start_dt'] = datetime.strptime(t['start'], date_format)
            t['end_dt'] = datetime.strptime(t['end'], date_format)
        except ValueError:
            print(f"[ERROR] 日期格式错误: {t['task']} - 请使用YYYY-MM-DD")
            sys.exit(1)

    # Plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.patches import FancyBboxPatch
        import numpy as np

        # Category colors
        categories = list(set(t['category'] for t in tasks))
        color_map = {}
        cmap = plt.cm.Set2
        for i, cat in enumerate(categories):
            color_map[cat] = cmap(i / max(len(categories), 1))

        fig, ax = plt.subplots(figsize=(14, max(6, len(tasks) * 0.5)))

        # Sort by start date
        tasks_sorted = sorted(tasks, key=lambda x: x['start_dt'])

        for i, t in enumerate(tasks_sorted):
            color = color_map[t['category']]
            duration = (t['end_dt'] - t['start_dt']).days

            if t['milestone']:
                # Draw diamond for milestone
                mid_date = t['start_dt']
                ax.plot(mid_date, i, marker='D', color='red', markersize=10, zorder=5)
                ax.annotate(t['task'], (mid_date, i), xytext=(5, 5),
                           textcoords='offset points', fontsize=8, fontweight='bold')
            else:
                # Draw bar
                ax.barh(i, duration, left=t['start_dt'], height=0.6,
                       color=color, alpha=0.8, edgecolor='gray', linewidth=0.5)
                # Task label
                if duration > 0:
                    ax.text(t['start_dt'], i, ' ' + t['task'], va='center', ha='left', fontsize=8)
                else:
                    ax.text(t['start_dt'] + mdates.DayLocator().tick_values(t['start_dt'], t['end_dt'])[0] if False else t['start_dt'],
                           i, t['task'], va='center', ha='left', fontsize=8)

        ax.set_yticks(range(len(tasks_sorted)))
        ax.set_yticklabels([t['task'] for t in tasks_sorted])
        ax.invert_yaxis()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)
        ax.set_title(title)
        ax.grid(axis='x', alpha=0.3)

        # Legend for categories
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color_map[cat], label=cat) for cat in categories]
        ax.legend(handles=legend_elements, loc='lower right')

        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"[Processing] 甘特图: {output_file}")

    except ImportError:
        # Fallback: text output
        txt_output = output_file.rsplit('.', 1)[0] + '.txt'
        with open(txt_output, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n{'='*60}\n\n")
            for t in tasks_sorted:
                ms = " [MILESTONE]" if t['milestone'] else ""
                f.write(f"{t['task']}: {t['start']} -> {t['end']}{ms} ({t['category']})\n")
        print(f"[WARN] matplotlib未安装，文本输出: {txt_output}")

    n_milestones = sum(1 for t in tasks if t['milestone'])
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  任务数:      {len(tasks)}")
    print(f"  里程碑:      {n_milestones}")
    print(f"  分类:        {len(categories)}")
    print(f"  输出:        {output_file}")
    print("=" * 60)
    print()
    print("[Done] timeline_gantt_plotter completed successfully!")


if __name__ == "__main__":
    main()
