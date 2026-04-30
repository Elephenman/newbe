#!/usr/bin/env python3
"""基因组坐标系统转换(hg19->hg38等,基于chain文件)"""

def main():
    input_file = input("输入坐标BED路径 [coords_hg19.bed]: ") or "coords_hg19.bed"
    output_file = input("输出转换后BED路径 [coords_hg38.bed]: ") or "coords_hg38.bed"
    from_build = input("源基因组版本 [hg19]: ") or "hg19"
    to_build = input("目标基因组版本 [hg38]: ") or "hg38"
    # Simple coordinate mapping (placeholder for liftOver)
    # In production, use pyliftover or UCSC liftOver binary
    try:
        from pyliftover import LiftOver
        lo = LiftOver(from_build, to_build)
    except ImportError:
        print("提示: 安装pyliftover进行坐标转换(pip install pyliftover)")
        print("当前仅做格式转换,不执行坐标映射")
        with open(input_file) as fin, open(output_file, "w") as fout:
            for line in fin: fout.write(line)
        print(f"格式转换: {output_file}"); return
    results = []; converted = 0; failed = 0
    with open(input_file) as f:
        for line in f:
            if line.startswith("#") or line.startswith("track"): continue
            p = line.strip().split("\t")
            if len(p) < 3: continue
            chrom, start, end = p[0], int(p[1]), int(p[2])
            rest = p[3:] if len(p) > 3 else []
            new_start = lo.convert_coordinate(chrom, start)
            new_end = lo.convert_coordinate(chrom, end)
            if new_start and new_end and len(new_start) > 0 and len(new_end) > 0:
                results.append([new_start[0][0], new_start[0][1], new_end[0][1]] + rest)
                converted += 1
            else: failed += 1
    with open(output_file, "w") as out:
        for r in results: out.write("\t".join(str(x) for x in r)+"\n")
    print(f"坐标转换: {converted} 成功, {failed} 失败")


if __name__ == "__main__":
    main()
