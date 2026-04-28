#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  fasta-sequence-reverser
  FASTA序列取反向互补序列工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def reverse_complement(seq):
    """获取序列的反向互补"""
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 
                  'a': 't', 't': 'a', 'g': 'c', 'c': 'g',
                  'N': 'N', 'n': 'n'}
    return ''.join(complement.get(base, base) for base in reversed(seq.upper()))

def reverse_fasta(input_file, output="reversed.fasta", complement=True):
    """处理FASTA文件生成反向互补序列"""
    sequences = []
    current_id = ""
    current_seq = []
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_id:
                    seq = ''.join(current_seq)
                    if complement:
                        seq = reverse_complement(seq)
                    sequences.append((current_id, seq))
                current_id = line
                current_seq = []
            else:
                current_seq.append(line)
        
        if current_id:
            seq = ''.join(current_seq)
            if complement:
                seq = reverse_complement(seq)
            sequences.append((current_id, seq))
    
    with open(output, 'w') as f:
        for seq_id, seq in sequences:
            f.write(seq_id + "\n")
            for i in range(0, len(seq), 60):
                f.write(seq[i:i+60] + "\n")
    
    return len(sequences)

def main():
    print("\n" + "=" * 60)
    print("  FASTA序列反向互补工具")
    print("=" * 60)
    print("\n生成FASTA序列的反向互补序列")
    
    input_file = get_input("\n输入FASTA文件", "sequence.fasta", str)
    output = get_input("输出FASTA文件", "reversed.fasta", str)
    do_complement = get_input("是否取互补序列(yes/no)", "yes", str).lower() == "yes"
    
    count = reverse_fasta(input_file, output, do_complement)
    
    print(f"\n处理了 {count} 条序列")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
