#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FASTQ质量一键体检报告
纯Python解析，不依赖FastQC，3秒出结果

功能：
- reads总数、平均长度、Q20/Q30比例
- GC含量分布、N碱基比例
- adapter残留检测（Illumina TruSeq等常见adapter）
- 终端打印报告 + 可选txt/html报告文件
"""

import os
import sys
from collections import defaultdict


# ========== 交互式输入统一范式 ==========

def get_input(prompt, default=None, type=str):
    """统一交互式输入函数，支持默认值和类型转换"""
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "":
        return default
    try:
        return type(val)
    except (ValueError, TypeError):
        print(f"  ⚠ 输入格式错误，使用默认值: {default}")
        return default


# ========== 常见adapter序列库 ==========

ADAPTER_SEQUENCES = {
    "Illumina TruSeq Read 1": "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA",
    "Illumina TruSeq Read 2": "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT",
    "Illumina Small RNA 3": "TGGAATTCTCGGGTGCCAAGG",
    "Illumina Small RNA 5": "GTTCAGAGTTCTACAGTCCGACGATC",
    "Nextera Transposase Read 1": "CTGTCTCTTATACACATCT",
    "Nextera Transposase Read 2": "CTGTCTCTTATACACATCTCCGAGCCCACGAGAC",
}


# ========== 核心计算函数 ==========

def parse_fastq(filepath):
    """逐行解析FASTQ文件，返回统计结果"""
    stats = {
        "total_reads": 0,
        "total_bases": 0,
        "lengths": [],
        "gc_counts": defaultdict(int),
        "n_bases": 0,
        "quality_scores": [],
        "adapter_hits": defaultdict(int),
        "read_qualities": [],  # 每条read的平均质量
    }

    current_read = []
    line_count = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            current_read.append(line)
            line_count += 1

            if line_count % 4 == 0:
                # 一条完整read：header, sequence, +, quality
                header = current_read[0]
                sequence = current_read[1]
                quality = current_read[3]

                # 基本统计
                seq_len = len(sequence)
                stats["total_reads"] += 1
                stats["total_bases"] += seq_len
                stats["lengths"].append(seq_len)

                # GC含量
                gc = sequence.count('G') + sequence.count('C')
                gc_pct = round(gc / seq_len * 100, 1) if seq_len > 0 else 0
                stats["gc_counts"][gc_pct] += 1

                # N碱基
                n_count = sequence.count('N')
                stats["n_bases"] += n_count

                # 质量分数
                read_qual_sum = 0
                for q_char in quality:
                    q_val = ord(q_char) - 33  # Phred+33
                    stats["quality_scores"].append(q_val)
                    read_qual_sum += q_val
                avg_read_qual = read_qual_sum / seq_len if seq_len > 0 else 0
                stats["read_qualities"].append(avg_read_qual)

                # adapter检测（检查序列前20bp是否包含adapter前缀）
                seq_prefix = sequence[:30]
                for adapter_name, adapter_seq in ADAPTER_SEQUENCES.items():
                    adapter_prefix = adapter_seq[:15]
                    if adapter_prefix in seq_prefix:
                        stats["adapter_hits"][adapter_name] += 1

                current_read = []

    return stats


def calculate_q_metrics(quality_scores):
    """计算Q20/Q30比例"""
    if not quality_scores:
        return 0, 0
    q20_count = sum(1 for q in quality_scores if q >= 20)
    q30_count = sum(1 for q in quality_scores if q >= 30)
    total = len(quality_scores)
    q20_pct = round(q20_count / total * 100, 2)
    q30_pct = round(q30_count / total * 100, 2)
    return q20_pct, q30_pct


def generate_report(stats, filepath):
    """生成文本报告"""
    q20, q30 = calculate_q_metrics(stats["quality_scores"])

    avg_len = round(stats["total_bases"] / stats["total_reads"], 1) if stats["total_reads"] > 0 else 0
    min_len = min(stats["lengths"]) if stats["lengths"] else 0
    max_len = max(stats["lengths"]) if stats["lengths"] else 0

    total_n_pct = round(stats["n_bases"] / stats["total_bases"] * 100, 4) if stats["total_bases"] > 0 else 0

    # GC含量分布统计
    gc_bins = defaultdict(int)
    for gc_pct, count in stats["gc_counts"].items():
        bin_idx = int(gc_pct / 10) * 10
        gc_bins[bin_idx] += count

    avg_gc = round(sum(gc_pct * count for gc_pct, count in stats["gc_counts"].items()) / stats["total_reads"], 1) if stats["total_reads"] > 0 else 0

    report = f"""
