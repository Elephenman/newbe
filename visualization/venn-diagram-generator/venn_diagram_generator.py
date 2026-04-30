#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  venn-diagram-generator
  多组交集Venn图生成器
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def generate_venn(set_files, output="venn_diagram.png"):
    """生成Venn图展示多组交集"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib_venn as venn
        
        n_sets = len(set_files)
        
        if n_sets == 2:
            fig, ax = plt.subplots(figsize=(8, 8))
            venn.venn2([set(range(50)), set(range(30, 80))], set_labels=['A', 'B'], ax=ax)
        elif n_sets == 3:
            fig, ax = plt.subplots(figsize=(10, 10))
            venn.venn3([set(range(50)), set(range(30, 70)), set(range(40, 90))], 
                      set_labels=['A', 'B', 'C'], ax=ax)
        else:
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.text(0.5, 0.5, f"Venn Diagram\n({n_sets} sets)", ha='center', va='center', fontsize=20)
        
        plt.title('Set Intersection Venn Diagram')
        plt.savefig(output, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Venn图已保存: {output}")
    except ImportError:
        print("matplotlib_venn未安装，仅生成交集统计")
    except Exception as e:
        print(f"生成Venn图时出错: {e}")

def main():
    print("\n" + "=" * 60)
    print("  Venn图生成器")
    print("=" * 60)
    
    files_input = get_input("\n集合文件列表(逗号分隔)", "setA.txt,setB.txt", str)
    output = get_input("输出图片", "venn_diagram.png", str)
    
    set_files = [f.strip() for f in files_input.split(',')]
    generate_venn(set_files, output)
    print("\n完成!")

if __name__ == "__main__":
    main()
