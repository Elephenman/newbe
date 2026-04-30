#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GFF3到GTF格式转换+属性保留"""
import os, sys, re

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def gff3_to_gtf(gff3_path, output_file=None, source_name="gff3_converter"):
    """将GFF3格式转换为GTF格式，保留关键属性"""
    out_path = output_file or gff3_path.replace('.gff3', '').replace('.gff', '') + '.gtf'

    converted = 0; skipped = 0

    with open(gff3_path, 'r') as fin, open(out_path, 'w') as fout:
        for line in fin:
            # 保留注释行
            if line.startswith('#'):
                fout.write(line)
                continue

            line = line.strip()
            if not line:
                continue

            fields = line.split('\t')
            if len(fields) < 9:
                skipped += 1
                continue

            seqid, source, ftype, start, end, score, strand, phase, attributes = fields

            # GTF只保留gene/transcript/exon/CDS/UTR/start_codon/stop_codon等
            gtf_features = {'gene', 'transcript', 'exon', 'CDS', 'five_prime_utr',
                           'three_prime_utr', 'start_codon', 'stop_codon',
                           'UTR', '5UTR', '3UTR', 'mRNA', 'ncRNA', 'rRNA', 'tRNA', 'miRNA'}

            if ftype not in gtf_features:
                # 尝试映射
                type_map = {'mRNA': 'transcript', 'primary_transcript': 'transcript',
                           'five_prime_UTR': 'five_prime_utr', 'three_prime_UTR': 'three_prime_utr'}
                if ftype in type_map:
                    ftype = type_map[ftype]
                else:
                    skipped += 1
                    continue

            # 解析GFF3属性 (key=value;key=value)
            attrs = {}
            for attr in attributes.split(';'):
                attr = attr.strip()
                if '=' in attr:
                    key, val = attr.split('=', 1)
                    attrs[key.strip()] = val.strip()

            # 构建GTF属性 (gene_id "xxx"; transcript_id "xxx"; ...)
            gene_id = attrs.get('gene_id', attrs.get('gene', attrs.get('Parent', attrs.get('ID', 'unknown'))))
            transcript_id = attrs.get('transcript_id', attrs.get('transcript', attrs.get('ID', '')))

            # Clean gene_id: if it's a comma-separated list, take first
            if ',' in gene_id:
                gene_id = gene_id.split(',')[0]

            # Build GTF attribute string
            gtf_attrs = f'gene_id "{gene_id}";'

            if transcript_id and transcript_id != gene_id:
                gtf_attrs += f' transcript_id "{transcript_id}";'

            # Preserve additional attributes as GTF format
            for key in ['gene_name', 'gene_biotype', 'gene_type', 'exon_number', 'protein_id']:
                if key in attrs:
                    gtf_attrs += f' {key} "{attrs[key]}";'

            # GTF coordinates: same as GFF3 (1-based, inclusive for features)
            # But CDS phase is kept
            fout.write(f"{seqid}\t{source_name}\t{ftype}\t{start}\t{end}\t{score}\t{strand}\t{phase}\t{gtf_attrs}\n")
            converted += 1

    print(f"GFF3 to GTF conversion complete")
    print(f"  Converted: {converted} features")
    print(f"  Skipped: {skipped} features (unsupported types)")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  GFF3到GTF格式转换+属性保留")
    print("=" * 60)
    gff3_file = get_input("GFF3文件路径", "annotation.gff3")
    output = get_input("输出GTF文件路径", "")
    source = get_input("GTF source名称", "gff3_converter")
    gff3_to_gtf(gff3_file, output or None, source)

if __name__ == "__main__":
    main()
