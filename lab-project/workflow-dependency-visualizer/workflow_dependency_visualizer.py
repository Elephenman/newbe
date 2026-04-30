#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  workflow-dependency-visualizer
  分析流程依赖关系可视化工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def visualize_workflow(workflow_file, output="workflow_dag.png"):
    """可视化分析流程的DAG结构"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        steps = {
            "QC": (0.1, 0.8),
            "Trim": (0.25, 0.8),
            "Align": (0.4, 0.8),
            "Count": (0.55, 0.8),
            "DE": (0.7, 0.8),
            "Enrich": (0.85, 0.8),
            "Report": (0.7, 0.5)
        }
        
        edges = [
            ("QC", "Trim"), ("Trim", "Align"), ("Align", "Count"),
            ("Count", "DE"), ("DE", "Enrich"), ("DE", "Report"), ("Enrich", "Report")
        ]
        
        for step, (x, y) in steps.items():
            circle = plt.Circle((x, y), 0.05, color='steelblue', ec='black')
            ax.add_patch(circle)
            ax.text(x, y, step, ha='center', va='center', fontsize=9, fontweight='bold')
        
        for src, dst in edges:
            x1, y1 = steps[src]
            x2, y2 = steps[dst]
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0.3, 1)
        ax.axis('off')
        ax.set_title('Bioinformatics Workflow DAG', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"流程图已保存: {output}")
    except ImportError:
        print("matplotlib未安装")

def main():
    print("\n" + "=" * 60)
    print("  分析流程依赖可视化工具")
    print("=" * 60)
    
    workflow_file = get_input("\n流程配置文件", "workflow.txt", str)
    output = get_input("输出图片", "workflow_dag.png", str)
    
    visualize_workflow(workflow_file, output)
    print("\n完成!")

if __name__ == "__main__":
    main()
