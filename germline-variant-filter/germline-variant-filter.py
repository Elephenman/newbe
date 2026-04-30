#!/usr/bin/env python3
"""胚系变异过滤与分类(Pathogenic/Likely Pathogenic/Benign等)"""

def main():
    input_vcf = input("输入VCF文件路径 [germline.vcf]: ") or "germline.vcf"
    output_file = input("过滤后VCF输出路径 [filtered_germline.vcf]: ") or "filtered_germline.vcf"
    min_qual = input("最低QUAL值 [30]: ") or "30"
    min_depth = input("最低DP [10]: ") or "10"
    af_threshold = input("等位基因频率阈值(0=不过滤) [0]: ") or "0"
    min_q = float(min_qual); min_dp = int(min_depth); af_thr = float(af_threshold)
    kept = total = 0
    with open(input_vcf) as fin, open(output_file, "w") as fout:
        for line in fin:
            if line.startswith("#"): fout.write(line); continue
            parts = line.strip().split("\t")
            if len(parts) < 8: continue
            total += 1
            try: qual = float(parts[5]) if parts[5] != "." else 0
            except: qual = 0
            info = dict(it.split("=",1) if "=" in it else (it,"T") for it in parts[7].split(";"))
            dp = int(info.get("DP","0"))
            af_str = info.get("AF", "0")
            try: af = float(af_str.split(",")[0])
            except ValueError: af = 0.0
            if qual < min_q or dp < min_dp: continue
            if af_thr > 0 and af > af_thr: continue
            fout.write(line); kept += 1
    print(f"胚系过滤: {kept}/{total} 变异保留")


if __name__ == "__main__":
    main()