╔══════════════════════════════════════════════════════════════╗
║              FASTQ 质量体检报告                              ║
╠══════════════════════════════════════════════════════════════╣
║ 文件: {os.path.basename(filepath)}
║══════════════════════════════════════════════════════════════║
║ 【基本信息】
║   总reads数:     {stats['total_reads']}
║   总碱基数:     {stats['total_bases']}
║   平均长度:     {avg_len} bp
║   最短read:     {min_len} bp
║   最长read:     {max_len} bp
║══════════════════════════════════════════════════════════════║
║ 【质量指标】
║   Q20比例:      {q20}%  {'✅ 优秀' if q20 >= 90 else '⚠️ 一般' if q20 >= 80 else '❌ 较差'}
║   Q30比例:      {q30}%  {'✅ 优秀' if q30 >= 85 else '⚠️ 一般' if q30 >= 70 else '❌ 较差'}
║   平均质量:     {round(sum(stats['read_qualities']) / len(stats['read_qualities']), 1) if stats['read_qualities'] else 0}
║══════════════════════════════════════════════════════════════║
║ 【碱基组成】
║   平均GC%:      {avg_gc}%
║   N碱基比例:    {total_n_pct}%  {'✅ 正常' if total_n_pct < 0.5 else '⚠️ 较高'}
║   GC分布:
"""
    for bin_start in sorted(gc_bins.keys()):
        bar_len = min(int(gc_bins[bin_start] / stats["total_reads"] * 50), 50)
        bar = "█" * bar_len
        report += f"║     {bin_start}-{bin_start+9}%: {bar} ({gc_bins[bin_start]})\n"

    report += f"""║══════════════════════════════════════════════════════════════║
║ 【Adapter检测】
"""
    if any(stats["adapter_hits"].values()):
        for adapter_name, hits in stats["adapter_hits"].items():
            pct = round(hits / stats["total_reads"] * 100, 2)
            report += f"║   {adapter_name}: {hits} reads ({pct}%)\n"
        total_adapter_pct = round(sum(stats["adapter_hits"].values()) / stats["total_reads"] * 100, 2)
        report += f"║   总adapter残留: {total_adapter_pct}%  {'⚠️ 建议修剪' if total_adapter_pct > 1 else '✅ 可忽略'}\n"
    else:
        report += "║   ✅ 未检测到常见adapter残留\n"

    report += "╚══════════════════════════════════════════════════════════════╝\n"
    return report


def save_txt_report(report, output_path):
    """保存txt格式报告"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"  ✅ txt报告已保存: {output_path}")


def save_html_report(stats, filepath, output_path):
    """保存html格式报告（带图表样式）"""
    q20, q30 = calculate_q_metrics(stats["quality_scores"])
    avg_len = round(stats["total_bases"] / stats["total_reads"], 1) if stats["total_reads"] > 0 else 0
    avg_gc = round(sum(gc_pct * count for gc_pct, count in stats["gc_counts"].items()) / stats["total_reads"], 1) if stats["total_reads"] > 0 else 0
    total_n_pct = round(stats["n_bases"] / stats["total_bases"] * 100, 4) if stats["total_bases"] > 0 else 0

    # GC分布HTML
    gc_bar_html = ""
    gc_bins = defaultdict(int)
    for gc_pct, count in stats["gc_counts"].items():
        bin_idx = int(gc_pct / 10) * 10
        gc_bins[bin_idx] += count
    for bin_start in sorted(gc_bins.keys()):
        pct = round(gc_bins[bin_start] / stats["total_reads"] * 100, 1)
        gc_bar_html += f'<tr><td>{bin_start}-{bin_start+9}%</td><td><div style="background:#4CAF50;width:{pct}%;height:20px;border-radius:3px;"></div></td><td>{gc_bins[bin_start]} reads ({pct}%)</td></tr>\n'

    # Adapter检测HTML
    adapter_html = ""
    if any(stats["adapter_hits"].values()):
        for name, hits in stats["adapter_hits"].items():
            pct = round(hits / stats["total_reads"] * 100, 2)
            adapter_html += f'<tr><td>{name}</td><td>{hits}</td><td>{pct}%</td></tr>\n'
    else:
        adapter_html = '<tr><td colspan="3" style="color:green;">未检测到常见adapter残留 ✅</td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>FASTQ质量体检报告</title>
