#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FASTQ转FASTA + 可选去冗余"""
import os, sys

def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "" or val is None: return default
    try: return type(val)
    except: return default

def fastq_to_fasta(filepath, deduplicate=True, output_path=None):
    sequences = {}; current_read = []; line_count = 0
    out_path = output_path or filepath.replace('.fastq','.fasta').replace('.fq','.fasta')
    
    with open(filepath, 'r') as f, open(out_path, 'w') as out:
        for line in f:
            current_read.append(line.strip())
            line_count += 1
            if line_count % 4 == 0:
                header = current_read[0][1:]  # 去掉@
                seq = current_read[1]
                if deduplicate:
                    if seq not in sequences:
                        sequences[seq] = header
                        out.write(f">{header}\n{seq}\n")
                else:
                    out.write(f">{header}\n{seq}\n")
                current_read = []
    
    unique = len(sequences) if deduplicate else line_count // 4
    print(f"✅ 转换完成: {out_path}")
    print(f"   序列数: {unique}")
    if deduplicate: print(f"   去冗余保留: {unique} (原始: {line_count//4})")

def main():
    print("="*50); print("  🔄 FASTQ→FASTA转换器"); print("="*50)
    fp = get_input("输入FASTQ文件路径", "sample.fastq")
    dedup = get_input("是否去冗余(yes/no)", "yes")
    op = get_input("输出FASTA路径(留空自动)", "")
    fastq_to_fasta(fp, dedup.lower() in ('yes','y'), op or None)

if __name__ == "__main__": main()