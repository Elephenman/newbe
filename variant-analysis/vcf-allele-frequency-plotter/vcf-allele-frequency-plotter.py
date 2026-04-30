#!/usr/bin/env python3
"""VCF等位基因频率分布可视化"""

# VCF等位基因频率分布可视化
import matplotlib.pyplot as plt
import gzip

print("=" * 60)
print("  🧬 VCF等位基因频率分布可视化")
print("=" * 60)

input_vcf = get_input("输入VCF文件路径", "variants.vcf")
af_field = get_input("等位基因频率字段名", "AF")
min_af = float(get_input("最小频率阈值", "0"))
max_af = float(get_input("最大频率阈值", "1"))
plot_out = get_input("输出图片路径", "af_distribution.png")

afs = []

opener = gzip.open if input_vcf.endswith('.gz') else open
mode = 'rt' if input_vcf.endswith('.gz') else 'r'

with opener(input_vcf, mode) as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        info = parts[7]
        for item in info.split(';'):
            if item.startswith(af_field + '='):
                val_str = item.split('=')[1]
                for v in val_str.split(','):
                    try:
                        af = float(v)
                        if min_af <= af <= max_af:
                            afs.append(af)
                    except ValueError:
                        continue

if not afs:
    print("⚠️ 未找到有效等位基因频率数据")
    exit(0)

print(f"\n✅ 提取完成: {len(afs)} 个有效AF值")
print(f"  平均AF: {sum(afs)/len(afs):.4f}")
print(f"  中位数: {sorted(afs)[len(afs)//2]:.4f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(afs, bins=50, edgecolor='black', alpha=0.7, color='#DD8452')
axes[0].set_xlabel("Allele Frequency")
axes[0].set_ylabel("Count")
axes[0].set_title("AF Distribution")

rare = sum(1 for a in afs if a < 0.01)
common = sum(1 for a in afs if a >= 0.05)
low_freq = len(afs) - rare - common
axes[1].bar(['Rare(<0.01)', 'Low(0.01-0.05)', 'Common(>=0.05)'],
            [rare, low_freq, common], color=['#C44E52', '#4C72B0', '#55A868'])
axes[1].set_ylabel("Count")
axes[1].set_title("AF Category")

plt.tight_layout()
plt.savefig(plot_out, dpi=150)
print(f"\n📊 分布图已保存到: {plot_out}")
