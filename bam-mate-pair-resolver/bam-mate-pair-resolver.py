#!/usr/bin/env python3
"""BAM mate-pair信息解析+配对修复"""

# BAM mate-pair信息解析与修复
import pysam

print("=" * 60)
print("  🧬 BAM Mate-Pair解析与修复")
print("=" * 60)

input_bam = get_input("输入BAM文件路径", "sample.bam")
output_bam = get_input("输出BAM路径", "resolved.bam")
fix_mates = get_input("是否修复mate信息(yes/no)", "yes")
report_file = get_input("配对统计报告路径", "mate_pair_report.txt")

paired = 0
unpaired = 0
proper = 0
mate_unmapped = 0
mate_wrong_chr = 0
abnormal_isize = 0

try:
    bamfile = pysam.AlignmentFile(input_bam, "rb")
    out = pysam.AlignmentFile(output_bam, "wb", template=bamfile)
    
    for read in bamfile:
        if read.is_paired:
            paired += 1
            if read.is_proper_pair:
                proper += 1
            if read.mate_is_unmapped:
                mate_unmapped += 1
            elif read.reference_name != read.next_reference_name:
                mate_wrong_chr += 1
            if abs(read.template_length) > 10000:
                abnormal_isize += 1
        else:
            unpaired += 1
        out.write(read)
    
    bamfile.close()
    out.close()
except Exception as e:
    print(f"❌ 错误: {e}")
    exit(1)

print(f"\n✅ 解析完成:")
print(f"  Paired reads: {paired}")
print(f"  Proper pairs: {proper} ({proper/paired*100:.1f}% if paired)")
print(f"  Unpaired: {unpaired}")
print(f"  Mate unmapped: {mate_unmapped}")
print(f"  Mate wrong chr: {mate_wrong_chr}")
print(f"  Abnormal isize: {abnormal_isize}")

if fix_mates == "yes":
    pysam.fixmate(output_bam, output_bam + ".fixed.bam")
    print("  ✅ Mate信息已修复")

with open(report_file, 'w') as f:
    f.write(f"Mate-Pair Report\n")
    f.write(f"Paired: {paired}\nProper: {proper}\nUnpaired: {unpaired}\n")
    f.write(f"Mate unmapped: {mate_unmapped}\nMate wrong chr: {mate_wrong_chr}\n")
print(f"📄 报告已保存到: {report_file}")
