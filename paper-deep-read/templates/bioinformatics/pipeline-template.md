# 生信分析流水线模板

> 本文件提供常用生物信息学分析流水线的 Mermaid 可视化模板，可直接复制使用。

---

## 一、scRNA-seq 分析流水线

### 1.1 10x Genomics 标准化流程
```mermaid
graph LR
    subgraph 输入["输入数据"]
        A1[Raw Reads<br/>FASTQ]
    end

    subgraph 预处理["预处理"]
        A1 --> B1[QC<br/>FastQC]
        B1 --> C1[Trimming<br/>Cutadapt]
        C1 --> D1[质量过滤<br/>过滤低质量 reads]
    end

    subgraph 比对["序列比对"]
        D1 --> E1[Alignment<br/>Cell Ranger]
        E1 --> F1[Barcode<br/>校正]
        F1 --> G1[UMI 计数<br/>生成 Feature-Barcode 矩阵]
    end

    subgraph 质控["细胞质控"]
        G1 --> H1[双细胞去除<br/>DoubletFinder]
        H1 --> I1[低质量细胞过滤<br/>线粒体基因%、RNA含量]
        I1 --> J1[细胞周期评分<br/>Scran]
    end

    subgraph 标准化["标准化与特征选择"]
        J1 --> K1[Normalize<br/>SCTransform]
        K1 --> L1[特征选择<br/>高变异基因]
        L1 --> M1[降维<br/>PCA]
    end

    subgraph 聚类["聚类与注释"]
        M1 --> N1[邻居计算<br/>UMAP/t-SNE]
        N1 --> O1[细胞聚类<br/>Louvain/Leiden]
        O1 --> P1[细胞类型注释<br/>SingleR/Azimuth]
    end

    subgraph 注释["下游分析"]
        P1 --> Q1[标记基因鉴定<br/>FindMarkers]
        Q1 --> R1[轨迹分析<br/>Monocle/Pseudotime]
        R1 --> S1[富集分析<br/>GO/KEGG]
    end

    subgraph 输出["输出结果"]
        S1 --> T1[可视化<br/>ggplot2/UCell]
    end

    style 输入 fill:#E9C46A,stroke:#333,stroke-width:2px
    style 预处理 fill:#F4A261,stroke:#333,stroke-width:2px
    style 比对 fill:#F4A261,stroke:#333,stroke-width:2px
    style 质控 fill:#E76F51,stroke:#333,stroke-width:2px
    style 标准化 fill:#2A9D8F,stroke:#333,stroke-width:2px
    style 聚类 fill:#264653,stroke:#333,stroke-width:2px,color:#fff
    style 注释 fill:#264653,stroke:#333,stroke-width:2px,color:#fff
    style 输出 fill:#2A9D8F,stroke:#333,stroke-width:2px
```

### 1.2 Smart-seq2 流程
```mermaid
graph LR
    A[Total RNA] --> B[mRNA 富集<br/>Poly(A) selection]
    B --> C[逆转录<br/>Oligo(dT) 引物]
    C --> D[cDNA 合成<br/>SMARTScribe]
    D --> E[PCR 扩增<br/>KAPA HiFi]
    E --> F[片段化<br/>Covaris]
    F --> G[文库构建<br/>Illumina]
    G --> H[测序<br/>NovaSeq]
    H --> I[比对<br/>STAR]
    I --> J[定量<br/>Salmon]
    J --> K[标准化<br/>DESeq2]
    K --> L[下游分析<br/>差异表达/聚类]
    L --> M[可视化]

    style A fill:#E9C46A
    style M fill:#2A9D8F
```

---

## 二、WGS/WES 分析流水线

