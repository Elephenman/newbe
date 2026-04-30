#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析流程日志解析+耗时统计"""
import os, sys, re
from collections import defaultdict
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def parse_log(filepath, make_timeline=True, detect_failures=True):
    steps = []; failures = []
    
    # 检测日志类型
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    log_type = "generic"
    if "nextflow" in content.lower() or "nf" in filepath.lower(): log_type = "nextflow"
    elif "snakemake" in content.lower() or "smk" in filepath.lower(): log_type = "snakemake"
    
    # 解析时间戳
    time_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2})')
    times = time_pattern.findall(content)
    
    # 解析步骤(简化)
    step_pattern = re.compile(r'(?:Running|Executed|Completed|Step|Process|Rule|task)[:\s]+(\w+)', re.IGNORECASE)
    step_matches = step_pattern.findall(content)
    
    # 解析耗时
    duration_pattern = re.compile(r'(\w+)[\s:]+(?:took|elapsed|duration|time)[\s:]+(\d+[hms]?)', re.IGNORECASE)
    durations = duration_pattern.findall(content)
    
    # 检测失败
    if detect_failures:
        fail_pattern = re.compile(r'(?:Error|FAIL|fail|failed|exception|crash|abort|killed)[:\s]+(.*?)(?:\n|$)', re.IGNORECASE)
        for m in fail_pattern.finditer(content):
            failures.append(m.group(1).strip()[:100])
    
    # 构建步骤表
    for name in step_matches:
        duration = "unknown"
        for d_name, d_time in durations:
            if d_name.lower() == name.lower(): duration = d_time
        steps.append({"name": name, "duration": duration})
    
    # 输出
    print(f"\n{'='*60}")
    print(f"  流程日志解析报告")
    print(f"{'='*60}")
    print(f"  文件: {filepath}")
    print(f"  类型: {log_type}")
    print(f"  时间戳数: {len(times)}")
    print(f"  步骤数: {len(steps)}")
    print(f"  失败数: {len(failures)}")
    
    if steps:
        print(f"\n  【步骤耗时】")
        for s in steps: print(f"    {s['name']}: {s['duration']}")
    
    if failures:
        print(f"\n  【失败步骤 ❌】")
        for f in failures: print(f"    {f}")
        print(f"\n  建议: 检查失败步骤的日志细节")
    
    # 保存
    with open("pipeline_steps.csv", 'w') as out:
        out.write("step,duration\n")
        for s in steps: out.write(f"{s['name']},{s['duration']}\n")
    
    # 时间线图
    if make_timeline and steps:
        try:
            import matplotlib; matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 4))
            names = [s['name'][:15] for s in steps]
            # 简化：用索引代替实际时间
            plt.barh(range(len(steps)), range(1, len(steps)+1), color='#2196F3')
            plt.yticks(range(len(steps)), names)
            plt.xlabel('步骤顺序'); plt.title('流程时间线')
            plt.tight_layout()
            plt.savefig("pipeline_timeline.png", dpi=300); plt.close()
            print("  时间线图: pipeline_timeline.png")
        except: pass
    
    print(f"  步骤CSV: pipeline_steps.csv")

def main():
    print("="*50); print("  流程日志解析"); print("="*50)
    fp = get_input("日志文件路径", "pipeline.log")
    mt = get_input("出时间线图(yes/no)", "yes")
    df = get_input("检测失败步骤(yes/no)", "yes")
    parse_log(fp, mt.lower() in ('yes','y'), df.lower() in ('yes','y'))

if __name__ == "__main__": main()