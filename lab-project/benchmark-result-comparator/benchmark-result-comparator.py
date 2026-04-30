#!/usr/bin/env python3
"""基准测试结果比较与排名(多方法/多指标)"""

def main():
    input_file = input("基准结果CSV(方法,指标1,指标2,...) [benchmark.csv]: ") or "benchmark.csv"
    output_file = input("比较报告路径 [benchmark_report.txt]: ") or "benchmark_report.txt"
    higher_is_better = input("指标方向(逗号分隔,1=越高越好,0=越低越好) [1,1,0]: ") or "1,1,0"
    import pandas as pd
    df = pd.read_csv(input_file)
    methods = df.iloc[:, 0].tolist()
    metrics = df.columns[1:].tolist()
    dirs = [int(d) for d in higher_is_better.split(",")]
    while len(dirs) < len(metrics): dirs.append(1)
    report = ["=== 基准测试比较报告 ===", ""]
    report.append(f"方法数: {len(methods)}"); report.append(f"指标数: {len(metrics)}"); report.append("")
    # Rank each metric
    ranks = {}
    for i, m in enumerate(metrics):
        vals = df[m]
        if dirs[i] == 1:
            rank = vals.rank(ascending=False)
        else:
            rank = vals.rank(ascending=True)
        ranks[m] = rank
        best = df.iloc[0][0] if rank.iloc[0] == 1 else df.loc[rank.idxmin(), df.columns[0]]
        report.append(f"{m}: 最优={df.loc[rank.idxmin(), df.columns[0]]} (值={vals[rank.idxmin()]:.4f})")
    # Overall ranking
    total_rank = sum(ranks[m] for m in metrics)
    df["total_rank"] = total_rank
    df["avg_rank"] = total_rank / len(metrics)
    df_sorted = df.sort_values("avg_rank")
    report.append(""); report.append("=== 综合排名 ===")
    for i, (_, row) in enumerate(df_sorted.iterrows()):
        report.append(f"#{i+1}: {row.iloc[0]} (avg_rank={row['avg_rank']:.2f})")
    with open(output_file, "w") as out: out.write("\n".join(report))
    print(f"基准比较: {output_file}")


if __name__ == "__main__":
    main()
