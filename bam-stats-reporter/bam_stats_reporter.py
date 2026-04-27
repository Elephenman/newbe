#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BAM/SAM文件关键指标速查
pysam封装，5行代码出报告

功能：
- 总reads数、mapped率、duplicate率
- 平均覆盖度、插入长度分布、MAPQ分布
- 终端打印 + 可选CSV统计表
"""

import os
import sys
from collections import defaultdict

try:
    import pysam
except ImportError:
    print("  ❌ 需要安装pysam: pip install pysam")
    sys.exit(1)


def get_input(prompt, default=None, type=str):
    """统一交互式输入函数"""
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "":
        return default
    try:
        return type(val)
    except (ValueError, TypeError):
        print(f"  ⚠ 输入格式错误，使用默认值: {default}")
        return default


def analyze_bam(bam_path, genome_length=None):
    """分析BAM/SAM文件，返回统计字典"""
    stats = {
        "total_reads": 0,
        "mapped_reads": 0,
        "unmapped_reads": 0,
        "duplicate_reads": 0,
        "secondary_reads": 0,
        "supplementary_reads": 0,
        "insert_lengths": [],
        "mapq_scores": [],
        "coverage": None,
        "ref_names": [],
    }

    bamfile = pysam.AlignmentFile(bam_path, "rb")

    for read in bamfile.fetch(until_eof=True):
        stats["total_reads"] += 1

        if read.is_duplicate:
            stats["duplicate_reads"] += 1

        if read.is_secondary:
            stats["secondary_reads"] += 1
            continue

        if read.is_supplementary:
            stats["supplementary_reads"] += 1
            continue

        if read.is_unmapped:
            stats["unmapped_reads"] += 1
        else:
            stats["mapped_reads"] += 1
            stats["mapq_scores"].append(read.mapping_quality)

            # 插入长度
            if read.is_paired and not read.is_unmapped and not read.mate_is_unmapped:
                il = read.template_length
                if il > 0:
                    stats["insert_lengths"].append(il)

    # 计算覆盖度
    if genome_length and genome_length > 0:
        try:
            total_covered_bases = 0
            for contig in bamfile.references:
                contig_len = bamfile.get_reference_length(contig)
                coverage = bamfile.count_coverage(contig)
                for pos_cov in coverage:
                    total_covered_bases += sum(1 for c in pos_cov if c > 0)

            stats["coverage"] = round(total_covered_bases / genome_length * 100, 2)
            stats["ref_names"] = list(bamfile.references)
        except Exception:
            # count_coverage可能失败，用近似计算
            total_aligned_bases = 0
            for read in bamfile.fetch():
                if not read.is_unmapped:
                    try:
                        total_aligned_bases += read.reference_length
                    except Exception:
                        pass
            stats["coverage"] = round(total_aligned_bases / genome_length * 100, 2)

    bamfile.close()
    return stats


def generate_report(stats, bam_path):
    """生成终端报告"""
    total = stats["total_reads"]
    mapped_pct = round(stats["mapped_reads"] / total * 100, 2) if total > 0 else 0
    dup_pct = round(stats["duplicate_reads"] / total * 100, 2) if total > 0 else 0

    # MAPQ统计
    mapq_vals = stats["mapq_scores"]
    avg_mapq = round(sum(mapq_vals) / len(mapq_vals), 1) if mapq_vals else 0
    mapq_0_pct = round(sum(1 for m in mapq_vals if m == 0) / len(mapq_vals) * 100, 2) if mapq_vals else 0
    mapq_20_pct = round(sum(1 for m in mapq_vals if m >= 20) / len(mapq_vals) * 100, 2) if mapq_vals else 0
    mapq_60_pct = round(sum(1 for m in mapq_vals if m >= 60) / len(mapq_vals) * 100, 2) if mapq_vals else 0

    # 插入长度统计
    inserts = stats["insert_lengths"]
    avg_insert = round(sum(inserts) / len(inserts), 1) if inserts else 0
    median_insert = sorted(inserts)[len(inserts)//2] if inserts else 0

    # MAPQ分布
    mapq_dist = defaultdict(int)
    for m in mapq_vals:
        mapq_dist[m // 10 * 10] += 1  # 按10分桶

    coverage_str = f"{stats['coverage']}%" if stats["coverage"] is not None else "未计算（需提供基因组长度）"

    report = f"""
