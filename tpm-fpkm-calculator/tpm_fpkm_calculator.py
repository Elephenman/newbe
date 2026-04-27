#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""raw counts → TPM/FPKM/CPM转换器"""
import os, sys, math

def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "" or val is None: return default
    try: return type(val)
    except: return default

def load_gene_lengths(length_file):
    lengths = {}
    with open(length_file, 'r') as f:
        header = f.readline()  # skip header
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 2:
                lengths[fields[0]] = float(fields[1])
    return lengths

def convert_counts(filepath, length_file, convert_type="TPM", log2=False):
    # 加载count矩阵
    with open(filepath, 'r') as f:
        header = f.readline().strip().split(',')
        gene_col = header[0]
        sample_cols = header[1:]
        genes = []; counts = []
        for line in f:
            fields = line.strip().split(',')
            genes.append(fields[0])
            counts.append([float(x) for x in fields[1:]])
    
    gene_lengths = load_gene_lengths(length_file) if length_file else {}
    
    import numpy as np
    mat = np.array(counts)
    
    if convert_type == "CPM" or convert_type == "all":
        cpm = mat / mat.sum(axis=0) * 1e6
        if log2: cpm = np.log2(cpm + 1)
    
    if convert_type == "TPM" or convert_type == "all":
        rpk = mat / np.array([gene_lengths.get(g, 1) for g in genes]).reshape(-1, 1)
        tpm = rpk / rpk.sum(axis=0) * 1e6
        if log2: tpm = np.log2(tpm + 1)
    
    if convert_type == "FPKM" or convert_type == "all":
        fpkm = mat / np.array([gene_lengths.get(g, 1) for g in genes]).reshape(-1, 1)
        fpkm = fpkm / mat.sum(axis=0) * 1e9
        if log2: fpkm = np.log2(fpkm + 1)
    
    # 保存结果
    for ct, result in [("CPM", cpm), ("TPM", tpm), ("FPKM", fpkm)]:
        if convert_type == ct or convert_type == "all":
            out_path = filepath.replace('.csv', f'_{ct}.csv')
            with open(out_path, 'w') as out:
                out.write(','.join(header) + '\n')
                for i, g in enumerate(genes):
                    out.write(g + ',' + ','.join(str(x) for x in result[i]) + '\n')
            print(f"✅ {ct}转换完成: {out_path}")

def main():
    print("="*50); print("  📊 Count→TPM/FPKM/CPM转换器"); print("="*50)
    fp = get_input("count矩阵CSV路径", "counts.csv")
    lf = get_input("基因长度文件路径(基因名+长度,TSV)", "gene_lengths.tsv")
    ct = get_input("转换类型(TPM/FPKM/CPM/all)", "TPM")
    l2 = get_input("是否log2转换(yes/no)", "no")
    convert_counts(fp, lf, ct, l2.lower() in ('yes','y'))

if __name__ == "__main__": main()