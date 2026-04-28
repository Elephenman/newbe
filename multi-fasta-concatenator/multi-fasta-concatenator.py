#!/usr/bin/env python3
"""将多个FASTA文件合并为一个，添加文件名前缀避免ID冲突"""

def main():
    input_dir = input("输入FASTA目录 [.]: ") or "."
    output_file = input("合并输出FASTA路径 [concatenated.fa]: ") or "concatenated.fa"
    add_prefix = input("添加文件名前缀(yes/no) [yes]: ") or "yes"
    pattern = input("文件匹配模式 [*.fasta]: ") or "*.fasta"
    import glob
    files = sorted(glob.glob(os.path.join(input_dir, pattern)))
    if not files: print(f"未找到 {pattern}"); return
    total = 0
    with open(output_file, "w") as out:
        for fp in files:
            pfx = os.path.splitext(os.path.basename(fp))[0] if add_prefix == "yes" else ""
            cnt = 0
            with open(fp) as fin:
                for line in fin:
                    if line.startswith(">"):
                        cnt += 1
                        if pfx: line = f">{pfx}_{line[1:]}"
                    out.write(line)
            total += cnt
    print(f"合并: {len(files)} files, {total} seqs -> {output_file}")


if __name__ == "__main__":
    main()
