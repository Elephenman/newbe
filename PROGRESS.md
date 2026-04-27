# Newbe 50工具开发进度追踪

> 自动化循环：每3小时执行一次，每次开发一批工具+审核+上传

## 总进度

| 状态 | 数量 |
|------|------|
| ✅ 已完成 | 5 |
| 🔨 开发中 | 0 |
| 🔍 审核中 | 0 |
| ⏳ 待开发 | 45 |

## 批次计划

### Batch 1 (入学前刚需，15个)
- [x] #1 fastq-qc-checker ✅
- [x] #4 bam-stats-reporter ✅
- [x] #8 sequence-stat-visualizer ✅
- [x] #11 deseq2-result-formatter ✅
- [x] #35 dna-damage-gene-collector ✅
- [ ] #16 pca-tsne-umap-plotter
- [ ] #21 seurat-qc-pipeline
- [ ] #35 dna-damage-gene-collector
- [ ] #36 pubmed-batch-searcher
- [ ] #37 doi-to-citation
- [ ] #43 obsidian-paper-note-generator
- [ ] #44 sci-color-palette
- [ ] #46 multi-panel-composer
- [ ] #47 project-dir-initializer
- [ ] #48 sample-sheet-validator

### Batch 2 (课题深入期，15个)
- [ ] #2 fastq-filter
- [ ] #3 fastq-to-fasta
- [ ] #5 vcf-filter-annotate
- [ ] #6 gtf-feature-extractor
- [ ] #7 genome-fasta-slicer
- [ ] #12 expression-heatmap-cluster
- [ ] #14 gsea-runner
- [ ] #15 tpm-fpkm-calculator
- [ ] #17 deg-compare-tool
- [ ] #18 co-expression-network
- [ ] #19 survival-expression-correlator
- [ ] #20 batch-effect-inspector
- [ ] #22 cell-type-annotator
- [ ] #23 umap-batch-plotter
- [ ] #24 pseudotime-setup

### Batch 3 (论文产出期，10个)
- [ ] #9 kmer-counter
- [ ] #10 bed-merge-annotate
- [ ] #25 cellchat-interaction-parser
- [ ] #26 doublet-detector-wrapper
- [ ] #27 spatial-spot-annotator
- [ ] #28 sc-marker-finder
- [ ] #29 snp-stats-reporter
- [ ] #30 motif-scanner
- [ ] #31 genome-density-plotter
- [ ] #32 ld-decay-calculator

### Batch 4 (补充工具，10个)
- [ ] #33 promoter-extractor
- [ ] #34 cnv-segment-plotter
- [ ] #38 paper-pdf-meta-extractor
- [ ] #39 keyword-network-builder
- [ ] #40 literature-review-matrix
- [ ] #41 citation-tracker
- [ ] #42 reference-cleaner
- [ ] #45 figure-size-checker
- [ ] #49 conda-env-checker
- [ ] #50 pipeline-log-parser

## 开发规范

每个工具目录结构：
```
tool-name/
├── tool_name.py (或 .R)    # 主脚本，所有参数 input() 交互
├── README.md               # 用法说明 + 参数说明 + 示例
└── requirements.txt        # 依赖列表（尽量≤5个包）
```

交互式输入范式：
```python
def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    return type(val) if val else default
```