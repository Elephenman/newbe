#!/usr/bin/env python3
"""从STAR-Fusion/Arriba输出中筛选基因融合事件"""

def main():
    input_file = input("融合检测结果路径 [fusions.tsv]: ") or "fusions.tsv"
    output_file = input("筛选输出路径 [filtered_fusions.tsv]: ") or "filtered_fusions.tsv"
    min_junction = input("最低junction reads [3]: ") or "3"
    tool = input("工具格式(star_fusion/arriba) [star_fusion]: ") or "star_fusion"
    min_jr = int(min_junction); filtered = []; header = None
    with open(input_file) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if header is None: header = p; continue
            if tool == "star_fusion" and len(p) > 10:
                jr = int(p[5]) if p[5].isdigit() else 0
            elif tool == "arriba" and len(p) > 6:
                jr = int(p[5].split("/")[0]) if "/" in p[5] and p[5].split("/")[0].isdigit() else 0
            else: jr = 0
            if jr >= min_jr: filtered.append(p)
    with open(output_file, "w") as out:
        if header: out.write("\t".join(header)+"\n")
        for r in filtered: out.write("\t".join(r)+"\n")
    print(f"融合筛选: {len(filtered)} 个事件")


if __name__ == "__main__":
    main()
