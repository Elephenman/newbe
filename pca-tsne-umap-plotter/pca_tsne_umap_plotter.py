#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""表达矩阵降维可视化三合一"""
import os, sys

def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "" or val is None: return default
    try: return type(val)
    except: return default

def run_dimred(filepath, group_file, methods="all", label_samples=False, color_scheme="default"):
    import numpy as np
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    except: print("需要matplotlib"); return
    try:
        from sklearn.decomposition import PCA
        from sklearn.manifold import TSNE
    except: print("需要scikit-learn"); return
    
    # 加载表达矩阵
    mat = np.loadtxt(filepath, delimiter=',', skiprows=1)
    # 加载分组
    groups = {}; group_labels = []
    if group_file and os.path.exists(group_file):
        with open(group_file, 'r') as f:
            for line in f:
                fields = line.strip().split('\t')
                if len(fields) >= 2: groups[fields[0]] = fields[1]
        sample_names = open(filepath).readline().strip().split(',')[1:]
        group_labels = [groups.get(s, 'Unknown') for s in sample_names]
    else:
        group_labels = ['All'] * (mat.shape[1] if len(mat.shape)>1 else 1)
    
    # 转置（样本为行）
    mat_t = mat.T if mat.shape[0] > mat.shape[1] else mat
    
    # 配色
    unique_groups = list(set(group_labels))
    cmap = plt.cm.get_cmap('Set2' if color_scheme == 'default' else color_scheme, len(unique_groups))
    colors = [cmap(unique_groups.index(g)) for g in group_labels]
    
    base = os.path.splitext(os.path.basename(filepath))[0]
    
    if methods == "all": methods_list = ["PCA", "tSNE", "UMAP"]
    else: methods_list = methods.split(',')
    
    for method in methods_list:
        if method == "PCA":
            pca = PCA(n_components=2)
            coords = pca.fit_transform(mat_t)
            var_exp = pca.explained_variance_ratio_
            title = f"PCA (PC1={var_exp[0]*100:.1f}%, PC2={var_exp[1]*100:.1f}%)"
        elif method == "tSNE":
            tsne = TSNE(n_components=2, perplexity=min(30, mat_t.shape[0]-1))
            coords = tsne.fit_transform(mat_t)
            title = "t-SNE"
        elif method == "UMAP":
            try:
                from umap import UMAP
                coords = UMAP(n_components=2).fit_transform(mat_t)
                title = "UMAP"
            except: print("需要umap-learn: pip install umap-learn"); continue
        
        plt.figure(figsize=(8, 6))
        plt.scatter(coords[:,0], coords[:,1], c=colors, s=50, alpha=0.8)
        for g in unique_groups:
            idx = [i for i, gl in enumerate(group_labels) if gl == g]
            plt.scatter(coords[idx,0], coords[idx,1], c=[cmap(unique_groups.index(g))], s=50, label=g)
        plt.legend()
        plt.title(title)
        if label_samples:
            sample_names = open(filepath).readline().strip().split(',')[1:]
            for i, name in enumerate(sample_names[:50]):
                plt.annotate(name, (coords[i,0], coords[i,1]), fontsize=6)
        plt.tight_layout()
        plt.savefig(f"{base}_{method}.png", dpi=300)
        plt.close()
        print(f"✅ {method}图已保存: {base}_{method}.png")

def main():
    print("="*50); print("  🎯 降维可视化三合一"); print("="*50)
    fp = get_input("表达矩阵CSV路径", "expression.csv")
    gf = get_input("分组标签文件路径(留空=无分组)", "")
    mt = get_input("降维方法(PCA/tSNE/UMAP/all)", "all")
    ls = get_input("是否标注样本名(yes/no)", "no")
    cs = get_input("配色方案(default/Set2/tab10)", "default")
    run_dimred(fp, gf or None, mt, ls.lower() in ('yes','y'), cs)

if __name__ == "__main__": main()