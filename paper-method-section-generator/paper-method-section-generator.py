#!/usr/bin/env python3
"""论文方法部分模板生成"""

# 论文方法部分模板生成
print("=" * 60)
print("  📖 论文方法部分模板生成器")
print("=" * 60)

analysis_type = get_input("分析类型(rna-seq/sc-rna-seq/chip-seq/variant)", "rna-seq")
species = get_input("物种", "human")
ref_genome = get_input("参考基因组版本", "GRCh38")
output_file = get_input("方法模板输出路径", "methods_section.md")

rna_seq_template = "## RNA-seq Analysis\n\n### Sample Preparation\nTotal RNA was extracted using TRIzol reagent (Invitrogen) following the manufacturer protocol. RNA quality was assessed using Agilent 2100 Bioanalyzer (RIN > 7.0).\n\n### Library Construction and Sequencing\nStrand-specific RNA-seq libraries were prepared using the NEBNext Ultra II RNA Library Prep Kit. Libraries were sequenced on the Illumina NovaSeq 6000 platform with 150bp paired-end reads.\n\n### Data Processing\nRaw reads were quality-checked using FastQC and trimmed using Trimmomatic to remove adapters and low-quality bases. Clean reads were aligned to the " + ref_genome + " reference genome using STAR aligner (v2.7.10a) with default parameters.\n\n### Quantification and Differential Expression\nGene expression was quantified using featureCounts (Subread v2.0.1). Differential expression analysis was performed using DESeq2 (v1.38.3) with the Wald test. Genes with |log2FC| > 1 and adjusted p-value < 0.05 were considered significantly differentially expressed.\n\n### Functional Enrichment\nGO and KEGG pathway enrichment analyses were performed using clusterProfiler (v4.6.2) with BH-adjusted p-value < 0.05 as the significance threshold."

sc_template = "## Single-cell RNA-seq Analysis\n\n### Sample Preparation\nSingle-cell suspensions were prepared using enzymatic dissociation. Cell viability was assessed (>85%) using Trypan Blue staining.\n\n### Library Construction\nSingle-cell libraries were constructed using the 10x Genomics Chromium platform (v3 chemistry). Sequencing was performed on Illumina NovaSeq 6000.\n\n### Data Processing\nRaw data was processed using Cell Ranger (v7.1.0) for demultiplexing, alignment to " + ref_genome + ", and UMI counting. Quality control was performed using Seurat (v5.0.0).\n\n### Quality Control and Filtering\nCells with nFeature_RNA < 200 or > 8000, or percent.mt > 20% were removed. Doublets were detected and removed using DoubletFinder.\n\n### Clustering and Annotation\nData was normalized using SCTransform, followed by PCA dimensionality reduction. Cells were clustered using Louvain algorithm at resolution 0.5. Cell type annotation was performed using marker gene expression and SingleR."

chip_template = "## ChIP-seq Analysis\n\n### Sample Preparation\nChromatin immunoprecipitation was performed. Cross-linking was performed with 1% formaldehyde for 10 min.\n\n### Library Construction\nChIP-seq libraries were prepared using the NEBNext Ultra II DNA Library Prep Kit and sequenced on Illumina NovaSeq 6000.\n\n### Data Processing\nReads were aligned to " + ref_genome + " using Bowtie2 (v2.5.1). Duplicate reads were removed using Picard MarkDuplicates.\n\n### Peak Calling\nPeaks were called using MACS2 (v2.2.7.1) with q-value < 0.01. Peak annotation was performed using ChIPseeker."

variant_template = "## Variant Analysis\n\n### Sample Preparation\nGenomic DNA was extracted using QIAamp DNA Mini Kit. DNA quality was assessed (Q>30, >1ug).\n\n### Sequencing\nWhole-genome sequencing was performed on Illumina NovaSeq 6000 with 150bp paired-end reads at minimum 30x coverage.\n\n### Data Processing\nRaw reads were aligned to " + ref_genome + " using BWA-MEM2 (v2.2.1). Variants were called using GATK HaplotypeCaller following GATK Best Practices.\n\n### Variant Filtering and Annotation\nVariants were filtered using VQSR and hard filters (QUAL>30, DP>10, FS<60). Annotation was performed using ANNOVAR and ClinVar database."

templates = {
    "rna-seq": rna_seq_template,
    "sc-rna-seq": sc_template,
    "chip-seq": chip_template,
    "variant": variant_template,
}

content = templates.get(analysis_type, "## " + analysis_type + " Analysis\n\n[Template not available for this analysis type]")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ 方法部分模板已生成")
print("  分析类型: " + analysis_type)
print("  物种: " + species)
print("  参考基因组: " + ref_genome)
print("📄 输出: " + output_file)
