#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  vcf-maf-distribution-plotter
  VCF等位基因频率分布可视化
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def plot_maf_distribution(vcf_file, output="maf_distribution.png", bins=50):
    """绘制MAF分布图"""
    import collections
    
    af_values = []
    
    try:
        import pysam
        vcf = pysam.VariantFile(vcf_file)
        for rec in vcf.fetch():
            for sample in rec.samples:
                gt = rec.samples[sample]["GT"]
                if gt is not None and all(g is not None for g in gt):
                    allele_count = sum(1 for g in gt if g > 0)
                    max_alleles = max(gt) if gt else 0
                    if rec.alts:
                        try:
                            ad = rec.samples[sample].get("AD", [0, 0])
                            if isinstance(ad, list) and len(ad) > 1:
                                total = sum(ad)
                                alt_freq = ad[1] / total if total > 0 else 0
                                af_values.append(alt_freq)
                        except:
                            pass
        vcf.close()
    except Exception as e:
        print(f"解析VCF时出错: {e}")
    
    if not af_values:
        af_values = [0.1, 0.2, 0.3, 0.5, 0.15, 0.25, 0.35, 0.45]
        print("使用示例数据生成图表")
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(af_values, bins=bins, edgecolor='black', alpha=0.7, color='steelblue')
        ax.set_xlabel('Allele Frequency', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Variant Allele Frequency Distribution', fontsize=14)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()
        print(f"图表已保存: {output}")
    except ImportError:
        print("matplotlib未安装，仅输出统计信息")
        counter = collections.Counter([round(x, 2) for x in af_values])
        print("频率分布:", dict(counter))

def main():
    print("\n" + "=" * 60)
    print("  VCF等位基因频率分布可视化")
    print("=" * 60)
    
    vcf_file = get_input("\nVCF文件路径", "variants.vcf", str)
    output = get_input("输出图片", "maf_distribution.png", str)
    bins = get_input("直方图bins数", 50, int)
    
    plot_maf_distribution(vcf_file, output, bins)
    print("\n完成!")

if __name__ == "__main__":
    main()
