#!/usr/bin/env python3
"""转录本ID与基因ID与基因名批量映射
从GTF注释文件或BioMart导出文件构建映射表，批量转换ID
"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def parse_gtf(gtf_path):
    """从GTF文件提取transcript_id, gene_id, gene_name映射"""
    mapping = []
    with open(gtf_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue

            feature = parts[2]
            attrs = parts[8]

            # Parse attributes
            gene_id = ''
            gene_name = ''
            transcript_id = ''

            for attr in attrs.split(';'):
                attr = attr.strip()
                if attr.startswith('gene_id'):
                    gene_id = attr.split('"')[1] if '"' in attr else attr.split()[-1]
                elif attr.startswith('gene_name') or attr.startswith('gene_name'):
                    gene_name = attr.split('"')[1] if '"' in attr else attr.split()[-1]
                elif attr.startswith('transcript_id'):
                    transcript_id = attr.split('"')[1] if '"' in attr else attr.split()[-1]

            if feature == 'transcript' and transcript_id:
                mapping.append({
                    'transcript_id': transcript_id,
                    'gene_id': gene_id,
                    'gene_name': gene_name
                })

    return mapping


def parse_biomart(biomart_path):
    """从BioMart导出的TSV文件提取映射"""
    mapping = []
    with open(biomart_path, 'r') as f:
        header = f.readline().strip().split('\t')
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < len(header):
                continue
            row = dict(zip(header, parts))
            mapping.append({
                'transcript_id': row.get('Transcript stable ID', row.get('transcript_id', '')),
                'gene_id': row.get('Gene stable ID', row.get('gene_id', '')),
                'gene_name': row.get('Gene name', row.get('gene_name', row.get('external_gene_name', '')))
            })
    return mapping


def parse_mapping_tsv(filepath):
    """解析简单的TSV映射文件(transcript_id, gene_id, gene_name)"""
    mapping = []
    with open(filepath, 'r') as f:
        header = f.readline()  # skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                mapping.append({
                    'transcript_id': parts[0],
                    'gene_id': parts[1] if len(parts) > 1 else '',
                    'gene_name': parts[2] if len(parts) > 2 else parts[1]
                })
    return mapping


def main():
    print("=" * 60)
    print("  转录本ID与基因ID与基因名批量映射")
    print("=" * 60)
    print()

    mapping_file = get_input("映射源文件路径(GTF/BioMart TSV/简单TSV)", "annotation.gtf")
    mapping_format = get_input("文件格式(gtf/biomart/tsv)", "gtf")
    input_ids = get_input("待映射ID文件路径(每行一个ID,留空=交互输入)", "")
    output_file = get_input("输出映射表路径", "id_mapping.tsv")
    id_type = get_input("输入ID类型(transcript_id/gene_id/gene_name)", "transcript_id")

    print()
    print(f"映射文件:  {mapping_file}")
    print(f"格式:      {mapping_format}")
    print(f"输出:      {output_file}")
    print()

    if not os.path.exists(mapping_file):
        print(f"[ERROR] 映射文件不存在: {mapping_file}")
        sys.exit(1)

    # Parse mapping
    print("[Processing] 解析映射文件...")
    if mapping_format == 'gtf':
        mapping = parse_gtf(mapping_file)
    elif mapping_format == 'biomart':
        mapping = parse_biomart(mapping_file)
    else:
        mapping = parse_mapping_tsv(mapping_file)

    if not mapping:
        print("[ERROR] 未解析到映射记录")
        sys.exit(1)

    print(f"[Processing] 找到 {len(mapping)} 条映射记录")

    # Build lookup dictionaries
    by_transcript = {}
    by_gene_id = {}
    by_gene_name = {}

    for m in mapping:
        if m['transcript_id']:
            by_transcript[m['transcript_id']] = m
        if m['gene_id']:
            by_gene_id.setdefault(m['gene_id'], []).append(m)
        if m['gene_name']:
            by_gene_name.setdefault(m['gene_name'], []).append(m)

    # Get input IDs
    ids_to_map = []
    if input_ids and os.path.exists(input_ids):
        with open(input_ids, 'r') as f:
            ids_to_map = [l.strip() for l in f if l.strip()]
    else:
        ids_str = get_input("输入ID(逗号分隔)", "")
        ids_to_map = [i.strip() for i in ids_str.split(',') if i.strip()]

    if not ids_to_map:
        # Map all
        print("[Processing] 无输入ID，输出完整映射表")
        ids_to_map = list(set(m[id_type] for m in mapping if m[id_type]))

    # Perform mapping
    print(f"[Processing] 映射 {len(ids_to_map)} 个ID...")
    results = []
    mapped = 0
    unmapped = 0

    for query_id in ids_to_map:
        result = {'query': query_id, 'transcript_id': '', 'gene_id': '', 'gene_name': ''}

        if id_type == 'transcript_id':
            m = by_transcript.get(query_id)
            if m:
                result.update(m)
                mapped += 1
            else:
                unmapped += 1
        elif id_type == 'gene_id':
            ms = by_gene_id.get(query_id, [])
            if ms:
                result['gene_id'] = query_id
                result['gene_name'] = ms[0]['gene_name']
                result['transcript_id'] = ';'.join(m['transcript_id'] for m in ms if m['transcript_id'])
                mapped += 1
            else:
                unmapped += 1
        elif id_type == 'gene_name':
            ms = by_gene_name.get(query_id, [])
            if ms:
                result['gene_name'] = query_id
                result['gene_id'] = ms[0]['gene_id']
                result['transcript_id'] = ';'.join(m['transcript_id'] for m in ms if m['transcript_id'])
                mapped += 1
            else:
                unmapped += 1

        results.append(result)

    # Save output
    try:
        with open(output_file, 'w') as out:
            out.write("Query\tTranscript_ID\tGene_ID\tGene_Name\n")
            for r in results:
                out.write(f"{r['query']}\t{r['transcript_id']}\t{r['gene_id']}\t{r['gene_name']}\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  查询ID数:     {len(ids_to_map)}")
    print(f"  映射成功:     {mapped}")
    print(f"  未映射:       {unmapped}")
    print(f"  映射率:       {mapped/len(ids_to_map)*100:.1f}%" if ids_to_map else "  N/A")
    print(f"  输出文件:     {output_file}")
    print("=" * 60)
    print()
    print("[Done] transcript_id_mapper completed successfully!")


if __name__ == "__main__":
    main()
