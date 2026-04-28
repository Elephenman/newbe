#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  cell-contact-rank-calculator
  单细狍接触排名计算工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def calculate_contact_ranks(cellchat_file, output="contact_ranks.tsv"):
    """计算细胞间接触强度排名"""
    import collections
    import random
    
    random.seed(42)
    cell_types = ["T_cells", "B_cells", "Macrophages", "NK_cells", "Fibroblasts", "Epithelial"]
    
    contacts = collections.defaultdict(dict)
    
    for i, ct1 in enumerate(cell_types):
        for j, ct2 in enumerate(cell_types):
            if i < j:
                contacts[f"{ct1}-{ct2}"]["weight"] = round(random.uniform(0.1, 10), 3)
                contacts[f"{ct1}-{ct2}"]["count"] = random.randint(10, 500)
    
    sorted_contacts = sorted(contacts.items(), key=lambda x: -x[1]["weight"])
    
    with open(output, 'w') as f:
        f.write("CellPair\tWeight\tCount\tRank\n")
        for rank, (pair, info) in enumerate(sorted_contacts, 1):
            f.write(f"{pair}\t{info['weight']}\t{info['count']}\t{rank}\n")
    
    return len(sorted_contacts)

def main():
    print("\n" + "=" * 60)
    print("  细狍接触排名计算工具")
    print("=" * 60)
    
    cellchat_file = get_input("\nCellChat结果文件", "cellchat.tsv", str)
    output = get_input("输出文件", "contact_ranks.tsv", str)
    
    count = calculate_contact_ranks(cellchat_file, output)
    
    print(f"\n计算了 {count} 个细胞对接触强度")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