### 2.1 全基因组测序 (WGS)
```mermaid
graph TD
    subgraph 测序["测序阶段"]
        A1[DNA 提取<br/>Qiagen DNeasy] --> B1[文库构建<br/>Illumina TruSeq]
        B1 --> C1[PCR 扩增<br/>Phi29]
        C1 --> D1[上机测序<br/>NovaSeq 6000]
    end

    subgraph 质控["原始数据质控"]
        D1 --> E1[QC<br/>FastQC]
        E1 --> F1[接头去除<br/>Trimmomatic]
        F1 --> G1[质量过滤<br/>去除低质量 reads]
    end

    subgraph 比对["序列比对"]
        G1 --> H1[比对参考基因组<br/>BWA-MEM]
        H1 --> I1[排序<br/>Samtools sort]
        I1 --> J1[去重复<br/>GATK MarkDuplicates]
    end

    subgraph 变异检测["变异检测"]
        J1 --> K1[BQSR<br/>Base Quality Score Recalibration]
        K1 --> L1[变异检测<br/>GATK HaplotypeCaller]
        L1 --> M1[变异注释<br/>ANNOVAR/Ensembl VEP]
    end

    subgraph 筛选["变异筛选"]
        M1 --> N1[人群频率过滤<br/>gnomAD]
        N1 --> O1[功能预测<br/>SIFT/PolyPhen-2]
        O1 --> P1[临床意义评估<br/>ClinVar]
    end

    subgraph 报告["报告生成"]
        P1 --> Q1[生成报告<br/>snpeff2html]
        Q1 --> R1[可视化<br/>IGV]
    end

    style 测序 fill:#E9C46A,stroke:#333
    style 质控 fill:#F4A261,stroke:#333
    style 比对 fill:#F4A261,stroke:#333
    style 变异检测 fill:#E76F51,stroke:#333
    style 筛选 fill:#2A9D8F,stroke:#333
    style 报告 fill:#264653,stroke:#333,color:#fff
```

### 2.2 全外显子测序 (WES)
```mermaid
graph LR
    A[DNA] --> B[杂交捕获<br/>Agilent SureSelect]
    B --> C[文库构建<br/>Illumina]
    C --> D[测序<br/>HiSeq]
    D --> E[QC]
    E --> F[比对<br/>BWA]
    F --> G[去重复<br/>Picard]
    G --> H[BQSR]
    H --> I[变异检测<br/>GATK]
    I --> J[变异注释<br/>ANNOVAR]
    J --> K[变异筛选<br/>人群频率+功能预测]
    K --> L[报告生成]

    style A fill:#E9C46A
    style L fill:#2A9D8F
```

---

## 三、RNA-seq 分析流水线

### 3.1 常规 mRNA-seq
```mermaid
graph LR
    subgraph 测序阶段["测序阶段"]
        A1[Total RNA] --> B1[mRNA 富集<br/>Poly(A) selection]
        B1 --> C1[逆转录<br/>Superscript IV]
        C1 --> D1[文库构建<br/>Illumina TruSeq]
        D1 --> E1[上机测序<br/>NovaSeq]
    end

    subgraph 预处理["数据预处理"]
        E1 --> F1[QC<br/>FastQC]
        F1 --> G1[质控过滤<br/>Trimmomatic]
        G1 --> H1[比对<br/>STAR]
    end

    subgraph 定量["表达定量"]
        H1 --> I1[计数<br/>featureCounts]
        I1 --> J1[标准化<br/>DESeq2/edgeR]
        J1 --> K1[TPM/FPKM]
    end

    subgraph 差异分析["差异表达分析"]
        K1 --> L1[差异表达<br/>DESeq2]
        L1 --> M1[p值校正<br/>BH FDR]
        M1 --> N1[阈值筛选<br/>|log2FC|>1 & padj<0.05]
    end

    subgraph 下游["下游分析"]
        N1 --> O1[GO 富集分析]
        O1 --> P1[KEGG 通路分析]
        P1 --> Q1[GSEA]
        Q1 --> R1[蛋白互作网络<br/>STRING]
    end

    style 测序阶段 fill:#E9C46A
    style 预处理 fill:#F4A261
    style 定量 fill:#F4A261
    style 差异分析 fill:#E76F51
    style 下游 fill:#2A9D8F
```

### 3.2 链特异性 RNA-seq
```mermaid
graph LR
    A[Total RNA] --> B[rRNA 去除<br/>RiboMinus]
    B --> C[片段化<br/>Mg2+ 离子]
    C --> D[逆转录<br/>dUTP 法]
    D --> E[第二链合成<br/>DNA Pol I]
    E --> F[末端修复<br/>T4 DNA Pol]
    F --> G[加 A 尾]
    G --> H[接头连接<br/>T4 DNA Ligase]
    H --> I[PCR 扩增<br/>Phusion]
    I --> J[测序<br/>Illumina]
    J --> K[QC]
    K --> L[比对<br/>STAR - strandSpecific]
    L --> M[计数<br/>featureCounts - strandSpecific]
    M --> N[标准化<br/>DESeq2]
    N --> O[差异表达]
    O --> P[可视化<br/>IGV]

    style A fill:#E9C46A
    style P fill:#2A9D8F
```

