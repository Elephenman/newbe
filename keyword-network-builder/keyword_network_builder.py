#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文献关键词共现网络构建"""
import os, sys
from collections import defaultdict
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def build_keyword_network(filepath, min_cooc=2, make_plot=True, layout="force"):
    try:
        import networkx as nx
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except: print("需要networkx+matplotlib"); return
    
    # 加载文献关键词
    papers = []
    with open(filepath, 'r') as f:
        header = f.readline()
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 2:
                kws = [k.strip() for k in fields[-1].split(';') if k.strip()]
                papers.append({"title": fields[0], "keywords": kws})
    
    # 共现矩阵
    cooc = defaultdict(int); kw_freq = defaultdict(int)
    for p in papers:
        for kw in p["keywords"]: kw_freq[kw] += 1
        for i, kw1 in enumerate(p["keywords"]):
            for kw2 in p["keywords"][i+1:]:
                pair = tuple(sorted([kw1, kw2]))
                cooc[pair] += 1
    
    # 构建网络
    G = nx.Graph()
    for kw, freq in kw_freq.items():
        G.add_node(kw, freq=freq)
    for pair, count in cooc.items():
        if count >= min_cooc:
            G.add_edge(pair[0], pair[1], weight=count)
    
    # 绘图
    if make_plot and len(G.nodes) > 0:
        plt.figure(figsize=(12, 10))
        if layout == "force":
            pos = nx.spring_layout(G, k=1.5/len(G.nodes)**0.5)
        else:
            pos = nx.circular_layout(G)
        
        node_sizes = [kw_freq[n]*100 for n in G.nodes]
        node_colors = list(range(len(G.nodes)))
        edge_widths = [cooc[tuple(sorted(e))]*0.5 for e in G.edges]
        
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.Set2, alpha=0.8)
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, edge_color='#888888')
        nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
        plt.title('关键词共现网络'); plt.axis('off'); plt.tight_layout()
        plt.savefig("keyword_network.png", dpi=300); plt.close()
        print("网络图: keyword_network.png")
    
    # 高频关键词排名
    top_kw = sorted(kw_freq.items(), key=lambda x: -x[1])[:20]
    print(f"\n关键词共现网络完成")
    print(f"  文献数: {len(papers)}")
    print(f"  关键词数: {len(kw_freq)}")
    print(f"  共现边数: {len(G.edges)}")
    print(f"  Top20关键词:")
    for kw, freq in top_kw: print(f"    {kw}: {freq}")
    
    # 保存
    with open("keyword_cooccurrence.csv", 'w') as out:
        out.write("keyword1,keyword2,cooccurrence\n")
        for pair, count in sorted(cooc.items(), key=lambda x: -x[1]):
            if count >= min_cooc: out.write(f"{pair[0]},{pair[1]},{count}\n")
    print("共现CSV: keyword_cooccurrence.csv")

def main():
    print("="*50); print("  关键词共现网络"); print("="*50)
    fp = get_input("文献列表文件(title+keywords TSV)", "papers.tsv")
    mc = get_input("最小共现次数", 2, int)
    mp = get_input("出网络图(yes/no)", "yes")
    la = get_input("布局(force/circular)", "force")
    build_keyword_network(fp, mc, mp.lower() in ('yes','y'), la)

if __name__ == "__main__": main()