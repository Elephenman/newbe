#!/usr/bin/env python3
"""SANKEY流向图可视化
从CSV/TSV读取源-目标-权重数据，生成Sankey流向图
"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def parse_flow_data(filepath):
    """解析流向数据文件(source, target, value)"""
    flows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t') if '\t' in line else line.split(',')
            if len(parts) >= 3:
                try:
                    source = parts[0].strip()
                    target = parts[1].strip()
                    value = float(parts[2].strip())
                    flows.append((source, target, value))
                except ValueError:
                    continue
    return flows


def main():
    print("=" * 60)
    print("  Sankey流向图（数据通路/样本流转）")
    print("=" * 60)
    print()

    input_file = get_input("流向数据文件(CSV/TSV: source,target,value)", "flows.csv")
    output_file = get_input("输出图片路径", "sankey_flow.png")
    title = get_input("图表标题", "Sankey Flow Diagram")

    print()
    print(f"输入:    {input_file}")
    print(f"输出:    {output_file}")
    print(f"标题:    {title}")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] 输入文件不存在: {input_file}")
        sys.exit(1)

    # Parse flow data
    flows = parse_flow_data(input_file)
    if not flows:
        print("[ERROR] 未解析到有效的流向数据")
        sys.exit(1)

    print(f"[Processing] 找到 {len(flows)} 条流向记录")

    # Try plotly first, then matplotlib
    try:
        import plotly.graph_objects as go

        # Build node and link lists
        all_nodes = []
        for source, target, _ in flows:
            if source not in all_nodes:
                all_nodes.append(source)
            if target not in all_nodes:
                all_nodes.append(target)

        node_indices = {node: i for i, node in enumerate(all_nodes)}

        sources = [node_indices[s] for s, _, _ in flows]
        targets = [node_indices[t] for _, t, _ in flows]
        values = [v for _, _, v in flows]

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color="rgba(31, 119, 180, 0.8)"
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color="rgba(31, 119, 180, 0.3)"
            )
        )])
        fig.update_layout(title_text=title, font_size=12)
        fig.write_image(output_file)
        print(f"[Processing] Sankey图(Plotly): {output_file}")

    except ImportError:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            from matplotlib.sankey import Sankey

            # Simple Sankey with matplotlib
            # Aggregate flows
            flow_dict = {}
            for source, target, value in flows:
                key = (source, target)
                flow_dict[key] = flow_dict.get(key, 0) + value

            # Build label list and flows for matplotlib Sankey
            all_labels = list(dict.fromkeys([s for s, _, _ in flows] + [t for _, t, _ in flows]))

            fig, ax = plt.subplots(figsize=(12, 8))
            # Create a simple alluvial-style visualization
            y_pos = {}
            y_current = 0
            for label in all_labels:
                y_pos[label] = y_current
                y_current += 1

            # Draw flows as colored bands
            max_val = max(v for _, _, v in flows)
            for source, target, value in flows:
                y_s = y_pos[source]
                y_t = y_pos[target]
                width = value / max_val * 2
                ax.annotate("", xy=(1, y_t), xytext=(0, y_s),
                           arrowprops=dict(arrowstyle="-", color="steelblue",
                                          alpha=min(value / max_val + 0.2, 0.8),
                                          lw=width * 5))

            # Draw nodes
            for label, y in y_pos.items():
                out_total = sum(v for s, t, v in flows if s == label)
                in_total = sum(v for s, t, v in flows if t == label)
                total = max(out_total, in_total)
                box_w = 0.15
                box_h = total / max_val * 2 + 0.2
                rect = mpatches.FancyBboxPatch((-box_w/2, y - box_h/2), box_w, box_h,
                                                boxstyle="round,pad=0.05",
                                                facecolor="steelblue", edgecolor="navy")
                ax.add_patch(rect)
                ax.text(-0.3, y, label, ha='right', va='center', fontsize=9)
                ax.text(1.3, y, label, ha='left', va='center', fontsize=9, alpha=0.5)

            ax.set_xlim(-0.5, 1.5)
            ax.set_ylim(-1, len(all_labels))
            ax.axis('off')
            ax.set_title(title)
            plt.tight_layout()
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()
            print(f"[Processing] Sankey图(Matplotlib): {output_file}")

        except ImportError:
            # Fallback: generate HTML with mermaid-style text
            html_file = output_file.rsplit('.', 1)[0] + '.html'
            with open(html_file, 'w') as f:
                f.write(f'<html><head><title>{title}</title></head><body>\n')
                f.write(f'<h2>{title}</h2><pre>\n')
                f.write(f"{'Source':<20} {'Target':<20} {'Value':>10}\n")
                f.write('-' * 52 + '\n')
                for source, target, value in flows:
                    f.write(f'{source:<20} {target:<20} {value:>10.1f}\n')
                f.write('</pre></body></html>\n')
            print(f"[WARN] 无plotly/matplotlib，生成HTML: {html_file}")

    # Summary
    unique_sources = set(s for s, _, _ in flows)
    unique_targets = set(t for _, t, _ in flows)
    total_value = sum(v for _, _, v in flows)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  流向记录:     {len(flows)}")
    print(f"  源节点:       {len(unique_sources)}")
    print(f"  目标节点:     {len(unique_targets)}")
    print(f"  总流量:       {total_value:.1f}")
    print(f"  输出:         {output_file}")
    print("=" * 60)
    print()
    print("[Done] sankey_flow_visualizer completed successfully!")


if __name__ == "__main__":
    main()
