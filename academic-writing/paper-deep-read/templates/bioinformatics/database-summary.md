# 数据库资源汇总模板

> 本文件用于系统记录生物信息学研究中常用的数据库资源，按类别整理。

---

## 一、数据库记录模板

### 通用记录格式
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| {{数据库名}} | {{如SRS000001}} | {{数据类型}} | HTTP/FTP/API | {{URL}} | {{备注}} |

### 记录示例
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| GEO | GSM000000 | 表达谱原始数据 | HTTP | https://www.ncbi.nlm.nih.gov/geo/ | 需注册 |
| SRA | SRR000000 | 测序原始数据 | HTTP/Aspera | https://www.ncbi.nlm.nih.gov/sra/ | 支持Aspera加速 |

---

## 二、序列数据库

### 2.1 核酸序列数据库
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| NCBI GenBank | {{如NM_001256799}} | 核酸序列 | HTTP/FTP | https://www.ncbi.nlm.nih.gov/genbank/ | 每日更新 |
| EMBL-EBI ENA | {{如ENST00000371385}} | 核酸序列 | HTTP/FTP/API | https://www.ebi.ac.uk/ena/ | 欧洲数据源 |
| DDBJ | {{如NM_001256799}} | 核酸序列 | HTTP | https://www.ddbj.nig.ac.jp/ | 日本数据源 |
| RefSeq | {{如NM_001198}} | 经审校序列 | HTTP/FTP | https://www.ncbi.nlm.nih.gov/refseq/ | 非冗余 |

### 2.2 蛋白质序列数据库
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| UniProtKB/Swiss-Prot | {{如P05387}} | 蛋白质序列/功能 | HTTP/API | https://www.uniprot.org/ | 人工审校 |
| UniProtKB/TrEMBL | {{如A0A023IWs6}} | 蛋白质序列 | HTTP/API | https://www.uniprot.org/ | 计算预测 |
| PIR | {{如PIRSR000000}} | 蛋白质序列 | HTTP | https://proteininformationresource.org/ | 蛋白质信息资源 |
| RefSeq Protein | {{如NP_001189}} | 蛋白质序列 | HTTP/FTP | https://www.ncbi.nlm.nih.gov/refseq/ | 与核酸RefSeq对应 |

---

## 三、基因组数据库

### 3.1 基因组浏览器
| 数据库 | ID格式 | 基因组版本 | 访问方式 | 链接 | 备注 |
|--------|--------|------------|----------|------|------|
| UCSC Genome Browser | {{如hg38}} | hg19/hg38/mm10 | HTTP | https://genome.ucsc.edu/ | 快速可视化 |
| Ensembl | {{如ENSG00000139618}} | GRCh37/GRCh38 | HTTP/API | https://www.ensembl.org/ | 包含基因注释 |
| NCBI Genome | {{如GCF_000001405}} | 多种物种 | HTTP/FTP | https://www.ncbi.nlm.nih.gov/genome/ | 基因组目录 |
| IGV | 本地安装 | 多种格式 | 桌面应用 | https://software.broadinstitute.org/igv/ | 高性能本地浏览器 |

### 3.2 物种特异性基因组
| 物种 | 数据库 | 基因组版本 | 链接 | 备注 |
|------|--------|------------|------|------|
| 人类 | UCSC/Ensembl | hg38 | https://genome.ucsc.edu/ | 最新版本hg38 |
| 小鼠 | UCSC/Ensembl | mm39 | https://genome.ucsc.edu/ | 最新版本mm39 |
| 大鼠 | UCSC/Ensembl | rn7 | https://genome.ucsc.edu/ | 最新版本rn7 |
| 斑马鱼 | UCSC/Ensembl | danRer11 | https://genome.ucsc.edu/ | 鱼类模型 |
| 酵母 | SGD | R64 | https://www.yeastgenome.org/ |酿酒酵母专用 |
| 拟南芥 | TAIR | TAIR10 | https://www.arabidopsis.org/ | 植物模型 |

---

## 四、基因表达数据库

### 4.1 高通量表达数据
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| NCBI GEO | {{如GSE00000}} | 表达谱 | HTTP | https://www.ncbi.nlm.nih.gov/geo/ | 支持series |
| ArrayExpress | {{如E-MTAB-000}} | 表达谱 | HTTP/API | https://www.ebi.ac.uk/arrayexpress/ | 支持已处理数据 |
| EMBL-EBI Expression Atlas | {{如E-MTAB-000}} | 差异表达 | HTTP | https://www.ebi.ac.uk/gxa/ | 支持跨物种比较 |
| SRA | {{如SRP000000}} | 原始测序数据 | HTTP/Aspera | https://www.ncbi.nlm.nih.gov/sra/ | RNA-seq原始数据 |

