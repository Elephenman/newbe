#!/usr/bin/env python3
"""统一基因ID格式(去除版本号/Ensembl转Symbol等)"""

def main():
    input_file = input("输入基因列表(每行一个) [gene_list.txt]: ") or "gene_list.txt"
    output_file = input("标准化输出路径 [normalized_genes.txt]: ") or "normalized_genes.txt"
    input_type = input("输入ID类型(ensembl/entrez/symbol) [ensembl]: ") or "ensembl"
    output_type = input("输出ID类型(symbol/ensembl/entrez) [symbol]: ") or "symbol"
    with open(input_file) as f: genes = [l.strip() for l in f if l.strip()]
    norm = []
    for g in genes:
        if input_type == "ensembl": g = g.split(".")[0]
        norm.append(g)
    with open(output_file, "w") as out:
        for g in norm: out.write(g + "\n")
    print(f"标准化: {len(norm)} 基因ID -> {output_file}")
    if input_type == "ensembl" and output_type == "symbol":
        print("提示: 完整Ensembl->Symbol映射需mygene包")


if __name__ == "__main__":
    main()