---

## 四、ChIP-seq 分析流水线

### 4.1 标准流程
```mermaid
graph TD
    subgraph 实验阶段["实验阶段"]
        A1[细胞固定<br/>1%甲醛] --> B1[染色质破碎<br/>超声/Covaris]
        B1 --> C1[免疫沉淀<br/>IP抗体]
        C1 --> D1[交联解除<br/>NaCl]
        D1 --> E1[DNA 纯化<br/>Phenol/Chloroform]
    end

    subgraph 测序["测序阶段"]
        E1 --> F1[文库构建<br/>NEBNext]
        F1 --> G1[PCR 扩增<br/>KAPA]
        G1 --> H1[上机测序<br/>HiSeq]
    end

    subgraph 分析["数据分析"]
        H1 --> I1[QC<br/>FastQC]
        I1 --> J1[比对参考基因组<br/>BWA]
        J1 --> K1[去重复<br/>Picard]
        K1 --> L1[peak calling<br/>MACS2]
    end

    subgraph 注释["Peak 注释"]
        L1 --> M1[peak 注释<br/>Homer annotatePeaks]
        M1 --> N1[motif 分析<br/>Homer findMotifs]
        N1 --> O1[富集分析<br/>GREAT]
    end

    subgraph 可视化["可视化"]
        O1 --> P1[基因组浏览器<br/>IGV]
        P1 --> Q1[热图<br/>deepTools plotHeatmap]
        Q1 --> R1[峰分布图<br/>ChIPseeker]
    end

    style 实验阶段 fill:#E9C46A
    style 测序 fill:#F4A261
    style 分析 fill:#F4A261
    style 注释 fill:#E76F51
    style 可视化 fill:#2A9D8F
```

### 4.2 CUT&RUN 流程
```mermaid
graph LR
    A[活细胞] --> B[ConA beads 结合]
    B --> C[穿孔<br/>Activated Tamxin]
    C --> D[一抗孵育<br/>目标蛋白抗体]
    D --> E[pAG-Tn5 结合]
    E --> F[Tn5 转座<br/>tagmentation]
    F --> G[DNA 片段化<br/>EDTA 终止]
    G --> H[DNA 纯化<br/>MinElute]
    H --> I[PCR 扩增<br/>Nextera]
    I --> J[片段大小选择<br/>SPRIselect]
    J --> K[测序<br/>NovaSeq]
    K --> L[比对<br/>BWA]
    L --> M[Peak calling<br/>MACS2]
    M --> N[下游分析<br/>motif/富集]

    style A fill:#E9C46A
    style N fill:#2A9D8F
```

---

## 五、Chip-seq vs ATAC-seq 对比
```mermaid
graph TD
    subgraph 共同步骤["共同步骤"]
        A1[QC] --> B1[比对<br/>BWA/STAR]
        B1 --> C1[去重复]
        C1 --> D1[Peak calling<br/>MACS2]
        D1 --> E1[注释]
        E1 --> F1[可视化]
    end

    subgraph Chip特定["ChIP-seq 特有"]
        A1 --> G1[甲醛交联]
        G1 --> H1[超声破碎]
        H1 --> I1[免疫沉淀]
        I1 --> J1[解交联]
    end

    subgraph ATAC特定["ATAC-seq 特有"]
        A1 --> K1[细胞核制备]
        K1 --> L1[Tn5 转座<br/>tagmentation]
        L1 --> M1[片段选择<br/>去除线粒体]
    end

    style 共同步骤 fill:#2A9D8F,color:#fff
    style Chip特定 fill:#F4A261
    style ATAC特定 fill:#E76F51
```

---

## 六、通用分析流水线模板