### 4.2 组织特异性表达
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| GTEx Portal | {{如GTEX-00000}} | 组织表达 | HTTP | https://gtexportal.org/ | 人体多组织表达 |
| Human Protein Atlas | {{如ENST000000}} | 蛋白表达 | HTTP | https://www.proteinatlas.org/ | 含免疫组化数据 |
| FANTOM5 | {{如FANTOM00000}} | 启动子活性 | HTTP | https://fantom.gsc.riken.jp/ | 人类转录图谱 |
| Encode | {{如ENC000000}} | 多组学数据 | HTTP | https://www.encodeproject.org/ | ENCODE项目 |

---

## 五、变异数据库

### 5.1 SNP/突变数据库
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| dbSNP | {{如rs000000}} | 单核苷酸多态性 | HTTP/FTP | https://www.ncbi.nlm.nih.gov/snp/ | 人类遗传变异 |
| ClinVar | {{如RCV000000}} | 临床相关变异 | HTTP/API | https://www.ncbi.nlm.nih.gov/clinvar/ | 变异临床意义 |
| gnomAD | {{如00001}} | 人群变异频率 | HTTP | https://gnomad.broadinstitute.org/ | 外显子组+基因组 |
| DbsSNP138 | {{如rs000000}} | SNP | HTTP | https://www.ncbi.nlm.nih.gov/snp/ | 版本标注 |

### 5.2 癌症变异数据库
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| COSMIC | {{如COSM00000}} | 癌症体细胞突变 | HTTP | https://cancer.sanger.ac.uk/cosmic/ | Sanger研究所 |
| cBioPortal | {{如00000}} | 癌症多组学 | HTTP | https://www.cbioportal.org/ | TCGA+ICGC |
| ICGC | {{如00000}} | 癌症基因组 | HTTP | https://icgc.org/ | 国际癌症基因组联盟 |
| TumorPortal | {{如00000}} | 癌症驱动突变 | HTTP | http://tumorportal.org/ | 癌症特异性变异 |

---

## 六、通路和功能数据库

### 6.1 代谢通路
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| KEGG | {{如PATH:map00010}} | 代谢/信号通路 | HTTP/API | https://www.kegg.jp/ | 经典通路数据库 |
| Reactome | {{如R-HSA-00000}} | 分子通路 | HTTP/API | https://reactome.org/ | 人工审校通路 |
| BioCyc | {{如ECOLI}} | 代谢通路 | HTTP | https://biocyc.org/ | 多种物种代谢 |
| MetaCyc | {{如META:ARG}} | 代谢反应 | HTTP | https://metacyc.org/ | 非冗余代谢数据库 |

### 6.2 信号通路
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| NCI-Nature PID | {{如20124}} | 信号通路 | HTTP | https://pid.nci.nih.gov/ | Nature出品 |
| Panther | {{如P00000}} | 信号通路 | HTTP | http://www.pantherdb.org/ | GO分类系统 |
| Signalink | {{如00000}} | 信号网络 | HTTP | http://csbd.bgu.ac.il/signalink/ | 人类信号网络 |
| WikiPathways | {{如WP0000}} | 社区通路 | HTTP/API | https://www.wikipathways.org/ | 开放协作 |

---

## 七、基因功能注释数据库

### 7.1 Gene Ontology 相关
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| Gene Ontology | {{如GO:000000}} | 基因功能 | HTTP | http://geneontology.org/ | GO注释 |
| AmiGO | {{如GO:000000}} | GO浏览器 | HTTP | http://amigo.geneontology.org/ | GO检索 |
| QuickGO | {{如GO:000000}} | GO浏览器 | HTTP | https://www.ebi.ac.uk/QuickGO/ | EBI出品 |

### 7.2 疾病关联
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| OMIM | {{如OMIM:000000}} | 遗传疾病 | HTTP | https://www.omim.org/ | 在线人类孟德尔遗传 |
| Orphanet | {{如ORPHA:00000}} | 罕见病 | HTTP | https://www.orpha.net/ | 欧洲罕见病数据库 |
| DisGeNET | {{如C0000000}} | 基因-疾病关联 | HTTP/API | https://www.disgenet.org/ | 综合疾病网络 |
| GAD | {{如000000}} | 基因-疾病关联 | HTTP | https://geneticassociationdb.nih.gov/ | 美国NIH |

---

## 八、蛋白质数据库

### 8.1 蛋白质结构
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| PDB | {{如1ABC}} | 蛋白质结构 | HTTP/FTP | https://www.rcsb.org/ | 实验解析结构 |
| AlphaFold DB | {{如AF-A0A023IWs6}} | 预测结构 | HTTP | https://alphafold.ebi.ac.uk/ | DeepMind预测 |
| SWISS-MODEL | {{如Q00000}} | 同源建模 | HTTP | https://swissmodel.expasy.org/ | 自动建模 |
| Pfam | {{如PF00000}} | 蛋白质家族 | HTTP | https://pfam.xfam.org/ | 隐马尔可夫模型 |

