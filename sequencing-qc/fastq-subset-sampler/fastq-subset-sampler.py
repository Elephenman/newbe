#!/usr/bin/env python3
"""从FASTQ文件中随机采样指定数量或比例的reads"""

def main():
    input_file = input("输入FASTQ文件路径 [input.fastq]: ") or "input.fastq"
    output_file = input("输出FASTQ路径 [sampled.fastq]: ") or "sampled.fastq"
    sample_type = input("采样方式(count/ratio) [ratio]: ") or "ratio"
    sample_value = input("采样数量或比例 [0.1]: ") or "0.1"
    seed = input("随机种子 [42]: ") or "42"
    import random; random.seed(int(seed))
    recs = []
    with open(input_file) as f:
        while True:
            h = f.readline()
            if not h: break
            s, p, q = f.readline(), f.readline(), f.readline()
            recs.append((h, s, p, q))
    total = len(recs)
    n = min(int(sample_value), total) if sample_type == "count" else max(1, int(total*float(sample_value)))
    sampled = random.sample(recs, n)
    with open(output_file, "w") as out:
        for r in sampled: out.write(r[0]+r[1]+r[2]+r[3])
    print(f"采样: {n}/{total} reads ({n/total*100:.1f}%)")


if __name__ == "__main__":
    main()
