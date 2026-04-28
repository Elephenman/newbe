#!/usr/bin/env python3
"""根据质量值对FASTQ reads进行3'/5'端截尾修剪"""

def main():
    input_file = input("输入FASTQ文件路径 [input.fastq]: ") or "input.fastq"
    output_file = input("输出FASTQ文件路径 [trimmed.fastq]: ") or "trimmed.fastq"
    min_quality = input("最低质量阈值(Phred33) [20]: ") or "20"
    min_length = input("修剪后最短read长度 [30]: ") or "30"
    trim_end = input("修剪方向(3prime/5prime/both) [3prime]: ") or "3prime"
    min_qual = int(min_quality); min_len = int(min_length)
    kept = total = 0
    with open(input_file) as fin, open(output_file, "w") as fout:
        while True:
            header = fin.readline().strip()
            if not header: break
            seq = fin.readline().strip()
            plus = fin.readline().strip()
            qual_str = fin.readline().strip()
            total += 1
            quals = [ord(c) - 33 for c in qual_str]
            start, end = 0, len(quals)
            if trim_end in ("3prime", "both"):
                while end > start and quals[end-1] < min_qual: end -= 1
            if trim_end in ("5prime", "both"):
                while start < end and quals[start] < min_qual: start += 1
            ts, tq = seq[start:end], qual_str[start:end]
            if len(ts) >= min_len:
                fout.write(f"{header}\n{ts}\n{plus}\n{tq}\n"); kept += 1
    print(f"修剪完成: {kept}/{total} reads ({kept/total*100:.1f}%)")


if __name__ == "__main__":
    main()
