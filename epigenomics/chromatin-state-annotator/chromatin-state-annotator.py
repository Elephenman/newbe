#!/usr/bin/env python3
"""ChromHMM/Segway染色质状态注释工具"""

def main():
    state_file = input("染色质状态BED路径 [chromatin_states.bed]: ") or "chromatin_states.bed"
    region_file = input("目标区域BED路径 [regions.bed]: ") or "regions.bed"
    output_file = input("输出注释路径 [annotated_regions.tsv]: ") or "annotated_regions.tsv"
    states = []
    with open(state_file) as f:
        for line in f:
            if line.startswith("#") or line.startswith("track"): continue
            p = line.strip().split("\t")
            if len(p) >= 4: states.append((p[0], int(p[1]), int(p[2]), p[3]))
    results = []
    with open(region_file) as f:
        for line in f:
            if line.startswith("#") or line.startswith("track"): continue
            p = line.strip().split("\t")
            if len(p) < 3: continue
            rc, rs, re = p[0], int(p[1]), int(p[2])
            rname = p[3] if len(p) > 3 else f"{rc}:{rs}-{re}"
            ov = {}
            for sc, ss, se, sn in states:
                if sc == rc and ss < re and se > rs:
                    overlap = min(se, re) - max(ss, rs)
                    ov[sn] = ov.get(sn, 0) + overlap
            total = sum(ov.values())
            dominant = max(ov, key=ov.get) if ov else "None"
            pct = ov.get(dominant, 0)/total*100 if total > 0 else 0
            results.append((rc, rs, re, rname, dominant, f"{pct:.1f}"))
    with open(output_file, "w") as out:
        out.write("Chrom\tStart\tEnd\tName\tState\tPct\n")
        for r in results: out.write("\t".join(str(x) for x in r)+"\n")
    print(f"染色质注释: {len(results)} 区域")


if __name__ == "__main__":
    main()