### 8.2 蛋白质互作
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| STRING | {{如9606.ENSP00000}} | 蛋白互作网络 | HTTP/API | https://string-db.org/ | 功能关联 |
| BioGRID | {{如00000}} | 蛋白互作 | HTTP/API | https://thebiogrid.org/ | 酵母双杂交等 |
| IntAct | {{如EBI-00000}} | 分子互作 | HTTP/API | https://www.ebi.ac.uk/intact/ | IMEx联盟 |
| DIP | {{如00000}} | 蛋白互作 | HTTP | https://dip.doe-mbi.ucla.edu/ | 蛋白质互作数据库 |

---

## 九、单细胞数据库

| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| Single Cell Portal | {{如SCP00000}} | 单细胞数据 | HTTP | https://singlecell.broadinstitute.org/ | Broad研究所 |
| HCA | {{如00000}} | 人体细胞图谱 | HTTP | https://data.humancellatlas.org/ | 人类细胞图谱 |
| PanglaoDB | {{如SRS000000}} | 单细胞RNA-seq | HTTP | https://panglaodb.se/ | 公共数据整合 |
| Single Cell Expression Atlas | {{如E-MTAB-000}} | 单细胞表达 | HTTP | https://www.ebi.ac.uk/gxa/sc/ | EBI出品 |
| scRNASeqDB | {{如GSE00000}} | 单细胞RNA-seq | HTTP | https://scrnaseqdb.crc.utoronto.ca/ | 人类单细胞 |

---

## 十、其他专业数据库

### 10.1 表观基因组
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| Roadmap Epigenomics | {{如00000}} | 表观修饰 | HTTP | https://www.roadmapepigenomics.org/ | 人类表观组 |
| IHEC | {{如E00000}} | 表观组数据 | HTTP | http://ihec-epigenomes.org/ | 国际人类表观组联盟 |
| dbSUPER | {{如00000}} | 超增强子 | HTTP | https://asiacoimm.bitbucket.io/dbSUPER/ | 超级增强子 |
| EnhancerAtlas | {{如00000}} | 增强子 | HTTP | https://enhanceratlas.org/ | 增强子注释 |

### 10.2 微生物组
| 数据库 | ID格式 | 数据类型 | 访问方式 | 链接 | 备注 |
|--------|--------|----------|----------|------|------|
| MG-RAST | {{如mgp00000}} | 宏基因组 | HTTP | https://www.mg-rast.org/ | 宏基因组分析 |
| IMG/M | {{如000000}} | 微生物组 | HTTP | https://img.jgi.doe.gov/m/ | DOE出品 |
| Greengenes | {{如000000}} | 16S rRNA | HTTP | https://greengenes.secondgenome.com/ | 细菌分类 |
| SILVA | {{如000000}} | rRNA | HTTP | https://www.arb-silva.de/ | rRNA数据库 |

---

## 十一、数据访问方式汇总

### 11.1 HTTP 下载
```bash
# 直接下载
wget https://example.com/datafile.gz

# 递归下载目录
wget -r -np --cut-dirs=2 https://example.com/directory/
```

### 11.2 FTP 下载
```bash
# FTP 连接
ftp ftp.ncbi.nlm.nih.gov
cd /blast/db/
get refseq_viral.1.1.genomic.fna.gz
bye
```

### 11.3 Aspera 高速下载
```bash
# 安装 asperaconnect 后使用
ascp -i ~/aspera/connect/etc/asperaweb_id_dsa.pub \
     -k 1 -T -l 300m \
     anonftp@ftp.ncbi.nlm.nih.gov:genomes/all/GSE00000/ .
```

### 11.4 API 查询
```python
# Python 示例：NCBI Entrez API
import requests

def search_ncbi(query, db="pubmed"):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    params = {
        "db": db,
        "term": query,
        "retmax": 10,
        "retmode": "json"
    }
    response = requests.get(base_url + "esearch.fcgi", params=params)
    return response.json()
```

---

## 十二、数据库更新记录

| 数据库 | 最近更新 | 更新频率 | 检查方式 |
|--------|----------|----------|----------|
| NCBI GenBank | {{日期}} | 每日 | https://www.ncbi.nlm.nih.gov/news |
| UniProt | {{日期}} | 每周 | https://www.uniprot.org/news |
| PDB | {{日期}} | 每日 | https://www.rcsb.org/news |
| KEGG | {{日期}} | 每月 | https://www.kegg.jp/kegg/update.html |
| GTEx | {{日期}} | 定期 | https://gtexportal.org/home/pages |
