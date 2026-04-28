#!/usr/bin/env python3
"""FASTQ read名称/ID提取与去重统计"""

# FASTQ read名称提取与去重统计
import gzip
from collections import Counter

def is_gzip(path):
    return path.endswith('.gz')

print("=" * 60)
print("  🧬 FASTQ Read名称提取与去重统计")
print("=" * 60)

input_file = get_input("输入FASTQ文件路径", "sample.fastq.gz")
output_file = get_input("输出文件路径", "read_names.txt")
check_dup = get_input("是否检查重复read名(yes/no)", "yes")
report = get_input("是否输出统计摘要(yes/no)", "yes")

read_names = []
total_reads = 0

opener = gzip.open if is_gzip(input_file) else open
mode = 'rt' if is_gzip(input_file) else 'r'

try:
    with opener(input_file, mode) as f:
        for line in f:
            if total_reads % 4 == 0:
                name = line.strip().split()[0]
                read_names.append(name)
            total_reads += 1
except FileNotFoundError:
    print(f"❌ 文件不存在: {input_file}")
    exit(1)

print(f"\n✅ 读取完成: {len(read_names)} reads")

if check_dup == "yes":
    counter = Counter(read_names)
    unique = len(counter)
    duplicates = sum(1 for n, c in counter.items() if c > 1)
    dup_count = sum(c - 1 for n, c in counter.items() if c > 1)
    print(f"  唯一read名: {unique}")
    print(f"  重复read名数: {duplicates}")
    print(f"  重复总数: {dup_count}")
    print(f"  重复率: {dup_count/len(read_names)*100:.2f}%")

with open(output_file, 'w') as f:
    for name in read_names:
        f.write(name + '\n')
print(f"\n📄 Read名已保存到: {output_file}")

if report == "yes":
    report_file = output_file.replace('.txt', '_report.txt')
    with open(report_file, 'w') as f:
        f.write(f"FASTQ Read名称统计报告\n")
        f.write(f"输入文件: {input_file}\n")
        f.write(f"总read数: {len(read_names)}\n")
        if check_dup == "yes":
            f.write(f"唯一read名: {unique}\n")
            f.write(f"重复率: {dup_count/len(read_names)*100:.2f}%\n")
    print(f"📊 统计报告已保存到: {report_file}")
