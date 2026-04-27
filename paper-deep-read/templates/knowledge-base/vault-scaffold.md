# PaperVault 知识库目录结构

## 目录结构

```
PaperVault/
├── 00-Inbox/                      # 收件箱 - 新论文临时存放
├── 01-Bioinformatics/              # 生物信息学
│   ├── Single-Cell/               # 单细胞组学
│   ├── RNA-seq/                    # RNA测序分析
│   ├── Genomics/                   # 基因组学
│   ├── Epigenomics/                # 表观基因组学
│   └── Metagenomics/               # 宏基因组学
├── 01-Biology/                     # 生物学
│   ├── Molecular-Biology/          # 分子生物学
│   ├── Cell-Biology/               # 细胞生物学
│   ├── Immunology/                 # 免疫学
│   └── Microbiology/               # 微生物学
├── 02-AI-ML/                       # 人工智能与机器学习
│   ├── NLP/                        # 自然语言处理
│   ├── CV/                         # 计算机视觉
│   ├── Generative-Models/          # 生成模型
│   └── Graph-Neural-Networks/     # 图神经网络
├── 03-Structural-Biology/          # 结构生物学
├── 04-Other/                       # 其他领域
├── Templates/                      # 笔记模板
├── MOC/                            # 领域地图
│   ├── Bioinformatics-MOC.md
│   ├── Biology-MOC.md
│   └── AI-ML-MOC.md
└── Resources/
    ├── Database-Links.md          # 数据库链接汇总
    └── Tool-Index.md              # 工具索引
```

## 创建脚本 (Bash)

