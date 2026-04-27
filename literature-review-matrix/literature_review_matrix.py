#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文献综述矩阵自动生成器"""
import os, sys
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def build_review_matrix(filepath, dimensions="method,findings,limitations,year", make_table=True):
    try: import pandas as pd
    except: print("需要pandas"); return
    
    # 加载文献数据
    df = pd.read_csv(filepath)
    dims = dimensions.split(',')
    
    # 构建矩阵
    matrix = pd.DataFrame()
    matrix['title'] = df.iloc[:,0] if 'title' in df.columns else df.columns[0]
    
    for dim in dims:
        dim = dim.strip()
        if dim in df.columns:
            matrix[dim] = df[dim]
        else:
            # 自动搜索可能的列名
            candidates = [c for c in df.columns if dim.lower() in c.lower()]
            if candidates:
                matrix[dim] = df[candidates[0]]
            else:
                matrix[dim] = ['' for _ in range(len(df))]
                print(f"  维度'{dim}'未找到匹配列，已创建空列")
    
    # 标记缺失字段
    empty_counts = {}
    for col in matrix.columns:
        empty_counts[col] = matrix[col].isna().sum() + (matrix[col] == '').sum()
    
    # 输出
    print(f"\n文献综述矩阵完成")
    print(f"  文献数: {len(matrix)}")
    print(f"  维度数: {len(matrix.columns)}")
    print(f"  缺失字段统计:")
    for col, cnt in empty_counts.items():
        if cnt > 0: print(f"    {col}: {cnt} 篇缺失 ⚠️")
    
    # 保存CSV
    matrix.to_csv("literature_review_matrix.csv", index=False)
    print("矩阵CSV: literature_review_matrix.csv")
    
    # 可选HTML表格
    if make_table:
        try:
            import matplotlib; matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            
            # 简化热图：每个维度每篇文献有/无内容
            heatmap_data = []
            for col in dims:
                row = []
                for i in range(len(matrix)):
                    val = matrix.iloc[i].get(col, '')
                    row.append(1 if val and val != '' else 0)
                heatmap_data.append(row)
            
            plt.figure(figsize=(max(10, len(matrix)*0.5), max(6, len(dims)*0.8)))
            plt.imshow(heatmap_data, cmap='RdYlGn', aspect='auto')
            plt.yticks(range(len(dims)), dims)
            plt.xticks(range(len(matrix)), [str(i+1) for i in range(len(matrix))])
            plt.title('文献综述矩阵 - 内容覆盖度')
            plt.colorbar(label='有内容=1/缺失=0')
            plt.tight_layout()
            plt.savefig("review_matrix_heatmap.png", dpi=300); plt.close()
            print("覆盖度热图: review_matrix_heatmap.png")
        except: pass

def main():
    print("="*50); print("  文献综述矩阵"); print("="*50)
    fp = get_input("文献数据CSV路径", "papers.csv")
    dm = get_input("矩阵维度(逗号分隔)", "method,findings,limitations,year")
    mt = get_input("是否出表格图(yes/no)", "yes")
    build_review_matrix(fp, dm, mt.lower() in ('yes','y'))

if __name__ == "__main__": main()