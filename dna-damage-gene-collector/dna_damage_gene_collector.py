#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA损伤修复相关基因集收集器
🔥 针对陆慧智课题组（DNA损伤修复方向）

功能：
- 预置7大修复通路基因字典（HR/NHEJ/BER/MMR/SSB/FA/p53）
- 支持多通路选择和交叉分析
- 可选PubMed API补充搜索
- 输出CSV(符号+Ensembl) + Venn交叉图 + 基因功能简述
"""

import os
import sys
from collections import defaultdict

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib_venn import venn2, venn3
    HAS_VENN = True
except ImportError:
    HAS_VENN = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "":
        return default
    try:
        return type(val)
    except (ValueError, TypeError):
        print(f"  ⚠ 输入格式错误，使用默认值: {default}")
        return default


# ========== 预置修复通路基因库 ==========

PATHWAY_GENES = {
    "HR": {
        "name": "同源重组 (Homologous Recombination)",
        "description": "利用同源模板精确修复DNA双链断裂",
        "human": {
            "BRCA1": {"symbol": "BRCA1", "ensembl": "ENSG00000012048", "function": "双链断裂识别与修复启动，肿瘤抑制基因"},
            "BRCA2": {"symbol": "BRCA2", "ensembl": "ENSG00000139618", "function": "Rad51加载介导，同源重组核心"},
            "RAD51": {"symbol": "RAD51", "ensembl": "ENSG00000051180", "function": "同源搜索与链交换，重组核心酶"},
            "RAD51B": {"symbol": "RAD51B", "ensembl": "ENSG00000108384", "function": "Rad51旁系同源基因，重组辅助"},
            "RAD51C": {"symbol": "RAD51C", "ensembl": "ENSG00000108387", "function": "Rad51旁系同源基因，重组辅助"},
            "RAD51D": {"symbol": "RAD51D", "ensembl": "ENSG00000108390", "function": "Rad51旁系同源基因，重组辅助"},
            "PALB2": {"symbol": "PALB2", "ensembl": "ENSG00000083093", "function": "BRCA1-BRCA2桥接蛋白，重组支架"},
            "XRCC2": {"symbol": "XRCC2", "ensembl": "ENSG00000164690", "function": "Rad51旁系同源基因，重组辅助"},
            "XRCC3": {"symbol": "XRCC3", "ensembl": "ENSG00000164695", "function": "Rad51旁系同源基因，重组辅助"},
            "DMC1": {"symbol": "DMC1", "ensembl": "ENSG00000120694", "function": "减数分裂特异性Rad51同源物"},
            "RPA1": {"symbol": "RPA1", "ensembl": "ENSG00000132383", "function": "单链DNA结合蛋白，稳定重组中间体"},
            "RPA2": {"symbol": "RPA2", "ensembl": "ENSG00000132386", "function": "单链DNA结合蛋白亚基"},
            "MRN_complex": {"symbol": "MRE11", "ensembl": "ENSG00000020922", "function": "MRN复合物核酸酶，断裂末端处理"},
            "NBS1": {"symbol": "NBN", "ensembl": "ENSG00000104320", "function": "MRN复合物调控亚基"},
            "RAD50": {"symbol": "RAD50", "ensembl": "ENSG00000120885", "function": "MRN复合物支架蛋白"},
            "ATM": {"symbol": "ATM", "ensembl": "ENSG00000182434", "function": "双链断裂信号激酶，磷酸化HR因子"},
            "ATR": {"symbol": "ATR", "ensembl": "ENSG00000175054", "function": "复制应激响应激酶"},
            "CHEK2": {"symbol": "CHEK2", "ensembl": "ENSG00000183765", "function": "ATM下游激酶，检查点激活"},
            "BLM": {"symbol": "BLM", "ensembl": "ENSG00000197299", "function": "RecQ解旋酶，防止异常重组"},
            "WRN": {"symbol": "WRN", "ensembl": "ENSG00000165995", "function": "RecQ解旋酶，HR辅助"},
        },
    },
    "NHEJ": {
        "name": "非同源末端连接 (Non-Homologous End Joining)",
        "description": "无需模板直接连接DNA双链断裂末端（易出错）",
        "human": {
            "KU70": {"symbol": "XRCC6", "ensembl": "ENSG00000196419", "function": "Ku70，DNA末端识别与结合"},
            "KU80": {"symbol": "XRCC5", "ensembl": "ENSG00000125974", "function": "Ku80，DNA末端识别与结合"},
            "DNA_PKcs": {"symbol": "PRKDC", "ensembl": "ENSG00000253729", "function": "DNA-PK催化亚基，NHEJ核心激酶"},
            "XRCC4": {"symbol": "XRCC4", "ensembl": "ENSG00000182307", "function": "连接酶IV辅助因子"},
            "LIG4": {"symbol": "LIG4", "ensembl": "ENSG00000116256", "function": "DNA连接酶IV，末端连接"},
            "XLF": {"symbol": "NHEJ1", "ensembl": "ENSG00000136457", "function": "XRCC4样因子，连接辅助"},
            "PAXX": {"symbol": "PAXX", "ensembl": "ENSG00000175329", "function": "Paralogue of XRCC4 and XLF"},
            "Artemis": {"symbol": "DCLRE1C", "ensembl": "ENSG00000152422", "function": "核酸酶，末端处理"},
            "PNKP": {"symbol": "PNKP", "ensembl": "ENSG00000178693", "function": "磷酸酶/激酶，末端修饰"},
            "APE1": {"symbol": "APEX1", "ensembl": "ENSG00000100823", "function": "AP内切酶，末端处理"},
            "POL_mu": {"symbol": "POLM", "ensembl": "ENSG00000175315", "function": "聚合酶mu，末端填充"},
            "POL_lambda": {"symbol": "POLL", "ensembl": "ENSG00000166211", "function": "聚合酶lambda，末端填充"},
            "53BP1": {"symbol": "TP53BP1", "ensembl": "ENSG00000112530", "function": "NHEJ偏向因子，抑制HR"},
            "RIF1": {"symbol": "RIF1", "ensembl": "ENSG00000132604", "function": "53BP1下游，NHEJ导向"},
        },
    },
    "BER": {
        "name": "碱基切除修复 (Base Excision Repair)",
        "description": "修复单碱基损伤和小型碱基修饰",
        "human": {
            "OGG1": {"symbol": "OGG1", "ensembl": "ENSG00000114034", "function": "8-氧代G糖基酶，氧化损伤修复"},
            "NTHL1": {"symbol": "NTHL1", "ensembl": "ENSG00000065057", "function": "糖基酶，氧化损伤识别"},
            "UDG": {"symbol": "UNG", "ensembl": "ENSG00000076248", "function": "尿嘧啶DNA糖基酶"},
            "SMUG1": {"symbol": "SMUG1", "ensembl": "ENSG00000123415", "function": "单链选择性尿嘧啶糖基酶"},
            "MBD4": {"symbol": "MBD4", "ensembl": "ENSG00000129071", "function": "甲基化CpG结合域糖基酶"},
            "TDG": {"symbol": "TDG", "ensembl": "ENSG00000139391", "function": "胸腺嘧啶DNA糖基酶"},
            "APE1": {"symbol": "APEX1", "ensembl": "ENSG00000100823", "function": "AP内切酶，BER核心"},
            "APE2": {"symbol": "APEX2", "ensembl": "ENSG00000178119", "function": "AP内切酶2"},
            "XRCC1": {"symbol": "XRCC1", "ensembl": "ENSG00000163141", "function": "BER支架蛋白"},
            "POLB": {"symbol": "POLB", "ensembl": "ENSG00000106477", "function": "聚合酶beta，短patch BER"},
            "POLD": {"symbol": "POLD1", "ensembl": "ENSG00000069345", "function": "聚合酶delta，长patch BER"},
            "LIG3": {"symbol": "LIG3", "ensembl": "ENSG00000122641", "function": "连接酶III，BER封口"},
            "FEN1": {"symbol": "FEN1", "ensembl": "ENSG00000168487", "function": "翼端核酸酶1，长patch处理"},
            "PARP1": {"symbol": "PARP1", "ensembl": "ENSG00000114034", "function": "聚ADP核糖聚合酶，SSB检测"},
        },
    },
    "MMR": {
        "name": "错配修复 (Mismatch Repair)",
        "description": "修复复制错误产生的碱基错配",
        "human": {
            "MSH2": {"symbol": "MSH2", "ensembl": "ENSG00000095002", "function": "MutS同源，错配识别"},
            "MSH6": {"symbol": "MSH6", "ensembl": "ENSG00000116062", "function": "MutSalpha复合物，单碱基错配"},
            "MSH3": {"symbol": "MSH3", "ensembl": "ENSG00000119559", "function": "MutSbeta复合物，插入/缺失错配"},
            "MLH1": {"symbol": "MLH1", "ensembl": "ENSG00000076242", "function": "MutL同源，MMR信号"},
            "PMS2": {"symbol": "PMS2", "ensembl": "ENSG00000122512", "function": "MutLalpha复合物，内切酶活性"},
            "PMS1": {"symbol": "PMS1", "ensembl": "ENSG00000122479", "function": "MutLgamma复合物"},
            "EXO1": {"symbol": "EXO1", "ensembl": "ENSG00000171961", "function": "外切核酸酶1，MMR切割"},
            "PCNA": {"symbol": "PCNA", "ensembl": "ENSG00000131746", "function": "滑动钳，聚合酶辅助"},
            "RFC": {"symbol": "RFC1", "ensembl": "ENSG00000133056", "function": "复制因子C，PCNA加载"},
            "RPA": {"symbol": "RPA1", "ensembl": "ENSG00000132383", "function": "单链结合蛋白，稳定MMR中间体"},
            "LIG1": {"symbol": "LIG1", "ensembl": "ENSG00000105486", "function": "连接酶I，MMR封口"},
            "POLE": {"symbol": "POLE", "ensembl": "ENSG00000114034", "function": "聚合酶epsilon外切域，校对功能"},
            "POLD1": {"symbol": "POLD1", "ensembl": "ENSG00000069345", "function": "聚合酶delta外切域，校对功能"},
        },
    },
    "SSB": {
        "name": "单链断裂修复 (Single-Strand Break Repair)",
        "description": "修复DNA单链断裂，与BER通路重叠",
        "human": {
            "PARP1": {"symbol": "PARP1", "ensembl": "ENSG00000114034", "function": "SSB检测与信号，聚ADP核糖化"},
            "PARP2": {"symbol": "PARP2", "ensembl": "ENSG00000114034", "function": "PARP辅助，SSB检测"},
            "XRCC1": {"symbol": "XRCC1", "ensembl": "ENSG00000163141", "function": "SSB修复支架蛋白"},
            "LIG3": {"symbol": "LIG3", "ensembl": "ENSG00000122641", "function": "连接酶III，SSB封口"},
            "APE1": {"symbol": "APEX1", "ensembl": "ENSG00000100823", "function": "AP内切酶，SSB处理"},
            "PNKP": {"symbol": "PNKP", "ensembl": "ENSG00000178693", "function": "磷酸酶/激酶，末端修复"},
            "POLB": {"symbol": "POLB", "ensembl": "ENSG00000106477", "function": "聚合酶beta，缺口填充"},
            "TDP1": {"symbol": "TDP1", "ensembl": "ENSG00000198242", "function": "酪氨酸-DNA磷酸二酯酶1"},
            "TDP2": {"symbol": "TDP2", "ensembl": "ENSG00000183421", "function": "酪氨酸-DNA磷酸二酯酶2"},
            "APE2": {"symbol": "APEX2", "ensembl": "ENSG00000178119", "function": "AP内切酶2，备用路径"},
        },
    },
    "FA": {
        "name": "范可尼贫血通路 (Fanconi Anemia Pathway)",
        "description": "修复DNA交联损伤，与HR通路协作",
        "human": {
            "FANCA": {"symbol": "FANCA", "ensembl": "ENSG00000187741", "function": "FA核心复合物，交联识别"},
            "FANCB": {"symbol": "FANCB", "ensembl": "ENSG00000136636", "function": "FA核心复合物"},
            "FANCC": {"symbol": "FANCC", "ensembl": "ENSG00000158169", "function": "FA核心复合物"},
            "FANCD2": {"symbol": "FANCD2", "ensembl": "ENSG00000144554", "function": "FA-ID2复合物，泛素化信号"},
            "FANCE": {"symbol": "FANCE", "ensembl": "ENSG00000112038", "function": "FA核心复合物"},
            "FANCF": {"symbol": "FANCF", "ensembl": "ENSG00000197571", "function": "FA核心复合物"},
            "FANCG": {"symbol": "FANCG", "ensembl": "ENSG00000221869", "function": "FA核心复合物"},
            "FANCI": {"symbol": "FANCI", "ensembl": "ENSG00000134882", "function": "FA-ID2复合物"},
            "FANCL": {"symbol": "FANCL", "ensembl": "ENSG00000130720", "function": "FA E3泛素连接酶"},
            "FANCM": {"symbol": "FANCM", "ensembl": "ENSG00000185643", "function": "FA解旋酶，叉点稳定"},
            "SLX4": {"symbol": "SLX4", "ensembl": "ENSG00000188884", "function": "FA修复核酸酶支架"},
            "XPF": {"symbol": "ERCC4", "ensembl": "ENSG00000175595", "function": "内切核酸酶，交联解链"},
            "BRCA1": {"symbol": "BRCA1", "ensembl": "ENSG00000012048", "function": "FA下游，与HR交汇"},
            "BRCA2": {"symbol": "BRCA2", "ensembl": "ENSG00000139618", "function": "FANCD1，FA与HR共同节点"},
        },
    },
    "p53": {
        "name": "p53通路 (p53 Pathway)",
        "description": "DNA损伤响应与细胞命运决定",
        "human": {
            "TP53": {"symbol": "TP53", "ensembl": "ENSG00000141510", "function": "p53转录因子，DNA损伤响应核心"},
            "MDM2": {"symbol": "MDM2", "ensembl": "ENSG00000135679", "function": "p53负调控，泛素连接酶"},
            "MDM4": {"symbol": "MDM4", "ensembl": "ENSG00000198625", "function": "p53负调控辅助"},
            "ATM": {"symbol": "ATM", "ensembl": "ENSG00000182434", "function": "p53上游激酶"},
            "CHEK2": {"symbol": "CHEK2", "ensembl": "ENSG00000183765", "function": "p53上游激酶"},
            "CDKN1A": {"symbol": "CDKN1A", "ensembl": "ENSG00000124762", "function": "p21，p53下游，细胞周期阻滞"},
            "BAX": {"symbol": "BAX", "ensembl": "ENSG00000187741", "function": "p53下游，凋亡促进"},
            "PUMA": {"symbol": "BBC3", "ensembl": "ENSG00000105327", "function": "p53下游，凋亡促进"},
            "NOXA": {"symbol": "PMAIP1", "ensembl": "ENSG00000146082", "function": "p53下游，凋亡促进"},
            "GADD45A": {"symbol": "GADD45A", "ensembl": "ENSG00000116717", "function": "p53下游，DNA修复辅助"},
            "PTEN": {"symbol": "PTEN", "ensembl": "ENSG00000171862", "function": "p53调控，PI3K抑制"},
        },
    },
}


def search_pubmed(query, max_results=20):
    """从PubMed搜索DNA损伤修复相关新基因"""
    if not HAS_REQUESTS:
        print("  ⚠ requests库未安装，无法搜索PubMed")
        return []

    genes = []
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    try:
        # 搜索
        params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"}
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])

        if not id_list:
            return []

        # 获取摘要
        fetch_params = {"db": "pubmed", "id": ",".join(id_list), "rettype": "abstract", "retmode": "text"}
        resp2 = requests.get(fetch_url, params=fetch_params, timeout=15)
        abstracts = resp2.text

        # 简化：从摘要中提取可能的基因符号（大写3-7字母词）
        import re
        gene_pattern = re.compile(r'\b[A-Z][A-Z0-9]{2,6}\b')
        found = gene_pattern.findall(abstracts)
        # 过滤常见非基因词
        common = {"DNA", "RNA", "PCR", "PCR", "NHEJ", "BER", "MMR", "HR", "FA", "ATP", "GTP", "DMSO", "SDS", "EDTA", "PBS", "PBS", "MAPK", "PI3K", "EGFR"}
        unique_genes = set(g for g in found if g not in common and len(g) >= 3)
        return list(unique_genes)[:30]

    except Exception as e:
        print(f"  ⚠ PubMed搜索失败: {e}")
        return []


def save_csv(selected_pathways, output_path):
    """保存基因列表CSV"""
    rows = []
    for pathway_key, pathway_data in selected_pathways.items():
        for gene_key, gene_info in pathway_data["human"].items():
            rows.append(f"{pathway_key},{gene_info['symbol']},{gene_info['ensembl']},{gene_info['function']}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("通路,基因符号,Ensembl ID,功能简述\n")
        f.write("\n".join(rows))
    print(f"  ✅ 基因列表已保存: {output_path}")


def plot_venn(selected_pathways, output_path):
    """绘制通路交叉Venn图（最多3通路）"""
    if not HAS_VENN:
        print("  ⚠ matplotlib-venn未安装，跳过Venn图")
        return

    pathway_keys = list(selected_pathways.keys())
    gene_sets = []
    for key in pathway_keys:
        symbols = set(g["symbol"] for g in selected_pathways[key]["human"].values())
        gene_sets.append(symbols)

    plt.figure(figsize=(10, 8))

    if len(pathway_keys) == 2:
        venn2(gene_sets, set_labels=[PATHWAY_GENES[k]["name"].split("(")[0].strip() for k in pathway_keys])
    elif len(pathway_keys) == 3:
        venn3(gene_sets, set_labels=[PATHWAY_GENES[k]["name"].split("(")[0].strip() for k in pathway_keys])
    else:
        # 多通路用柱状图展示交叉
        all_genes = set()
        for s in gene_sets:
            all_genes.update(s)
        cross_counts = []
        for gene in sorted(all_genes):
            count = sum(1 for s in gene_sets if gene in s)
            cross_counts.append((gene, count))
        multi = [(g, c) for g, c in cross_counts if c >= 2]
        if multi:
            genes_m, counts_m = zip(*multi[:20])
            plt.barh(range(len(genes_m)), counts_m, color='#2196F3')
            plt.yticks(range(len(genes_m)), genes_m)
            plt.xlabel('出现通路数')
            plt.title('多通路交叉基因 Top20')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"  ✅ Venn图已保存: {output_path}")


def print_report(selected_pathways):
    """终端打印通路报告"""
    report = "\n╔══════════════════════════════════════════════════════════════╗\n"
    report += "║        DNA损伤修复基因集收集报告                              ║\n"
    report += "╠══════════════════════════════════════════════════════════════╣\n"

    total_genes = 0
    all_symbols = set()
    for key, data in selected_pathways.items():
        symbols = [g["symbol"] for g in data["human"].values()]
        all_symbols.update(symbols)
        total_genes += len(symbols)
        report += f"║ 【{data['name']}】\n"
        report += f"║   {data['description']}\n"
        report += f"║   基因数: {len(symbols)}\n"
        report += f"║   基因: {', '.join(symbols[:10])}{'...' if len(symbols)>10 else ''}\n"
        report += "║══════════════════════════════════════════════════════════════║\n"

    unique_count = len(all_symbols)
    overlap = total_genes - unique_count
    report += f"║ 【总统计】\n"
    report += f"║   总基因条目: {total_genes}\n"
    report += f"║   唯一基因数: {unique_count}\n"
    report += f"║   通路交叉数: {overlap} (基因出现在≥2通路)\n"

    # 交叉基因列表
    gene_pathway_map = defaultdict(list)
    for key, data in selected_pathways.items():
        for g_key, g_info in data["human"].items():
            gene_pathway_map[g_info["symbol"]].append(key)

    cross_genes = [(g, ps) for g, ps in gene_pathway_map.items() if len(ps) >= 2]
    if cross_genes:
        report += f"║   交叉基因: {', '.join(g for g, _ in cross_genes[:10])}\n"

    report += "╚══════════════════════════════════════════════════════════════╝\n"
    return report


def main():
    print("=" * 60)
    print("  🔬 DNA损伤修复基因集收集器")
    print("  🎯 针对陆慧智课题组（DNA损伤修复方向）")
    print("=" * 60)

    # 显示可选通路
    print("\n可选修复通路：")
    for key, data in PATHWAY_GENES.items():
        print(f"  {key}: {data['name']} ({len(data['human'])} 基因)")

    pathway_input = get_input("选择通路(多选，逗号分隔，如HR,NHEJ,BER)", default="HR,NHEJ,BER")
    selected_keys = [k.strip().upper() for k in pathway_input.split(',')]

    # 验证并选择通路
    valid_keys = []
    for k in selected_keys:
        if k in PATHWAY_GENES:
            valid_keys.append(k)
        else:
            print(f"  ⚠ 未知通路: {k}，跳过")

    if not valid_keys:
        print("  ❌ 未选择任何有效通路")
        sys.exit(1)

    selected_pathways = {k: PATHWAY_GENES[k] for k in valid_keys}

    species = get_input("物种(human/mouse)", default="human")
    search_pubmed_flag = get_input("是否PubMed补充搜索(yes/no)", default="no")
    include_p53 = get_input("是否包含p53通路(yes/no)", default="no")

    # 如选择包含p53但未选
    if include_p53.lower() in ('yes', 'y') and "p53" not in selected_pathways:
        selected_pathways["p53"] = PATHWAY_GENES["p53"]

    # PubMed补充
    pubmed_genes = []
    if search_pubmed_flag.lower() in ('yes', 'y') and HAS_REQUESTS:
        print("  ⏳ 正在搜索PubMed补充基因...")
        for key in valid_keys:
            query = f"DNA damage repair {PATHWAY_GENES[key]['name'].split('(')[0].strip()} new gene"
            extra = search_pubmed(query)
            pubmed_genes.extend(extra)
            print(f"    {key}: 发现 {len(extra)} 个候选基因")

        if pubmed_genes:
            print(f"  🔍 PubMed补充候选基因: {', '.join(pubmed_genes[:15])}")
            print("  💡 请手动验证这些候选基因是否属于相关通路")

    # 打印报告
    report = print_report(selected_pathways)
    print(report)

    if pubmed_genes:
        print(f"\n  PubMed补充候选基因({len(pubmed_genes)}个):")
        for g in pubmed_genes:
            print(f"    - {g}")

    # 保存CSV
    base_name = "dna_damage_genes"
    output_dir = "."
    csv_path = os.path.join(output_dir, f"{base_name}_{','.join(valid_keys)}.csv")
    save_csv(selected_pathways, csv_path)

    # PubMed候选也保存
    if pubmed_genes:
        pubmed_path = os.path.join(output_dir, f"{base_name}_pubmed_candidates.csv")
        with open(pubmed_path, 'w', encoding='utf-8') as f:
            f.write("候选基因,来源\n")
            for g in pubmed_genes:
                f.write(f"{g},PubMed搜索\n")
        print(f"  ✅ PubMed候选已保存: {pubmed_path}")

    # Venn图
    make_venn = get_input("是否绘制通路交叉Venn图(yes/no)", default="yes")
    if make_venn.lower() in ('yes', 'y') and HAS_VENN:
        venn_path = os.path.join(output_dir, f"{base_name}_venn.png")
        plot_venn(selected_pathways, venn_path)

    print("  ✅ DNA损伤修复基因集收集完成！")


if __name__ == "__main__":
    main()