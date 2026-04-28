#!/usr/bin/env python3
"""生信分析流程文档自动生成器"""

def main():
    input_file = input("流程脚本路径(.py/.R/.sh) [pipeline.py]: ") or "pipeline.py"
    output_file = input("输出文档路径 [pipeline_doc.md]: ") or "pipeline_doc.md"
    title = input("文档标题 [Analysis Pipeline]: ") or "Analysis Pipeline"
    import re
    with open(input_file) as f: content = f.read()
    lines = content.split("\n")
    doc = [f"# {title}", "", "## 概述", f"脚本: {input_file}", f"总行数: {len(lines)}", ""]
    # Extract imports
    imports = [l.strip() for l in lines if l.strip().startswith("import ") or l.strip().startswith("library(")]
    if imports:
        doc.append("## 依赖"); doc.append("```"); doc.extend(imports); doc.append("```"); doc.append("")
    # Extract functions
    funcs = [(i+1, l.strip()) for i, l in enumerate(lines) if l.strip().startswith("def ") or l.strip().startswith("function(")]
    if funcs:
        doc.append("## 函数"); doc.append("| 行号 | 函数 |"); doc.append("|------|------|")
        for ln, fn in funcs: doc.append(f"| {ln} | `{fn}` |")
        doc.append("")
    # Extract comments
    comments = [(i+1, l.strip()) for i, l in enumerate(lines) if l.strip().startswith("#") and not l.strip().startswith("#!")]
    if comments:
        doc.append("## 注释摘要"); doc.append("```")
        for ln, c in comments[:30]: doc.append(f"L{ln}: {c}")
        doc.append("```"); doc.append("")
    doc.append("## 自动生成"); doc.append(f"由 bioinformatics-pipeline-doc 从 {input_file} 生成")
    with open(output_file, "w") as out: out.write("\n".join(doc))
    print(f"文档已生成: {output_file}")


if __name__ == "__main__":
    main()
