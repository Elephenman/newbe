#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FASTQ按质量/长度/GC含量过滤"""
import os, sys

def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "" or val is None: return default
    try: return type(val)
    except: return default

def filter_fastq(filepath, min_qual=20, min_len=50, gc_min=0.3, gc_max=0.7, output_path=None):
    kept = 0; dropped = 0; reasons = {"quality":0, "length":0, "gc":0}
    current_read = []; line_count = 0
    out = open(output_path or filepath.replace('.fastq','_filtered.fastq').replace('.fq','_filtered.fq'), 'w')
    
    with open(filepath, 'r') as f:
        for line in f:
            current_read.append(line.strip())
            line_count += 1
            if line_count % 4 == 0:
                seq = current_read[1]; qual = current_read[3]; seq_len = len(seq)
                # 计算平均质量
                avg_q = sum(ord(c)-33 for c in qual)/seq_len if seq_len>0 else 0
                # GC含量
                gc = (seq.count('G')+seq.count('C'))/seq_len if seq_len>0 else 0
                
                drop_reason = None
                if avg_q < min_qual: drop_reason = "quality"; reasons["quality"] += 1
                elif seq_len < min_len: drop_reason = "length"; reasons["length"] += 1
                elif gc < gc_min or gc > gc_max: drop_reason = "gc"; reasons["gc"] += 1
                
                if drop_reason is None:
                    for l in current_read: out.write(l + '\n')
                    kept += 1
                else: dropped += 1
                current_read = []
    
    out.close()
    print(f"\n╔══════════════════════════════════════╗")
    print(f"║  FASTQ过滤统计                       ║")
    print(f"║  保留reads: {kept}                   ║")
    print(f"║  丢弃reads: {dropped}                ║")
    print(f"║  质量不足: {reasons['quality']}       ║")
    print(f"║  长度过短: {reasons['length']}        ║")
    print(f"║  GC超标:   {reasons['gc']}           ║")
    print(f"║  输出文件: {out.name}                 ║")
    print(f"╚══════════════════════════════════════╝")

def main():
    print("="*50); print("  🔬 FASTQ过滤器"); print("="*50)
    fp = get_input("输入FASTQ文件路径", "sample.fastq")
    mq = get_input("最小平均质量阈值", 20, int)
    ml = get_input("最小序列长度(bp)", 50, int)
    gc = get_input("GC含量范围(如0.3-0.7)", "0.3-0.7")
    gc_min, gc_max = float(gc.split('-')[0]), float(gc.split('-')[1])
    op = get_input("输出文件路径(留空自动命名)", "")
    filter_fastq(fp, mq, ml, gc_min, gc_max, op or None)

if __name__ == "__main__": main()