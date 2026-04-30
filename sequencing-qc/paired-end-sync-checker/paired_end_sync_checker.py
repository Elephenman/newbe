#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paired-end FASTQ配对一致性检查"""
import os, sys
from collections import defaultdict

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def check_paired_end_sync(r1_path, r2_path, output_file=None):
    """检查paired-end FASTQ文件的read配对一致性"""
    # 读取R1 read名称
    print("Reading R1 file...")
    r1_reads = {}
    r1_count = 0
    with open(r1_path, 'r') as f:
        while True:
            header = f.readline()
            if not header:
                break
            seq = f.readline()
            plus = f.readline()
            qual = f.readline()

            # 提取read名称(去/@和 /1 /2后缀和空格后内容)
            read_name = header.strip()[1:].split()[0]
            read_name = read_name.rstrip('/1').rstrip('/2')
            r1_reads[read_name] = r1_count
            r1_count += 1

    # 读取R2 read名称
    print("Reading R2 file...")
    r2_reads = {}
    r2_count = 0
    with open(r2_path, 'r') as f:
        while True:
            header = f.readline()
            if not header:
                break
            seq = f.readline()
            plus = f.readline()
            qual = f.readline()

            read_name = header.strip()[1:].split()[0]
            read_name = read_name.rstrip('/1').rstrip('/2')
            r2_reads[read_name] = r2_count
            r2_count += 1

    # 分析
    r1_names = set(r1_reads.keys())
    r2_names = set(r2_reads.keys())

    only_in_r1 = r1_names - r2_names
    only_in_r2 = r2_names - r1_names
    common = r1_names & r2_names

    # 检查顺序一致性
    order_mismatches = 0
    for name in common:
        if r1_reads[name] != r2_reads[name]:
            order_mismatches += 1

    # 输出
    out_path = output_file or "paired_end_sync_report.txt"
    with open(out_path, 'w') as out:
        out.write("=== Paired-End Sync Check Report ===\n\n")
        out.write(f"R1 file: {r1_path}\n")
        out.write(f"R2 file: {r2_path}\n")
        out.write(f"R1 reads: {r1_count}\n")
        out.write(f"R2 reads: {r2_count}\n")
        out.write(f"Common pairs: {len(common)}\n")
        out.write(f"Only in R1: {len(only_in_r1)}\n")
        out.write(f"Only in R2: {len(only_in_r2)}\n")
        out.write(f"Order mismatches: {order_mismatches}\n")
        out.write(f"\nSync status: {'PASS' if not only_in_r1 and not only_in_r2 and order_mismatches == 0 else 'FAIL'}\n")

        if only_in_r1:
            out.write(f"\n# Reads only in R1 (first 100)\n")
            for name in sorted(only_in_r1)[:100]:
                out.write(f"  {name}\n")

        if only_in_r2:
            out.write(f"\n# Reads only in R2 (first 100)\n")
            for name in sorted(only_in_r2)[:100]:
                out.write(f"  {name}\n")

    print(f"Paired-end sync check complete")
    print(f"  R1 reads: {r1_count}")
    print(f"  R2 reads: {r2_count}")
    print(f"  Common pairs: {len(common)}")
    print(f"  Only in R1: {len(only_in_r1)}")
    print(f"  Only in R2: {len(only_in_r2)}")
    print(f"  Order mismatches: {order_mismatches}")
    sync_ok = not only_in_r1 and not only_in_r2 and order_mismatches == 0
    print(f"  Status: {'PASS' if sync_ok else 'FAIL'}")
    print(f"  Report: {out_path}")

def main():
    print("=" * 60)
    print("  paired-end FASTQ配对一致性检查")
    print("=" * 60)
    r1_path = get_input("R1 FASTQ文件路径", "R1.fastq")
    r2_path = get_input("R2 FASTQ文件路径", "R2.fastq")
    output = get_input("输出报告路径", "")
    check_paired_end_sync(r1_path, r2_path, output or None)

if __name__ == "__main__":
    main()
