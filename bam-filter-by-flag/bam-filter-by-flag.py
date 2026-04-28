#!/usr/bin/env python3
"""根据SAM flag过滤BAM文件中的reads"""

def main():
    input_bam = input("输入BAM文件路径 [input.bam]: ") or "input.bam"
    output_bam = input("输出BAM文件路径 [filtered.bam]: ") or "filtered.bam"
    exclude_flags = input("排除flag值(如1024=PCR重复) [1024]: ") or "1024"
    require_flags = input("要求flag值 [0]: ") or "0"
    min_mapq = input("最低MAPQ [0]: ") or "0"
    import pysam
    exc_f, req_f, min_mq = int(exclude_flags), int(require_flags), int(min_mapq)
    fin = pysam.AlignmentFile(input_bam, "rb")
    fout = pysam.AlignmentFile(output_bam, "wb", header=fin.header)
    kept = total = 0
    for r in fin:
        total += 1
        if r.flag & exc_f: continue
        if req_f and not (r.flag & req_f): continue
        if r.mapping_quality < min_mq: continue
        fout.write(r); kept += 1
    fin.close(); fout.close()
    print(f"过滤: {kept}/{total} reads ({kept/total*100:.1f}%)")


if __name__ == "__main__":
    main()
