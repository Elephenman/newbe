#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  fastq-interleave-splitter
  FASTQ成对交叉/解交叉工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def interleave_fastq(r1_file, r2_file, output="interleaved.fastq"):
    """交叉合并两个FASTQ文件"""
    try:
        import gzip
        r1_open = gzip.open if r1_file.endswith('.gz') else open
        r2_open = gzip.open if r2_file.endswith('.gz') else open
        
        count = 0
        with r1_open(r1_file, 'rt') as f1, r2_open(r2_file, 'rt') as f2, \
             open(output, 'w') as out:
            while True:
                h1 = f1.readline()
                h2 = f2.readline()
                if not h1 or not h2:
                    break
                s1 = f1.readline()
                s2 = f2.readline()
                p1 = f1.readline()
                p2 = f2.readline()
                q1 = f1.readline()
                q2 = f2.readline()
                
                out.write(h1 + s1 + p1 + q1)
                out.write(h2 + s2 + p2 + q2)
                count += 1
                
                if count >= 10000:
                    print(f"  已处理 {count} read pairs...")
        
        return count
    except Exception as e:
        print(f"错误: {e}")
        return 0

def main():
    print("\n" + "=" * 60)
    print("  FASTQ交叉合并工具")
    print("=" * 60)
    
    r1_file = get_input("\nRead1 FASTQ", "sample_R1.fastq.gz", str)
    r2_file = get_input("Read2 FASTQ", "sample_R2.fastq.gz", str)
    output = get_input("输出交叉文件", "interleaved.fastq", str)
    
    count = interleave_fastq(r1_file, r2_file, output)
    print(f"\n已交叉合并 {count} read pairs")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
