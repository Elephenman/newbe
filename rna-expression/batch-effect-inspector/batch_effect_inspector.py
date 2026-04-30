#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批次效应检测+可视化"""
import os, sys
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v=="" or v is None: return d
    try: return t(v)
    except: return d

def inspect_batch(mat_path, batch_file, method="PCA"):
    import numpy as np
    try: import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    except: print("需要matplotlib"); return
    
    mat = np.loadtxt(mat_path, delimiter=',', skiprows=1).T  # 样本为行
    # 分组
    batches = {}; labels = []
    if batch_file and os.path.exists(batch_file):
        with open(batch_file) as f:
            for line in f: fields=line.strip().split('\t'); batches[fields[0]]=fields[1]
        header = open(mat_path).readline().strip().split(',')[1:]
        labels = [batches.get(s,'Unknown') for s in header]
    
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2); coords = pca.fit_transform(mat)
    
    unique = list(set(labels))
    cmap = plt.cm.get_cmap('Set2', len(unique))
    plt.figure(figsize=(8,6))
    for i, g in enumerate(unique):
        idx=[i for i,l in enumerate(labels) if l==g]
        plt.scatter(coords[idx,0], coords[idx,1], label=g, s=50, color=cmap(i))
    plt.legend(); plt.title("Batch Effect PCA"); plt.tight_layout()
    plt.savefig("batch_pca.png", dpi=300); plt.close()
    
    # 批次间相关性
    from scipy import stats
    batch_means = {}
    for g in unique:
        idx=[i for i,l in enumerate(labels) if l==g]
        batch_means[g] = np.mean(mat[idx], axis=0)
    print(f"✅ 批次效应检测完成")
    for g,m in batch_means.items(): print(f"   {g}: 均值向量长度={len(m)}")
    print(f"   PC1解释比例: {pca.explained_variance_ratio_[0]*100:.1f}%")

def main():
    print("="*50); print("  🔍 批次效应检测"); print("="*50)
    m=get_input("表达矩阵CSV路径","expression.csv")
    b=get_input("批次信息文件(留空=无)","")
    t=get_input("检测方法(PCA/boxplot)","PCA")
    inspect_batch(m, b or None, t)
if __name__=="__main__": main()