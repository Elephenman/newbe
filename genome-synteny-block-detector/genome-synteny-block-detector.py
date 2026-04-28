#!/usr/bin/env python3
"""基因组同线性区块检测"""

# 基因组同线性区块检测
print("=" * 60)
print("  🧪 基因组同线性区块检测器")
print("=" * 60)

input_file = get_input("同线性数据文件路径", "synteny_data.tsv")
min_block = int(get_input("最小区块大小(bp)", "100000"))
min_genes = int(get_input("最小区块基因数", "5"))
output_file = get_input("检测结果路径", "synteny_blocks.tsv")

pairs = []
with open(input_file, 'r') as f:
    header = f.readline()
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 6:
            chr_a, start_a, end_a = parts[0], int(parts[1]), int(parts[2])
            chr_b, start_b, end_b = parts[3], int(parts[4]), int(parts[5])
            gene = parts[6] if len(parts) > 6 else ''
            pairs.append((chr_a, start_a, end_a, chr_b, start_b, end_b, gene))

print(f"✅ 加载 {len(pairs)} 同线性配对")

blocks = []
current_block = []
prev = None

for p in pairs:
    if not current_block:
        current_block = [p]
    else:
        prev = current_block[-1]
        if p[0] == prev[0] and p[3] == prev[3]:
            dist_a = abs(p[1] - prev[2])
            dist_b = abs(p[4] - prev[5])
            if dist_a < 500000 and dist_b < 500000:
                current_block.append(p)
            else:
                if len(current_block) >= min_genes:
                    blocks.append(current_block)
                current_block = [p]
        else:
            if len(current_block) >= min_genes:
                blocks.append(current_block)
            current_block = [p]

if len(current_block) >= min_genes:
    blocks.append(current_block)

with open(output_file, 'w') as f:
    f.write("block_id\tchr_a\tstart_a\tend_a\tchr_b\tstart_b\tend_b\tsize_a\tsize_b\tgene_count\n")
    for i, block in enumerate(blocks):
        chr_a = block[0][0]
        start_a = min(p[1] for p in block)
        end_a = max(p[2] for p in block)
        chr_b = block[0][3]
        start_b = min(p[4] for p in block)
        end_b = max(p[5] for p in block)
        size_a = end_a - start_a
        size_b = end_b - start_b
        f.write(f"B{i}\t{chr_a}\t{start_a}\t{end_a}\t{chr_b}\t{start_b}\t{end_b}\t{size_a}\t{size_b}\t{len(block)}\n")

filtered = [b for b in blocks if max(p[2]-p[1] for p in b) >= min_block or len(b) >= min_genes]
print(f"\n✅ 检测完成: {len(blocks)} 个区块 (过滤后: {len(filtered)})")
print(f"📄 结果: {output_file}")
