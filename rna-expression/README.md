<div align="center">

# 📊 转录组/表达分析

**DESeq2/DEG/标准化/火山图/热图/WGCNA等转录组表达分析工具** (34个工具)

</div>

---

## 工具列表

| # | 工具 | 语言 | 说明 |
|---|------|:----:|------|
| 1 | [alternative-splicing-detector](./alternative-splicing-detector/) | R | Detect alternative splicing events + visualization |
| 2 | [batch-effect-inspector](./batch-effect-inspector/) | Python | Batch effect detection + PCA visualization |
| 3 | [deg-compare-tool](./deg-compare-tool/) | Python | Cross-compare multiple DEG results (Venn/UpSet) |
| 4 | [deg-direction-plotter](./deg-direction-plotter/) | Python | DEG direction consistency arrow plot |
| 5 | [deg-effect-size-calculator](./deg-effect-size-calculator/) | Python | Calculate DEG effect sizes (log2FC confidence intervals) |
| 6 | [deg-fdr-adjuster](./deg-fdr-adjuster/) | Python | Compare multiple testing corrections (BH/BY/Q-value) |
| 7 | [deg-meta-analyzer](./deg-meta-analyzer/) | Python | 对多个研究的DEG结果进行元分析，找出跨研究的共识差异基因。 |
| 8 | [deg-pathway-annotator](./deg-pathway-annotator/) | R | Auto-annotate DEGs to KEGG/GO pathways |
| 9 | [deg-upset-plotter](./deg-upset-plotter/) | Python | 绘制多组差异表达基因交集UpSet图，比Venn图更清晰展示复杂交集。 |
| 10 | [deg-venn-plotter](./deg-venn-plotter/) | Python | Venn diagram for multi-group DEG overlap |
| 11 | [deg-volcano-interactive](./deg-volcano-interactive/) | Python | Interactive volcano plot (Plotly click-to-inspect genes) |
| 12 | [deseq2-result-formatter](./deseq2-result-formatter/) | R | DESeq2 results → publication table + volcano plot |
| 13 | [expression-boxplot-maker](./expression-boxplot-maker/) | R | Batch gene expression boxplots + statistical tests |
| 14 | [expression-correlation-matrix](./expression-correlation-matrix/) | Python | Gene expression correlation matrix + heatmap |
| 15 | [expression-heatmap-cluster](./expression-heatmap-cluster/) | R | Expression matrix → clustered heatmap (Nature palette) |
| 16 | [expression-outlier-detector](./expression-outlier-detector/) | Python | 检测表达矩阵中的异常样本和基因（IQR/Z-score方法）。 |
| 17 | [expression-percentile-ranker](./expression-percentile-ranker/) | Python | Gene expression percentile ranking + binning |
| 18 | [expression-quartile-scaler](./expression-quartile-scaler/) | Python | 对表达矩阵进行分位数标准化，消除样本间技术偏差。 |
| 19 | [expression-signal-to-noise](./expression-signal-to-noise/) | Python | Expression signal-to-noise ratio + low-quality gene filter |
| 20 | [expression-violin-plotter](./expression-violin-plotter/) | R | Multi-gene/multi-sample expression violin plots |
| 21 | [expression-z-score-transformer](./expression-z-score-transformer/) | Python | Expression matrix Z-score normalization + heatmap |
| 22 | [gene-length-normalizer](./gene-length-normalizer/) | Python | Gene length bias correction (RPKM/TPM/GC) |
| 23 | [isoform-expression-comparer](./isoform-expression-comparer/) | R | Compare isoform expression within same gene |
| 24 | [rna-seq-count-merger](./rna-seq-count-merger/) | Python | Merge multi-sample count matrices + consistency check |
| 25 | [rna-seq-normalizer](./rna-seq-normalizer/) | Python | RNA-seq count normalization (TPM/FPKM/RPKM/CPM) |
| 26 | [rna-seq-power-calculator](./rna-seq-power-calculator/) | R | RNA-seq sample size/power calculation |
| 27 | [rna-seq-spike-in-normalizer](./rna-seq-spike-in-normalizer/) | R | ERCC spike-in normalization for RNA-seq |
| 28 | [rpkm-to-tpm-converter](./rpkm-to-tpm-converter/) | Python | 将RPKM标准化表达矩阵转换为TPM格式。 |
| 29 | [splice-junction-counter](./splice-junction-counter/) | Python | Count splice junctions from STAR SJ.out.tab |
| 30 | [tpm-fpkm-calculator](./tpm-fpkm-calculator/) | Python | Convert raw counts to TPM/FPKM/CPM |
| 31 | [tpm-matrix-normalizer](./tpm-matrix-normalizer/) | Python | 对TPM表达矩阵进行标准化和log2转换处理。 |
| 32 | [transcript-length-extractor](./transcript-length-extractor/) | Python | 从GTF注释文件中提取转录本长度和exon数量信息。 |
| 33 | [volcano-label-editor](./volcano-label-editor/) | Python | Volcano plot label editor (add/modify gene labels) |
| 34 | [volcano-plot-enhancer](./volcano-plot-enhancer/) | Python | Enhanced volcano plot (annotation + palette + threshold lines) |

---

← [返回主目录](../)
