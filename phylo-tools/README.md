# Phylo-Tools：进化树批量处理工具集

三个Python脚本，用于进化树构建后的枝名批量处理。

## 工具概览

| 脚本 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `parse_fasta_headers.py` | 解析NCBI FASTA头→提取序列号+物种名→生成CSV | FASTA文件 | CSV映射表 + 可选重命名FASTA |
| `fill_csv_from_ncbi.py` | 自动识别CSV缺列→NCBI抓取填补 | 缺列的CSV | 完整CSV |
| `rename_tree_tips.py` | 用CSV映射表批量替换树文件枝名 | 树文件 + CSV | 重命名后的树文件 |

## 典型工作流

```
1. 从NCBI下载FASTA → 用脚本3提取序列号+物种名CSV
2. 如果CSV不完整 → 用脚本2从NCBI自动补全
3. 用CSV替换树文件枝名 → 用脚本1生成美化后的树文件
```

## 依赖安装

```bash
pip install biopython
```

脚本1（树文件替换）不需要BioPython，只用标准库。
脚本2和3需要BioPython来访问NCBI。

---

## 脚本1：rename_tree_tips.py

**功能**：读取CSV映射表，识别树文件枝名中的序列号，替换为物种名或整齐序列号。

```bash
# 替换为物种名
python rename_tree_tips.py -t tree.nwk -c mapping.csv --column 2 -o tree_species.nwk

# 替换为整齐序列号
python rename_tree_tips.py -t tree.nwk -c mapping.csv --column 1 -o tree_clean.nwk

# 物种名加斜体标记
python rename_tree_tips.py -t tree.nwk -c mapping.csv --column 2 --italic
```

**CSV格式**：
```csv
Accession,Species
AB123456.1,Species name
PP987654.1,Another species
```

**识别逻辑**：
- 枝名可能是 `AB123456.1_Species_name_other_stuff` 这样的长字符串
- 脚本自动提取其中的序列号（如AB123456.1），匹配CSV，替换为目标名称
- 支持Newick和Nexus格式

---

## 脚本2：fill_csv_from_ncbi.py

**功能**：自动识别CSV中缺了哪一列，从NCBI抓取数据填补。

```bash
# 自动检测并填补
python fill_csv_from_ncbi.py -c mapping.csv --email your@email.com

# 指定目标基因（用于缺序列号时的搜索）
python fill_csv_from_ncbi.py -c mapping.csv --email your@email.com --gene COI --gene-length 1550

# 指定输出路径
python fill_csv_from_ncbi.py -c mapping.csv --email your@email.com -o filled.csv
```

**识别逻辑**：
- 序列号列：包含标准NCBI格式（字母+数字+.+版本号）
- 物种名列：包含拉丁学名格式（属名+种加词）

**填补逻辑**：
- 缺序列号→搜索NCBI，优先选RefSeq参考序列，其次选最接近标准基因长度的序列
- 缺物种名→通过序列号查NCBI，获取物种学名

**常用基因长度参考**：
| 基因 | 标准长度(bp) |
|------|-------------|
| COI | 1550 |
| Cytb | 1140 |
| 16S | 600 |
| 18S | 1800 |
| 28S | 850 |
| ITS | 650 |
| 12S | 950 |

---

## 脚本3：parse_fasta_headers.py

**功能**：解析从NCBI下载的FASTA文件，提取序列号和物种名，生成CSV映射表，可选重命名。

```bash
# 仅解析生成CSV
python parse_fasta_headers.py -f sequences.fasta

# 解析+重命名为物种名
python parse_fasta_headers.py -f sequences.fasta --rename-species

# 解析+重命名为整齐序列号
python parse_fasta_headers.py -f sequences.fasta --rename-accession

# 交互模式（会询问重命名选项）
python parse_fasta_headers.py -f sequences.fasta --interactive
```

**NCBI FASTA头解析逻辑**：

NCBI头格式：`>AB123456.1 Species name mitochondrial gene for COI, complete cds`

- 第1列提取：`AB123456.1`（>后第一个空格前的序列号）
- 第2列提取：`Species name`（拉丁学名，属名首字母大写+种加词小写）
- 其余描述信息：丢弃

**重命名选项**：
- `--rename-species`：序列名改为物种名（空格变下划线，如 `Species_name`）
- `--rename-accession`：序列名改为整齐序列号（如 `AB123456.1`）
- 不加参数：仅输出CSV，不修改FASTA

---

## 注意事项

1. **NCBI限速**：脚本2每次查询间隔0.5秒，避免被NCBI封IP。大量数据时请耐心等待。
2. **编码问题**：如果FASTA文件包含中文或特殊字符，使用 `--encoding` 参数指定编码。
3. **斜体格式**：进化树绘图软件（如FigTree、iTOL）中物种名需要手动设置斜体。脚本1的 `--italic` 选项会在物种名前后加标记，方便后续处理。
4. **序列号匹配**：如果树文件中的序列号和CSV不完全一致（如带/不带版本号），脚本会尝试去掉版本号后匹配。