╔══════════════════════════════════════════════════════════════╗
║              BAM/SAM 关键指标速查报告                        ║
╠══════════════════════════════════════════════════════════════╣
║ 文件: {os.path.basename(bam_path)}
║══════════════════════════════════════════════════════════════║
║ 【Reads统计】
║   总reads数:     {total}
║   Mapped:       {stats['mapped_reads']} ({mapped_pct}%)
║   Unmapped:     {stats['unmapped_reads']} ({round(100-mapped_pct,2)}%)
║   Duplicate:    {stats['duplicate_reads']} ({dup_pct}%)
║   Secondary:    {stats['secondary_reads']}
║   Supplementary:{stats['supplementary_reads']}
║══════════════════════════════════════════════════════════════║
║ 【MAPQ分布】
║   平均MAPQ:     {avg_mapq}
║   MAPQ=0:       {mapq_0_pct}%  {'⚠️ 多重比对' if mapq_0_pct > 5 else '✅ 正常'}
║   MAPQ≥20:      {mapq_20_pct}%
║   MAPQ≥60:      {mapq_60_pct}%  {'✅ 高质量' if mapq_60_pct > 80 else '⚠️ 需检查'}
║   分布:
"""
    for q_bin in sorted(mapq_dist.keys()):
        pct = round(mapq_dist[q_bin] / len(mapq_vals) * 100, 1) if mapq_vals else 0
        bar_len = min(int(pct / 2), 50)
        bar = "█" * bar_len
        report += f"║     MAPQ {q_bin}-{q_bin+9}: {bar} ({mapq_dist[q_bin]}, {pct}%)\n"

    report += f"""║══════════════════════════════════════════════════════════════║
║ 【插入长度】
║   平均插入长度: {avg_insert} bp
║   中位数:       {median_insert} bp
║   插入长度数:   {len(inserts)} paired reads
║══════════════════════════════════════════════════════════════║
║ 【覆盖度】
║   平均覆盖度:   {coverage_str}
╚══════════════════════════════════════════════════════════════╝
"""
    return report


def save_csv(stats, bam_path, output_path):
    """保存CSV统计表"""
    total = stats["total_reads"]
    lines = [
        "指标,值",
        f"文件名,{os.path.basename(bam_path)}",
        f"总reads数,{total}",
        f"Mapped reads,{stats['mapped_reads']} ({round(stats['mapped_reads']/total*100,2)}%)",
        f"Unmapped reads,{stats['unmapped_reads']}",
        f"Duplicate reads,{stats['duplicate_reads']} ({round(stats['duplicate_reads']/total*100,2)}%)",
        f"平均MAPQ,{round(sum(stats['mapq_scores'])/len(stats['mapq_scores']),1) if stats['mapq_scores'] else 0}",
        f"平均插入长度,{round(sum(stats['insert_lengths'])/len(stats['insert_lengths']),1) if stats['insert_lengths'] else 0} bp",
        f"覆盖度,{stats['coverage']}%{'(未计算)' if stats['coverage'] is None else ''}",
    ]
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"  ✅ CSV统计已保存: {output_path}")


def main():
    print("=" * 60)
    print("  📊 BAM/SAM 关键指标速查")
    print("=" * 60)

    filepath = get_input("输入BAM/SAM文件路径", default="sample.bam")
    if not os.path.exists(filepath):
        print(f"  ❌ 文件不存在: {filepath}")
        sys.exit(1)

    calc_coverage = get_input("是否计算覆盖度(yes/no)", default="no")
    genome_length = None
    if calc_coverage.lower() in ('yes', 'y', 'true', '1'):
        genome_length = get_input("参考基因组总长度(bp)", default=3000000000, type=int)

    save_csv = get_input("是否保存CSV统计表", default="no")
    export_csv = save_csv.lower() in ('yes', 'y', 'true', '1')

    print(f"\n  ⏳ 正在解析BAM文件: {filepath} ...")

    stats = analyze_bam(filepath, genome_length)

    if stats["total_reads"] == 0:
        print("  ❌ 未读取到任何read，请检查文件格式")
        sys.exit(1)

    report = generate_report(stats, filepath)
    print(report)

    if export_csv:
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_dir = os.path.dirname(filepath) or "."
        output_path = os.path.join(output_dir, f"{base_name}_bam_stats.csv")
        save_csv(stats, filepath, output_path)

    print("  ✅ BAM指标速查完成！")


if __name__ == "__main__":
    main()