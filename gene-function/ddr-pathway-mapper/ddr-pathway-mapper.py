#!/usr/bin/env python3
"""🔥DNA损伤修复通路映射(NER/BER/HR/NHEJ/MMR等)"""

# DNA损伤修复通路映射
import matplotlib.pyplot as plt

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


print("=" * 60)
print("  🔥 DNA损伤修复通路映射器")
print("=" * 60)

input_genes = get_input("输入基因列表文件路径", "gene_list.txt")
output_file = get_input("通路映射结果路径", "ddr_pathway_mapping.tsv")
plot_out = get_input("通路分布图路径", "ddr_pathway_distribution.png")
detail = get_input("详细程度(brief/full)", "full")

# DDR pathway gene sets (for LU lab - DNA damage repair)
ddr_pathways = {
    'NER (Nucleotide Excision Repair)': ['XPA','XPC','XPD','XPB','XPF','XPG','ERCC1','ERCC4','ERCC5','ERCC6','ERCC8','DDB1','DDB2','POLH','TFIIH'],
    'BER (Base Excision Repair)': ['OGG1','NTHL1','APE1','APEX2','POLB','POLL','XRCC1','LIG3','PARP1','MUTYH','UDG','MBD4','SMUG1','NTH1'],
    'HR (Homologous Recombination)': ['BRCA1','BRCA2','RAD51','RAD52','RAD54','RAD50','MRE11','NBS1','ATM','ATR','PALB2','BARD1','CHEK2','DMC1','HJURP'],
    'NHEJ (Non-Homologous End Joining)': ['KU70','KU80','DNA-PKcs','XRCC4','LIG4','XLF','Artemis','PAXX','MRI','POLQ'],
    'MMR (Mismatch Repair)': ['MSH2','MSH3','MSH6','MLH1','PMS1','PMS2','EXO1','PCNA','RPA','DNA2'],
    'TLS (Translesion Synthesis)': ['REV1','REV3','REV7','POLH','POLK','POLI','POLZ','RAD18','RAD5','PCNA'],
    'DDR Signaling': ['ATM','ATR','CHEK1','CHEK2','TP53','MDM2','H2AX','MDC1','RPA','53BP1','BRCA1','CLASPIN'],
    'Fanconi Anemia Pathway': ['FANCA','FANCB','FANCC','FANCD2','FANCE','FANCF','FANCG','FANCI','FANCL','FANCM','FANCN','FANCO']
}

genes = [line.strip() for line in open(input_genes) if line.strip()]
print(f"✅ 输入基因: {len(genes)}")

mapping = {}
for gene in genes:
    mapped = []
    for pathway, pgenes in ddr_pathways.items():
        if gene in pgenes:
            mapped.append(pathway)
    if mapped:
        mapping[gene] = mapped
    else:
        mapping[gene] = ['Unclassified']

classified = sum(1 for g in genes if mapping[g] != ['Unclassified'])
print(f"  已分类: {classified}, 未分类: {len(genes)-classified}")

with open(output_file, 'w') as f:
    f.write("gene\tpathway\n")
    for gene in genes:
        for path in mapping[gene]:
            f.write(f"{gene}\t{path}\n")

pathway_counts = {}
for gene in genes:
    for path in mapping[gene]:
        pathway_counts[path] = pathway_counts.get(path, 0) + 1

sorted_paths = sorted(pathway_counts.items(), key=lambda x: -x[1])
fig, ax = plt.subplots(figsize=(10, 6))
names = [p[0].split('(')[0] for p in sorted_paths]
counts = [p[1] for p in sorted_paths]
colors = ['#C44E52','#4C72B0','#55A868','#DD8452','#8C8C8C','#CCB974','#64B5CD','#E5AE38']
ax.barh(names, counts, color=colors[:len(names)])
ax.set_xlabel("Gene Count")
ax.set_title("DDR Pathway Distribution 🔥")
plt.tight_layout()
plt.savefig(plot_out, dpi=150)
print(f"\n✅ 映射完成")
print(f"📄 结果: {output_file}")
print(f"📊 分布图: {plot_out}")
