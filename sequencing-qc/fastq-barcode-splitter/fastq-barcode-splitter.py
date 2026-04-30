#!/usr/bin/env python3
"""FASTQ按barcode/标签拆分文件"""

# FASTQ按barcode拆分
import gzip
import os

print("=" * 60)
print("  🧬 FASTQ Barcode拆分器")
print("=" * 60)

input_fq = get_input("输入FASTQ文件路径", "sample.fastq.gz")
barcode_file = get_input("barcode列表文件路径", "barcodes.txt")
bc_pos = get_input("barcode位置(start/end)", "start")
bc_len = int(get_input("barcode长度", "6"))
output_dir = get_input("输出目录", "split_output")

os.makedirs(output_dir, exist_ok=True)

barcodes = []
with open(barcode_file, 'r') as f:
    for line in f:
        bc = line.strip()
        if bc:
            barcodes.append(bc)
print(f"✅ 加载 {len(barcodes)} 个barcodes")

bc_counts = {bc: 0 for bc in barcodes}
unmatched = 0
total = 0

out_files = {}
for bc in barcodes:
    path = os.path.join(output_dir, f"{bc}.fastq")
    out_files[bc] = open(path, 'w')
unknown_path = os.path.join(output_dir, "unmatched.fastq")
unknown_file = open(unknown_path, 'w')

is_gz = input_fq.endswith('.gz')
opener = gzip.open if is_gz else open
mode = 'rt' if is_gz else 'r'

with opener(input_fq, mode) as f:
    while True:
        header = f.readline()
        if not header:
            break
        seq = f.readline()
        plus = f.readline()
        qual = f.readline()
        total += 1
        
        extract = seq.strip()[:bc_len] if bc_pos == "start" else seq.strip()[-bc_len:]
        
        if extract in bc_counts:
            bc_counts[extract] += 1
            out_files[extract].write(header + seq + plus + qual)
        else:
            unmatched += 1
            unknown_file.write(header + seq + plus + qual)

for bc in barcodes:
    out_files[bc].close()
unknown_file.close()

print(f"\n✅ 拆分完成: {total} reads处理")
print(f"  匹配: {sum(bc_counts.values())} ({sum(bc_counts.values())/total*100:.1f}%)")
print(f"  未匹配: {unmatched} ({unmatched/total*100:.1f}%)")
for bc, cnt in bc_counts.items():
    print(f"  {bc}: {cnt} reads")