### 6.1 模板结构
```mermaid
graph TD
    subgraph 输入["输入阶段"]
        A[原始数据<br/>{{数据类型}}]
    end

    subgraph 预处理["预处理阶段"]
        A --> B[质量控制<br/>{{质控工具}}]
        B --> C[数据过滤<br/>{{过滤标准}}]
    end

    subgraph 分析["分析阶段"]
        C --> D[主分析方法<br/>{{方法1}}]
        D --> E[辅助分析<br/>{{方法2}}]
        E --> F[验证分析<br/>{{方法3}}]
    end

    subgraph 输出["输出阶段"]
        F --> G[结果整理<br/>{{整理工具}}]
        G --> H[可视化<br/>{{可视化工具}}]
        H --> I[报告生成<br/>{{报告格式}}]
    end

    style 输入 fill:#E9C46A
    style 预处理 fill:#F4A261
    style 分析 fill:#E76F51
    style 输出 fill:#2A9D8F
```

### 6.2 自定义示例
```mermaid
graph LR
    subgraph 数据准备
        A[样本数据] --> B[样本信息表]
    end

    subgraph QC
        B --> C[表达矩阵 QC]
        C --> D{质控通过?}
        D -->|否| E[重采样/过滤]
        E --> C
        D -->|是| F[保留合格样本]
    end

    subgraph 标准化
        F --> G[Normalization<br/>TPM/FPKM]
        G --> H[批次效应校正<br/>ComBat]
    end

    subgraph 差异分析
        H --> I[差异检验<br/>limma/DESeq2]
        I --> J[多重检验校正<br/>BH FDR]
        J --> K[阈值筛选]
    end

    subgraph 功能分析
        K --> L[GO 富集]
        K --> M[KEGG 通路]
        K --> N[GSEA]
    end

    subgraph 可视化
        L --> O[热图]
        M --> P[通路图]
        N --> Q[富集图]
    end

    style 数据准备 fill:#E9C46A
    style QC fill:#F4A261
    style 标准化 fill:#F4A261
    style 差异分析 fill:#E76F51
    style 功能分析 fill:#264653,color:#fff
    style 可视化 fill:#2A9D8F
```

---

## 七、流水线参数速查

### 7.1 工具版本推荐
| 分析类型 | 工具 | 推荐版本 | 备注 |
|----------|------|----------|------|
| RNA-seq比对 | STAR | 2.7.x | 支持链特异性 |
| RNA-seq比对 | HISAT2 | 2.2.x | 低内存 |
| 变异检测 | GATK | 4.3.x | Best Practice |
| Peak calling | MACS2 | 2.2.x | ChIP-seq/ATAC-seq |
| 差异表达 | DESeq2 | 1.38.x | R包 |
| 单细胞聚类 | Seurat | 4.3.x | R包 |
| 单细胞分析 | Scanpy | 1.9.x | Python |

### 7.2 常用参数配置
| 工具 | 参数 | 推荐值 | 说明 |
|------|------|--------|------|
| FastQC | --threads | 4-8 | 线程数 |
| Trimmomatic | ILLUMINACLIP | TruSeq3:2:30:10 | 接头序列 |
| STAR | --outSAMtype | BAM SortedByCoordinate | 输出格式 |
| featureCounts | -t | exon | 计数特征类型 |
| MACS2 | --qvalue | 0.05 | 显著性阈值 |

---

## 八、常见问题排查

### 8.1 流程失败检查点
```mermaid
graph TD
    A[流程失败] --> B{错误信息类型}
    B -->|内存不足| C[增加 -mem 或减少样本]
    B -->|磁盘空间不足| D[清理临时文件]
    B -->|样本匹配失败| E[检查样本命名]
    B -->|工具版本冲突| F[检查依赖版本]
    C --> G[重新运行]
    D --> G
    E --> G
    F --> G
```

### 8.2 常见问题与解决方案
| 步骤 | 问题 | 可能原因 | 解决方案 |
|------|------|----------|----------|
| QC | GC bias | 偏好性扩增 | 换用其他建库方式 |
| 比对 | 比对率低 | 测序质量/污染 | 检查原始数据 |
| 标准化 | 批次效应强 | 实验批次差异 | ComBat校正 |
| 差异分析 | 差异基因少 | 阈值设置过严 | 放宽padj阈值 |
| 富集分析 | 无显著富集 | 功能注释过时 | 更新数据库版本 |