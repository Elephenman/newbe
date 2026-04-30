#!/usr/bin/env python3
"""多QC报告汇总+综合评分"""

# 多QC报告汇总
import os
import pandas as pd

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


print("=" * 60)
print("  🧪 QC报告汇总器")
print("=" * 60)

qc_dir = get_input("QC报告目录路径", "qc_reports")
report_type = get_input("报告类型(fastqc/multiqc/custom)", "fastqc")
output_file = get_input("汇总报告路径", "qc_summary.tsv")
threshold = float(get_input("综合评分阈值", "80"))

qc_files = [f for f in os.listdir(qc_dir) if f.endswith(".txt") or f.endswith(".csv") or f.endswith(".tsv")]
print("✅ 找到 " + str(len(qc_files)) + " 个QC报告")

all_results = []

for qc_file in qc_files:
    path = os.path.join(qc_dir, qc_file)
    sep = "\t" if qc_file.endswith(".tsv") else ","
    
    try:
        df = pd.read_csv(path, sep=sep)
        sample_name = qc_file.replace(".txt", "").replace(".csv", "").replace(".tsv", "")
        
        metrics = {}
        col_map = {"total_reads": "total_reads", "Total Reads": "total_reads",
                   "q30_rate": "q30_rate", "Q30 Rate": "q30_rate",
                   "gc_content": "gc_content", "GC Content": "gc_content",
                   "duplication_rate": "duplication_rate", "Duplication Rate": "duplication_rate"}
        
        for col_name, metric_name in col_map.items():
            if col_name in df.columns:
                metrics[metric_name] = df[col_name].iloc[0]
        
        score = 100
        if "q30_rate" in metrics:
            score -= (1 - metrics["q30_rate"]) * 50
        if "duplication_rate" in metrics:
            score -= metrics["duplication_rate"] * 30
        
        metrics["composite_score"] = round(score, 1)
        metrics["pass_fail"] = "PASS" if score >= threshold else "FAIL"
        metrics["sample"] = sample_name
        
        all_results.append(metrics)
    except Exception as e:
        print("  ⚠️ 解析失败: " + qc_file + " - " + str(e))

result_df = pd.DataFrame(all_results)
if len(result_df) > 0:
    result_df = result_df.sort_values("composite_score", ascending=False)
    result_df.to_csv(output_file, sep="\t", index=False)
    
    passes = sum(1 for r in all_results if r.get("pass_fail") == "PASS")
    fails = len(all_results) - passes
    print("\n✅ 汇总完成: " + str(len(all_results)) + " 样本")
    print("  PASS: " + str(passes) + ", FAIL: " + str(fails))
print("📄 结果: " + output_file)
