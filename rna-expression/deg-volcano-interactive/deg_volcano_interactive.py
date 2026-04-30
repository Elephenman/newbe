#!/usr/bin/env python3
"""Interactive volcano plot (Plotly click-to-view gene info)"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def create_interactive_volcano(deg_file, output_file, log2fc_col="log2FoldChange",
                                padj_col="padj", gene_col="gene",
                                log2fc_threshold=1.0, padj_threshold=0.05):
    """Create an interactive volcano plot using Plotly."""
    try:
        import pandas as pd
        import plotly.express as px
    except ImportError:
        print("[ERROR] pandas and plotly are required: pip install pandas plotly")
        sys.exit(1)

    # Read DEG results
    df = pd.read_csv(deg_file)

    # Resolve column names with common aliases
    col_aliases = {
        log2fc_col: ["log2FoldChange", "logFC", "log2FC", "FC"],
        padj_col: ["padj", "p_adj", "adj.P.Val", "FDR", "padjust"],
        gene_col: ["gene", "gene_id", "symbol", "rowname", "Gene"],
    }

    resolved = {}
    for target, aliases in col_aliases.items():
        for alias in aliases:
            if alias in df.columns:
                resolved[target] = alias
                break

    log2fc_col = resolved.get(log2fc_col, log2fc_col)
    padj_col = resolved.get(padj_col, padj_col)
    gene_col = resolved.get(gene_col, gene_col)

    # If gene column is rowname, create it from index
    if gene_col not in df.columns:
        df[gene_col] = df.index.astype(str)

    # Validate required columns
    for col_name, col_key in [("log2FoldChange", log2fc_col), ("padj", padj_col)]:
        if col_key not in df.columns:
            print(f"[ERROR] Column '{col_key}' not found. Available: {list(df.columns)}")
            sys.exit(1)

    # Classify genes
    df["neg_log10_padj"] = -df[padj_col].apply(lambda x: -1 if x <= 0 else __import__('math').log10(x) * -1 if x > 0 else 0)
    # More robust: handle edge cases
    import math
    df["neg_log10_padj"] = df[padj_col].apply(
        lambda x: -math.log10(x) if x > 0 else 300
    )

    df["category"] = "Not Significant"
    df.loc[(df[log2fc_col] >= log2fc_threshold) & (df[padj_col] < padj_threshold), "category"] = "Up"
    df.loc[(df[log2fc_col] <= -log2fc_threshold) & (df[padj_col] < padj_threshold), "category"] = "Down"

    up_count = (df["category"] == "Up").sum()
    down_count = (df["category"] == "Down").sum()
    ns_count = (df["category"] == "Not Significant").sum()

    # Create interactive plot
    color_map = {"Up": "#E64B35", "Down": "#4DBBD5", "Not Significant": "#AAAAAA"}

    fig = px.scatter(
        df, x=log2fc_col, y="neg_log10_padj",
        color="category", color_discrete_map=color_map,
        hover_name=gene_col,
        hover_data={gene_col: True, log2fc_col: ":.3f", padj_col: ":.2e"},
        title=f"Volcano Plot (Up: {up_count}, Down: {down_count})",
        labels={log2fc_col: "log2(Fold Change)", "neg_log10_padj": "-log10(adj p-value)"},
        opacity=0.6,
    )

    # Add threshold lines
    fig.add_hline(y=-math.log10(padj_threshold), line_dash="dash", line_color="grey",
                  annotation_text=f"padj={padj_threshold}")
    fig.add_vline(x=log2fc_threshold, line_dash="dash", line_color="grey",
                  annotation_text=f"log2FC={log2fc_threshold}")
    fig.add_vline(x=-log2fc_threshold, line_dash="dash", line_color="grey",
                  annotation_text=f"log2FC=-{log2fc_threshold}")

    fig.update_layout(width=1000, height=700)

    # Save as HTML
    fig.write_html(output_file)

    return {
        "up": up_count,
        "down": down_count,
        "not_sig": ns_count,
    }


def main():
    print("=" * 60)
    print("  Interactive Volcano Plot (Plotly)")
    print("=" * 60)
    print()

    input_file = get_input("DEG results CSV path", "deg_results.csv")
    output_file = get_input("Output HTML path", "volcano_interactive.html")
    log2fc_thresh = get_input("log2FC threshold", "1.0", float)
    padj_thresh = get_input("padj threshold", "0.05", float)
    gene_col = get_input("Gene column name", "gene")

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    stats = create_interactive_volcano(
        input_file, output_file,
        log2fc_threshold=log2fc_thresh,
        padj_threshold=padj_thresh,
        gene_col=gene_col,
    )

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Up-regulated:     {stats['up']}")
    print(f"  Down-regulated:   {stats['down']}")
    print(f"  Not significant:  {stats['not_sig']}")
    print(f"  Output saved to:  {output_file}")
    print("=" * 60)
    print()
    print("[Done] Interactive volcano plot created successfully!")


if __name__ == "__main__":
    main()