```bash
#!/bin/bash
# PaperVault 目录结构创建脚本
# 使用方法: bash create-vault.sh [根目录名]

VAULT_NAME=${1:-PaperVault}

# 创建主目录和子目录
mkdir -p "${VAULT_NAME}/00-Inbox"
mkdir -p "${VAULT_NAME}/01-Bioinformatics/Single-Cell"
mkdir -p "${VAULT_NAME}/01-Bioinformatics/RNA-seq"
mkdir -p "${VAULT_NAME}/01-Bioinformatics/Genomics"
mkdir -p "${VAULT_NAME}/01-Bioinformatics/Epigenomics"
mkdir -p "${VAULT_NAME}/01-Bioinformatics/Metagenomics"
mkdir -p "${VAULT_NAME}/01-Biology/Molecular-Biology"
mkdir -p "${VAULT_NAME}/01-Biology/Cell-Biology"
mkdir -p "${VAULT_NAME}/01-Biology/Immunology"
mkdir -p "${VAULT_NAME}/01-Biology/Microbiology"
mkdir -p "${VAULT_NAME}/02-AI-ML/NLP"
mkdir -p "${VAULT_NAME}/02-AI-ML/CV"
mkdir -p "${VAULT_NAME}/02-AI-ML/Generative-Models"
mkdir -p "${VAULT_NAME}/02-AI-ML/Graph-Neural-Networks"
mkdir -p "${VAULT_NAME}/03-Structural-Biology"
mkdir -p "${VAULT_NAME}/04-Other"
mkdir -p "${VAULT_NAME}/Templates"
mkdir -p "${VAULT_NAME}/MOC"
mkdir -p "${VAULT_NAME}/Resources"

# 创建占位文件和README
echo "# ${VAULT_NAME}" > "${VAULT_NAME}/README.md"
echo "" >> "${VAULT_NAME}/README.md"
echo "## 目录结构" >> "${VAULT_NAME}/README.md"
echo "本知识库按照领域分类组织论文笔记。" >> "${VAULT_NAME}/README.md"

# 创建 Templates 目录说明
cat > "${VAULT_NAME}/Templates/README.md" << 'EOF'
# 笔记模板

本目录存放论文深度解读所需的各类模板。

## 模板列表

| 模板 | 用途 | 文件名 |
|------|------|--------|
| 单论文笔记模板 | 深度解读单篇论文 | single-paper/note-template.md |
| 图像说明模板 | 图像命名和引用规范 | single-paper/images-readme.md |
| 对比分析模板 | 多论文对比分析 | comparison/comparison-template.md |
| Pipeline模板 | 生信分析流程可视化 | bioinformatics/pipeline-template.md |
| 数据库汇总模板 | 数据库资源记录 | bioinformatics/database-summary.md |
| MOC模板 | 领域地图 | knowledge-base/moc-template.md |
| Dataview查询 | 常用数据查询 | knowledge-base/dataview-queries.md |

## 使用说明

1. 复制模板到对应论文笔记目录
2. 按 {{}} 提示填充内容
3. 根据论文类型增删相关章节
EOF

# 创建 Resources 目录文件
cat > "${VAULT_NAME}/Resources/Database-Links.md" << 'EOF'
# 数据库链接汇总

## 序列数据库

| 数据库 | URL | 用途 |
|--------|-----|------|
| NCBI GenBank | https://www.ncbi.nlm.nih.gov/genbank/ | 核酸序列 |
| EMBL-EBI | https://www.ebi.ac.uk/ | 核酸/蛋白质序列 |
| DDBJ | https://www.ddbj.nig.ac.jp/ | 核酸序列 |

## 蛋白质数据库

| 数据库 | URL | 用途 |
|--------|-----|------|
| UniProt | https://www.uniprot.org/ | 蛋白质序列/功能 |
| PDB | https://www.rcsb.org/ | 蛋白质结构 |
| Pfam | https://pfam.xfam.org/ | 蛋白质家族 |

## 基因组数据库

| 数据库 | URL | 用途 |
|--------|-----|------|
| Ensembl | https://www.ensembl.org/ | 基因组浏览器 |
| UCSC Genome Browser | https://genome.ucsc.edu/ | 基因组浏览器 |
| NCBI Genome | https://www.ncbi.nlm.nih.gov/genome/ | 基因组目录 |

## 通路数据库

| 数据库 | URL | 用途 |
|--------|-----|------|
| KEGG | https://www.kegg.jp/ | 代谢/信号通路 |
| Reactome | https://reactome.org/ | 分子通路 |
| GO | http://geneontology.org/ | 基因本体 |

## 表达数据库

| 数据库 | URL | 用途 |
|--------|-----|------|
| GEO | https://www.ncbi.nlm.nih.gov/geo/ | 基因表达谱 |
| ArrayExpress | https://www.ebi.ac.uk/arrayexpress/ | 基因表达数据 |
| GTEx | https://gtexportal.org/ | 组织表达 |

## 变异数据库

| 数据库 | URL | 用途 |
|--------|-----|------|
| dbSNP | https://www.ncbi.nlm.nih.gov/snp/ | 单核苷酸多态性 |
| ClinVar | https://www.ncbi.nlm.nih.gov/clinvar/ | 临床变异 |
| gnomAD | https://gnomad.broadinstitute.org/ | 基因组变异 |

## 单细胞数据库

| 数据库 | URL | 用途 |
|--------|-----|------|
| Single Cell Portal | https://singlecell.broadinstitute.org/ | 单细胞数据 |
| HCA | https://data.humancellatlas.org/ | 人细胞图谱 |
| PanglaoDB | https://panglaodb.se/ | 单细胞RNA-seq |

EOF

cat > "${VAULT_NAME}/Resources/Tool-Index.md" << 'EOF'
# 工具索引

## 序列分析

| 工具 | 用途 | 语言 | 链接 |
|------|------|------|------|
| BLAST | 序列比对 | C | https://blast.ncbi.nlm.nih.gov/ |
| Bowtie | 短序列比对 | C++ | http://bowtie-bio.sourceforge.net/ |
| STAR | RNA-seq比对 | C++ | https://github.com/alexdobin/STAR |

## 表达分析

| 工具 | 用途 | 语言 | 链接 |
|------|------|------|------|
| DESeq2 | 差异表达分析 | R | https://bioconductor.org/packages/DESeq2/ |
| edgeR | 差异表达分析 | R | https://bioconductor.org/packages/edgeR/ |
| cufflinks | 转录本组装 | C++ | https://github.com/cole-trapnell-lab/cufflinks |

## 单细胞分析

| 工具 | 用途 | 语言 | 链接 |
|------|------|------|------|
| Seurat | 单细胞分析 | R | https://satijalab.org/seurat/ |
| Scanpy | 单细胞分析 | Python | https://scanpy.readthedocs.io/ |
| Cell Ranger | 10x数据处理 | C++ | https://support.10xgenomics.com/ |

## 基因组分析

| 工具 | 用途 | 语言 | 链接 |
|------|------|------|------|
| GATK | 变异检测 | Java | https://gatk.broadinstitute.org/ |
| FreeBayes | 变异检测 | C++ | https://github.com/ekg/freebayes |
| SAMtools | 高通量测序数据处理 | C | http://samtools.sourceforge.net/ |

## 可视化

| 工具 | 用途 | 语言 | 链接 |
|------|------|------|------|
| IGV | 基因组浏览器 | Java | https://software.broadinstitute.org/igv/ |
| UCSC Browser | 在线基因组浏览器 | Web | https://genome.ucsc.edu/ |
| ggplot2 | 统计绘图 | R | https://ggplot2.tidyverse.org/ |

EOF

# 创建 MOC 目录占位文件
cat > "${VAULT_NAME}/MOC/Bioinformatics-MOC.md" << 'EOF'
---
type: moc
domain: bioinformatics
updated: {{YYYY-MM-DD}}
tags: [type/moc, domain/bioinformatics]
---

# 生物信息学 MOC

## 领域概述
{{简要描述生物信息学的研究范围和发展方向}}

## 子主题

### [[../01-Bioinformatics/Single-Cell/]] 单细胞组学
### [[../01-Bioinformatics/RNA-seq/]] RNA测序分析
### [[../01-Bioinformatics/Genomics/]] 基因组学
### [[../01-Bioinformatics/Epigenomics/]] 表观基因组学
### [[../01-Bioinformatics/Metagenomics/]] 宏基因组学

## 近期更新
```dataview
TABLE file.ctime as 创建时间, paper_type as 类型
FROM "01-Bioinformatics"
WHERE note_version > 0
SORT file.ctime DESC
LIMIT 10
```

## 核心概念
- [[../01-Bioinformatics/Single-Cell/]] 单细胞RNA-seq (scRNA-seq)
- [[../01-Bioinformatics/RNA-seq/]] 差异表达分析
- [[../01-Bioinformatics/Genomics/]] 全基因组测序

## 交叉引用
- [[../01-Biology/]] 生物学基础
- [[../02-AI-ML/]] AI/ML方法应用
EOF

cat > "${VAULT_NAME}/MOC/Biology-MOC.md" << 'EOF'
---
type: moc
domain: biology
updated: {{YYYY-MM-DD}}
tags: [type/moc, domain/biology]
---

# 生物学 MOC

## 领域概述
{{简要描述生物学的研究范围和发展方向}}

## 子主题

### [[../01-Biology/Molecular-Biology/]] 分子生物学
### [[../01-Biology/Cell-Biology/]] 细胞生物学
### [[../01-Biology/Immunology/]] 免疫学
### [[../01-Biology/Microbiology/]] 微生物学

## 近期更新
```dataview
TABLE file.ctime as 创建时间, paper_type as 类型
FROM "01-Biology"
WHERE note_version > 0
SORT file.ctime DESC
LIMIT 10
```

## 核心概念
- [[../01-Biology/Molecular-Biology/]] 基因表达调控
- [[../01-Biology/Cell-Biology/]] 细胞信号转导
- [[../01-Biology/Immunology/]] 免疫应答机制

## 交叉引用
- [[../01-Bioinformatics/]] 生物信息学工具
- [[../03-Structural-Biology/]] 结构生物学
EOF

cat > "${VAULT_NAME}/MOC/AI-ML-MOC.md" << 'EOF'
---
type: moc
domain: ai-ml
updated: {{YYYY-MM-DD}}
tags: [type/moc, domain/ai-ml]
---

# 人工智能与机器学习 MOC

## 领域概述
{{简要描述AI/ML的研究范围和发展方向}}

## 子主题

### [[../02-AI-ML/NLP/]] 自然语言处理
### [[../02-AI-ML/CV/]] 计算机视觉
### [[../02-AI-ML/Generative-Models/]] 生成模型
### [[../02-AI-ML/Graph-Neural-Networks/]] 图神经网络

## 近期更新
```dataview
TABLE file.ctime as 创建时间, paper_type as 类型
FROM "02-AI-ML"
WHERE note_version > 0
SORT file.ctime DESC
LIMIT 10
```

## 核心概念
- [[../02-AI-ML/NLP/]] Transformer架构
- [[../02-AI-ML/CV/]] 卷积神经网络
- [[../02-AI-ML/Generative-Models/]] 扩散模型

## 交叉引用
- [[../01-Bioinformatics/]] 生物信息学应用
- [[../01-Biology/]] 生物学问题建模
EOF

echo "PaperVault 目录结构创建完成!"
echo "目录位置: $(pwd)/${VAULT_NAME}"
```

## 目录说明

| 目录 | 用途 | 说明 |
|------|------|------|
| 00-Inbox/ | 收件箱 | 新论文暂时存放，阅读后移到相应领域 |
| 01-Bioinformatics/ | 生物信息学 | 组学数据分析、工具开发等论文 |
| 01-Biology/ | 生物学 | 基础生物学研究论文 |
| 02-AI-ML/ | AI/机器学习 | 算法、模型、应用论文 |
| 03-Structural-Biology/ | 结构生物学 | 蛋白质/核酸结构解析论文 |
| 04-Other/ | 其他 | 不属于以上分类的论文 |
| Templates/ | 模板 | 各类笔记模板 |
| MOC/ | 领域地图 | 领域概览和文献索引 |
| Resources/ | 资源 | 数据库链接、工具索引等 |

## 命名规范

- 文件夹：使用 kebab-case，如 `single-cell`、`rna-seq`
- 笔记文件：使用 `{年}-{期刊}-{关键词}.md` 格式
- 图像文件夹：在笔记同目录下创建 `images/` 文件夹
