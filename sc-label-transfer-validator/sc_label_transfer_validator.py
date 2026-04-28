#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  sc-label-transfer-validator
  单细狍标签转移验证工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def validate_label_transfer(ref_labels, query_labels, output="transfer_validation.txt"):
    """验证标签转移的一致性"""
    import collections
    import random
    
    random.seed(42)
    
    cell_types = ["T_cells", "B_cells", "Macrophages", "NK_cells"]
    
    confusion = {ct: {ct2: 0 for ct2 in cell_types} for ct in cell_types}
    
    for i in range(min(len(ref_labels), len(query_labels))):
        if i < len(ref_labels) and i < len(query_labels):
            confusion[ref_labels[i]][query_labels[i]] += 1
    
    accuracy = 0
    for ct in cell_types:
        accuracy += confusion[ct][ct]
    accuracy /= sum(sum(confusion[ct].values()) for ct in cell_types)
    
    with open(output, 'w') as f:
        f.write("Label Transfer Validation\n")
        f.write("=" * 50 + "\n")
        f.write(f"Overall Accuracy: {accuracy:.2%}\n\n")
        f.write("Confusion Matrix:\n")
        f.write("\t" + "\t".join(cell_types) + "\n")
        for ct in cell_types:
            row = [str(confusion[ct][ct2]) for ct2 in cell_types]
            f.write(ct + "\t" + "\t".join(row) + "\n")
    
    return accuracy

def main():
    print("\n" + "=" * 60)
    print("  标签转移验证工具")
    print("=" * 60)
    
    ref_labels = get_input("\n参考标签文件", "ref_labels.txt", str)
    query_labels = get_input("查询标签文件", "query_labels.txt", str)
    output = get_input("输出文件", "transfer_validation.txt", str)
    
    accuracy = validate_label_transfer([], [], output)
    
    print(f"\n标签转移准确率: {accuracy:.2%}")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
