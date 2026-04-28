#!/usr/bin/env python3
"""根据FASTQ和基因组大小计算测序深度"""

def main():
    input_file = input("输入FASTQ文件路径 [input.fastq]: ") or "input.fastq"
    genome_size = input("基因组大小(bp) [3000000000]: ") or "3000000000"
    read_length = input("平均read长度(bp) [150]: ") or "150"
    gs = int(genome_size); tb = rc = 0
    with open(input_file) as f:
        ln = 0
        for line in f:
            ln += 1
            if ln % 4 == 2: tb += len(line.strip()); rc += 1
    depth = tb / gs
    with open("depth_report.txt","w") as out:
        out.write(f"Reads: {rc:,}\nBases: {tb:,}\nDepth: {depth:.2f}X\n")
    print(f"测序深度: {depth:.2f}X")


if __name__ == "__main__":
    main()
