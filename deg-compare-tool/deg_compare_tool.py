#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多组DEG结果交叉对比"""
import os, sys

def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "" or val is None: return default
    try: return type(val)
    except: return default

def compare_deg(files, mode="Venn", gene_id_col="gene"):
    gene_sets = {}; all_genes = set()
    for fp in files:
        name = os.path.splitext(os.path.basename(fp))[0]
        genes = set()
        with open(fp, 'r') as f:
            header = f.readline().strip().split(',')
            g_idx = header.index(gene_id_col) if gene_id_col in header else 0
            for line in f:
                fields = line.strip().split(',')
                genes.add(fields[g_idx])
        gene_sets[name] = genes
        all_genes.update(genes)
    
    # 交叉分析
    intersections = {}
    from itertools import combinations
    for combo in combinations(gene_sets.keys(), 2):
        inter = gene_sets[combo[0]] & gene_sets[combo[1]]
        intersections[f"{combo[0]}∩{combo[1]}"] = inter
    
    # 绘图
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        if mode == "Venn" and len(files) <= 3:
            try:
                from matplotlib_venn import venn2, venn3
                plt.figure(figsize=(8,6))
                if len(files) == 2:
                    venn2([gene_sets[files[0]], gene_sets[files[1]]], set_labels=[os.path.splitext(os.path.basename(f))[0] for f in files[:2]])
                elif len(files) == 3:
                    venn3([gene_sets[f] for f in files[:3]], set_labels=[os.path.splitext(os.path.basename(f))[0] for f in files[:3]])
                plt.savefig("deg_compare_venn.png", dpi=300); plt.close()
                print("✅ Venn图已保存")
            except: print("需要matplotlib-venn")
        else:
            # UpSet或简单柱状图
            plt.figure(figsize=(10,6))
            sizes = [len(gene_sets[n]) for n in gene_sets]
            plt.bar(range(len(gene_sets)), sizes, color='#2196F3')
            plt.xticks(range(len(gene_sets)), [n[:15] for n in gene_sets], rotation=30)
            plt.ylabel('DEG数量')
            plt.title('多组DEG对比')
            plt.savefig("deg_compare_bar.png", dpi=300); plt.close()
    except: pass
    
    # 保存交集基因
    with open("deg_intersection.csv", 'w') as out:
        out.write("比较组,交集基因数,基因列表\n")
        for name, inter in intersections.items():
            out.write(f"{name},{len(inter)},{'|'.join(list(inter)[:100])}\n")
    for name in gene_sets:
        unique = gene_sets[name] - all_genes - gene_sets[name]  # 简化
        with open(f"deg_{name}_specific.csv", 'w') as out:
            for g in gene_sets[name]: out.write(g + '\n')
    print(f"✅ DEG交叉对比完成: {len(files)}组")
    for n, s in gene_sets.items(): print(f"   {n}: {len(s)} genes")

def main():
    print("="*50); print("  🔄 DEG交叉对比工具"); print("="*50)
    file_input = get_input("DEG结果文件路径(逗号分隔多个)", "deg1.csv,deg2.csv")
    files = [f.strip() for f in file_input.split(',') if f.strip()]
    mode = get_input("对比模式(Venn/UpSet/bar)", "Venn")
    gc = get_input("基因ID列名", "gene")
    compare_deg(files, mode, gc)

if __name__ == "__main__": main()