<style>
body {{ font-family: 'Segoe UI', Arial; margin: 20px; background: #f5f5f5; }}
.card {{ background: white; border-radius: 8px; padding: 20px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
h1 {{ color: #2196F3; }} h2 {{ color: #333; border-bottom: 2px solid #2196F3; padding-bottom: 5px; }}
table {{ width: 100%; border-collapse: collapse; }} th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
.good {{ color: #4CAF50; font-weight: bold; }} .warn {{ color: #FF9800; font-weight: bold; }} .bad {{ color: #F44336; font-weight: bold; }}
.bar-container {{ width: 100%; background: #e0e0e0; height: 20px; border-radius: 3px; }}
</style></head><body>
<h1>🧬 FASTQ质量体检报告</h1>
<p>文件: <b>{os.path.basename(filepath)}</b></p>

<div class="card"><h2>📊 基本信息</h2><table>
<tr><td>总reads数</td><td><b>{stats['total_reads']}</b></td></tr>
<tr><td>总碱基数</td><td><b>{stats['total_bases']}</b></td></tr>
<tr><td>平均长度</td><td><b>{avg_len} bp</b></td></tr>
</table></div>

<div class="card"><h2>🎯 质量指标</h2><table>
<tr><td>Q20比例</td><td><b>{q20}%</b> <span class="{'good' if q20>=90 else 'warn' if q20>=80 else 'bad'}">{'✅优秀' if q20>=90 else '⚠️一般' if q20>=80 else '❌较差'}</span></td></tr>
<tr><td>Q30比例</td><td><b>{q30}%</b> <span class="{'good' if q30>=85 else 'warn' if q30>=70 else 'bad'}">{'✅优秀' if q30>=85 else '⚠️一般' if q30>=70 else '❌较差'}</span></td></tr>
</table></div>

<div class="card"><h2>🧪 碱基组成</h2><table>
<tr><td>平均GC%</td><td><b>{avg_gc}%</b></td></tr>
<tr><td>N碱基比例</td><td><b>{total_n_pct}%</b></td></tr>
</table>
<h3>GC分布</h3><table><tr><th>GC范围</th><th>分布</th><th>数量</th></tr>
{gc_bar_html}</table></div>

<div class="card"><h2>🔍 Adapter检测</h2><table><tr><th>Adapter类型</th><th>命中数</th><th>比例</th></tr>
{adapter_html}</table></div>
</body></html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✅ html报告已保存: {output_path}")


# ========== 主函数 ==========

def main():
    print("=" * 60)
    print("  🧬 FASTQ质量一键体检报告")
    print("=" * 60)

    # 交互式参数输入
    filepath = get_input("输入FASTQ文件路径", default="sample.fastq.gz")
    if not os.path.exists(filepath):
        print(f"  ❌ 文件不存在: {filepath}")
        sys.exit(1)

    generate_file = get_input("是否生成报告文件", default="yes")
    save_report = generate_file.lower() in ('yes', 'y', 'true', '1')

    report_format = get_input("报告格式(txt/html)", default="txt") if save_report else "txt"

    print(f"\n  ⏳ 正在解析FASTQ文件: {filepath} ...")

    # 解析FASTQ
    stats = parse_fastq(filepath)

    if stats["total_reads"] == 0:
        print("  ❌ 未解析到任何read，请检查文件格式")
        sys.exit(1)

    # 生成并打印报告
    report = generate_report(stats, filepath)
    print(report)

    # 保存报告文件
    if save_report:
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        if base_name.endswith('.fastq') or base_name.endswith('.fq'):
            base_name = os.path.splitext(base_name)[0]
        output_dir = os.path.dirname(filepath) or "."

        if report_format == "html":
            output_path = os.path.join(output_dir, f"{base_name}_qc_report.html")
            save_html_report(stats, filepath, output_path)
        else:
            output_path = os.path.join(output_dir, f"{base_name}_qc_report.txt")
            save_txt_report(report, output_path)

    print("  ✅ FASTQ质量体检完成！")


if __name__ == "__main__":
    main()