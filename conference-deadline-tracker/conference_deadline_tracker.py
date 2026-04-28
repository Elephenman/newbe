#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  conference-deadline-tracker
  会议截稿日期追踪工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def track_deadlines(output="conference_deadlines.txt"):
    """追踪学术会议截稿日期"""
    from datetime import datetime, timedelta
    
    conferences = [
        {"name": "ISMB/ECCB", "abstract_deadline": "2026-02-15", "paper_deadline": "2026-03-01", "venue": "Lyon, France"},
        {"name": "RECOMB", "abstract_deadline": "2026-01-20", "paper_deadline": "2026-02-01", "venue": "Barcelona, Spain"},
        {"name": "NeurIPS", "abstract_deadline": "2026-05-01", "paper_deadline": "2026-05-15", "venue": "Vancouver, Canada"},
        {"name": "ICML", "abstract_deadline": "2026-01-15", "paper_deadline": "2026-02-01", "venue": "Baltimore, USA"},
        {"name": "Genome Informatics", "abstract_deadline": "2026-06-01", "paper_deadline": "2026-06-15", "venue": "Wellcome Genome Campus"},
        {"name": "AACR Annual Meeting", "abstract_deadline": "2026-01-10", "paper_deadline": "2026-01-10", "venue": "Chicago, USA"},
    ]
    
    today = datetime.now()
    
    with open(output, 'w') as f:
        f.write("Conference Deadline Tracker\n")
        f.write("=" * 80 + "\n")
        f.write(f"Updated: {today.strftime('%Y-%m-%d')}\n\n")
        f.write("Conference\tAbstract Deadline\tPaper Deadline\tVenue\n")
        for conf in conferences:
            ab_date = datetime.strptime(conf["abstract_deadline"], "%Y-%m-%d")
            days_left = (ab_date - today).days
            days_str = f"({days_left} days)" if days_left > 0 else "(PASSED)"
            f.write(f"{conf['name']}\t{conf['abstract_deadline']} {days_str}\t{conf['paper_deadline']}\t{conf['venue']}\n")
    
    return conferences

def main():
    print("\n" + "=" * 60)
    print("  会议截稿日期追踪工具")
    print("=" * 60)
    
    output = get_input("\n输出文件", "conference_deadlines.txt", str)
    
    conferences = track_deadlines(output)
    
    print(f"\n追踪 {len(conferences)} 个会议截稿日期")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
