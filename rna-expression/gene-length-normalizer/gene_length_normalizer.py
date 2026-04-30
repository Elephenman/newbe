#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基因长度偏差校正（RPKM/TPM/GC）"""
import os, sys

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def normalize_gene_length(count_file, method="TPM", output_file=None):
    """基因长度归一化: RPKM, FPKM, or TPM"""
    # 读取计数+长度文件 (gene_id\tcount\tlength)
    data = []
    with open(count_file, 'r') as f:
        header = f.readline()  # skip header
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            fields = line.split('\t') if '\t' in line else line.split(',')
            if len(fields) < 3:
                continue
            gene_id = fields[0]
            try:
                count = float(fields[1])
                length = float(fields[2])
            except ValueError:
                continue
            data.append({"gene_id": gene_id, "count": count, "length": length})

    if not data:
        print("[ERROR] No valid data rows found. Expected format: gene_id<TAB>count<TAB>length")
        return

    total_counts = sum(d["count"] for d in data)

    if method.upper() == "RPKM" or method.upper() == "FPKM":
        # RPKM = (count * 1e9) / (total_counts * length)
        # FPKM is the same for single-end data
        for d in data:
            d["rpkm"] = (d["count"] * 1e9) / (total_counts * d["length"]) if total_counts > 0 and d["length"] > 0 else 0
        norm_key = "rpkm"
    elif method.upper() == "TPM":
        # TPM: first compute RPK, then normalize so all TPMs sum to 1e6
        for d in data:
            d["rpk"] = d["count"] / (d["length"] / 1000) if d["length"] > 0 else 0
        total_rpk = sum(d["rpk"] for d in data)
        for d in data:
            d["tpm"] = (d["rpk"] / total_rpk * 1e6) if total_rpk > 0 else 0
        norm_key = "tpm"
    elif method.upper() == "CPM":
        # CPM = count / total_counts * 1e6
        for d in data:
            d["cpm"] = (d["count"] / total_counts * 1e6) if total_counts > 0 else 0
        norm_key = "cpm"
    else:
        print(f"[ERROR] Unknown method: {method}. Use RPKM, FPKM, TPM, or CPM.")
        return

    # 输出
    out_path = output_file or os.path.splitext(count_file)[0] + f"_{method.upper()}.tsv"
    with open(out_path, 'w') as out:
        out.write(f"gene_id\tcount\tlength\t{norm_key}\n")
        for d in data:
            out.write(f"{d['gene_id']}\t{d['count']}\t{d['length']}\t{d[norm_key]:.4f}\n")

    norm_values = [d[norm_key] for d in data]
    print(f"Gene length normalization complete")
    print(f"  Method: {method.upper()}")
    print(f"  Genes: {len(data)}")
    print(f"  Total counts: {total_counts:.0f}")
    if norm_values:
        print(f"  {norm_key} range: {min(norm_values):.4f} - {max(norm_values):.4f}")
        print(f"  {norm_key} median: {sorted(norm_values)[len(norm_values)//2]:.4f}")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  基因长度偏差校正（RPKM/TPM/CPM）")
    print("=" * 60)
    count_file = get_input("计数+长度文件(gene_id/count/length TSV)", "counts.tsv")
    method = get_input("归一化方法(RPKM/FPKM/TPM/CPM)", "TPM")
    output = get_input("输出文件路径", "")
    normalize_gene_length(count_file, method.upper(), output or None)

if __name__ == "__main__":
    main()
