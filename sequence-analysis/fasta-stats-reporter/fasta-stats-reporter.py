#!/usr/bin/env python3
"""统计FASTA文件中序列的长度、GC含量、N含量等"""

def main():
    input_fasta = input("输入FASTA文件路径 [input.fasta]: ") or "input.fasta"
    output_file = input("输出统计报告路径 [fasta_stats.txt]: ") or "fasta_stats.txt"
    seqs = {}; cur_id = None; cur_seq = []
    with open(input_fasta) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if cur_id: seqs[cur_id] = "".join(cur_seq)
                cur_id = line[1:].split()[0]; cur_seq = []
            else: cur_seq.append(line.upper())
    if cur_id: seqs[cur_id] = "".join(cur_seq)
    lens = [len(s) for s in seqs.values()]
    gcs = [(s.count("G")+s.count("C"))/len(s)*100 for s in seqs.values() if s]
    ns = sum(s.count("N") for s in seqs.values())
    with open(output_file, "w") as out:
        out.write(f"Total: {len(seqs)}\nLength: {sum(lens):,}\nAvg: {sum(lens)/len(lens):,.1f}\n")
        out.write(f"Min/Max: {min(lens):,}/{max(lens):,}\nGC: {sum(gcs)/len(gcs):.2f}%\nN: {ns:,}\n")
    print(f"统计报告: {output_file}")


if __name__ == "__main__":
    main()
