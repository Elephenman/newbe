#!/usr/bin/env python3
"""实验设计检查器(样本量/重复/对照完整性)"""

def main():
    input_file = input("实验设计CSV路径(样本,组,重复,处理) [design.csv]: ") or "design.csv"
    output_file = input("输出检查报告路径 [design_check.txt]: ") or "design_check.txt"
    import pandas as pd
    df = pd.read_csv(input_file)
    issues = []
    checks = []
    # Check required columns
    req_cols = ["sample", "group"]
    for c in req_cols:
        if c not in df.columns: issues.append(f"缺少必要列: {c}")
    if issues:
        with open(output_file, "w") as out:
            out.write("\n".join(issues))
        print("设计检查失败"); return
    # Check replicates
    rep_counts = df["group"].value_counts()
    min_rep = rep_counts.min()
    if min_rep < 3: issues.append(f"警告: 组 {rep_counts[rep_counts==min_rep].index[0]} 仅{min_rep}个重复(建议>=3)")
    else: checks.append(f"重复数: {min_rep}-{rep_counts.max()} (OK)")
    # Check control group
    if "control" not in df["group"].str.lower().values and "ctrl" not in df["group"].str.lower().values:
        issues.append("警告: 未检测到对照组(control/ctrl)")
    else: checks.append("对照组: 已检测")
    # Check balanced design
    if rep_counts.nunique() > 1:
        issues.append(f"非平衡设计: 组大小 {rep_counts.to_dict()}")
    else: checks.append("平衡设计: OK")
    with open(output_file, "w") as out:
        out.write("=== 实验设计检查 ===\n")
        out.write(f"总样本数: {len(df)}\n组数: {len(rep_counts)}\n")
        out.write("\n--- 检查通过 ---\n" + "\n".join(checks) + "\n")
        if issues: out.write("\n--- 问题 ---\n" + "\n".join(issues) + "\n")
    print(f"设计检查: {len(checks)} 通过, {len(issues)} 问题")


if __name__ == "__main__":
    main()
