#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  dna-structural-aligner
  DNA结构比对工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def structural_align(seq1, seq2, output="alignment.txt"):
    """DNA结构比对"""
    gc1 = sum(1 for c in seq1.upper() if c in 'GC') / len(seq1) if seq1 else 0
    gc2 = sum(1 for c in seq2.upper() if c in 'GC') / len(seq2) if seq2 else 0
    
    similarity = 1 - abs(gc1 - gc2)
    
    results = {
        "seq1_gc": gc1,
        "seq2_gc": gc2,
        "similarity": similarity,
        "seq1_length": len(seq1),
        "seq2_length": len(seq2)
    }
    
    with open(output, 'w') as f:
        f.write("DNA Structural Alignment Results\n")
        f.write("=" * 50 + "\n")
        for k, v in results.items():
            if isinstance(v, float):
                f.write(f"{k}: {v:.4f}\n")
            else:
                f.write(f"{k}: {v}\n")
    
    return results

def main():
    print("\n" + "=" * 60)
    print("  DNA结构比对工具")
    print("=" * 60)
    
    seq1 = get_input("\n序列1", "ATGCGATCGATCGATCG", str)
    seq2 = get_input("序列2", "ATGCGATCGATCGA", str)
    output = get_input("输出文件", "alignment.txt", str)
    
    results = structural_align(seq1, seq2, output)
    
    print("\n比对结果:")
    print(f"  序列1 GC%: {results['seq1_gc']:.2%}")
    print(f"  序列2 GC%: {results['seq2_gc']:.2%}")
    print(f"  相似度: {results['similarity']:.2%}")
    print(f"\n结果已保存到: {output}")

if __name__ == "__main__":
    main()
