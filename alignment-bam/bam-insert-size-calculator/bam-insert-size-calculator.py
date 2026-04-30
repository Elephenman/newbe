#!/usr/bin/env python3
"""BAM插入片段大小统计+分布图"""

# BAM插入片段大小统计+分布图
import pysam
import matplotlib.pyplot as plt
import numpy as np

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


print("=" * 60)
print("  🧬 BAM插入片段大小统计")
print("=" * 60)

input_bam = get_input("输入BAM文件路径", "sample.bam")
min_isize = int(get_input("最小插入片段大小", "0"))
max_isize = int(get_input("最大插入片段大小", "1000"))
plot_out = get_input("分布图输出路径", "insert_size_distribution.png")
stats_out = get_input("统计结果路径", "insert_size_stats.txt")

insert_sizes = []

try:
    bamfile = pysam.AlignmentFile(input_bam, "rb")
    for read in bamfile:
        if read.is_proper_pair and not read.is_secondary and not read.is_supplementary:
            isize = abs(read.template_length)
            if min_isize <= isize <= max_isize:
                insert_sizes.append(isize)
    bamfile.close()
except Exception as e:
    print(f"❌ BAM文件读取错误: {e}")
    exit(1)

if not insert_sizes:
    print("⚠️ 未找到有效插入片段数据")
    exit(0)

isize_arr = np.array(insert_sizes)
print(f"\n✅ 统计完成: {len(insert_sizes)} 有效片段")
print(f"  中位数: {np.median(isize_arr):.1f}")
print(f"  平均值: {np.mean(isize_arr):.1f}")
print(f"  标准差: {np.std(isize_arr):.1f}")
print(f"  最小值: {np.min(isize_arr)}")
print(f"  最大值: {np.max(isize_arr)}")

plt.figure(figsize=(10, 6))
plt.hist(insert_sizes, bins=50, edgecolor='black', alpha=0.7, color='#4C72B0')
plt.xlabel("Insert Size (bp)")
plt.ylabel("Count")
plt.title("Insert Size Distribution")
plt.axvline(np.median(isize_arr), color='red', linestyle='--', label=f'Median={np.median(isize_arr):.0f}')
plt.legend()
plt.tight_layout()
plt.savefig(plot_out, dpi=150)
print(f"\n📊 分布图已保存到: {plot_out}")

with open(stats_out, 'w') as f:
    f.write(f"Insert Size Statistics\n")
    f.write(f"Total pairs: {len(insert_sizes)}\n")
    f.write(f"Median: {np.median(isize_arr):.1f}\n")
    f.write(f"Mean: {np.mean(isize_arr):.1f}\n")
    f.write(f"Std: {np.std(isize_arr):.1f}\n")
print(f"📄 统计结果已保存到: {stats_out}")
