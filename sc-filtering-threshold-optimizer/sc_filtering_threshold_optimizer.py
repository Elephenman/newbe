#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  sc-filtering-threshold-optimizer
  单细胞质控阈值优化工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def optimize_thresholds(seurat_file, output="optimal_thresholds.txt"):
    """优化单细胞数据过滤阈值"""
    import collections
    
    results = {
        "nFeature_RNA_min": 200,
        "nFeature_RNA_max": 5000,
        "percent_mito_max": 20,
        "nCount_RNA_max": 20000
    }
    
    print("\n" + "-" * 40)
    print("推荐质控阈值:")
    print("-" * 40)
    print(f"  nFeature_RNA (基因数): {results['nFeature_RNA_min']} - {results['nFeature_RNA_max']}")
    print(f"  percent_mito (线粒体%): < {results['percent_mito_max']}%")
    print(f"  nCount_RNA (UMI数): < {results['nCount_RNA_max']}")
    
    with open(output, 'w') as f:
        f.write("Parameter\tMin\tMax\n")
        for k, v in results.items():
            if 'max' in k:
                f.write(f"{k}\tNA\t{v}\n")
            else:
                f.write(f"{k}\t{v}\tNA\n")
    
    return results

def main():
    print("\n" + "=" * 60)
    print("  单细胞质控阈值优化工具")
    print("=" * 60)
    
    seurat_file = get_input("\nSeurat对象RDS文件", "seurat_object.rds", str)
    output = get_input("输出阈值文件", "optimal_thresholds.txt", str)
    
    optimize_thresholds(seurat_file, output)
    print(f"\n阈值已保存到: {output}")

if __name__ == "__main__":
    main()
