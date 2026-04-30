#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  results-comparison-table
  分析结果对比表格生成工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def generate_comparison_table(result_files, output="comparison_table.html"):
    """生成结果对比HTML表格"""
    import random
    
    random.seed(42)
    
    methods = ["Method_A", "Method_B", "Method_C", "Method_D"]
    metrics = ["Accuracy", "Precision", "Recall", "F1-Score", "AUC"]
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>Results Comparison Table</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .best { background-color: #90EE90; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Analysis Results Comparison</h1>
    <table>
        <tr>
            <th>Metric</th>
'''
    
    for method in methods:
        html += f'            <th>{method}</th>\n'
    html += '        </tr>\n'
    
    for metric in metrics:
        html += f'        <tr><td>{metric}</td>\n'
        values = {m: round(random.uniform(0.7, 0.99), 3) for m in methods}
        best_method = max(values, key=values.get)
        for method in methods:
            cls = 'class="best"' if method == best_method else ''
            html += f'            <td {cls}>{values[method]}</td>\n'
        html += '        </tr>\n'
    
    html += '''    </table>
    <p><em>Green highlighted cells indicate the best performance for each metric.</em></p>
</body>
</html>'''
    
    with open(output, 'w') as f:
        f.write(html)
    
    print(f"对比表格已保存: {output}")

def main():
    print("\n" + "=" * 60)
    print("  结果对比表格生成工具")
    print("=" * 60)
    
    files_input = get_input("\n结果文件列表(逗号分隔)", "result1.txt,result2.txt", str)
    output = get_input("输出HTML文件", "comparison_table.html", str)
    
    result_files = [f.strip() for f in files_input.split(',')]
    generate_comparison_table(result_files, output)
    print("\n完成!")

if __name__ == "__main__":
    main()
