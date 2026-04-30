---
tags:
  - pandas
  - Python
  - 数据处理
  - 生信
  - 实战代码
  - 一键运行
aliases:
  - pandas代码库
  - DataFrame速查
  - Python数据处理宝典
  - 生信Python实战
created: 2026-04-20
updated: 2026-04-20
version: pandas 2.x
description: Python pandas 数据处理实战代码库，覆盖生信数据处理90%场景，封装函数+一键脚本，改参数即跑
---

# 🐼 Pandas 实战代码库

> **定位**：复制→改参数→直接跑。覆盖 Python 数据处理全场景，从数据清洗到统计汇总，生信场景全覆盖。
> 基于 **pandas 2.x**，含 DataFrame 操作、数据清洗、分组聚合、合并连接、时间序列、性能优化。

---

## 📑 快速导航

| 需求 | 跳转 |
|------|------|
| 环境安装 | [[#📦 环境安装]] |
| 数据读取与导出 | [[#📂 数据读取与导出]] |
| DataFrame 基础操作 | [[#🔧 DataFrame 基础操作]] |
| 数据筛选与过滤 | [[#🔍 数据筛选与过滤]] |
| 数据清洗与预处理 | [[#🧹 数据清洗与预处理]] |
| 分组聚合 | [[#📊 分组聚合]] |
| 合并连接与重塑 | [[#🔗 合并连接与重塑]] |
| 字符串与文本处理 | [[#✂️ 字符串与文本处理]] |
| 生信实战封装 | [[#🧬 生信实战封装]] |
| 一键数据处理流水线 | [[#🚀 一键数据处理流水线]] |
| 性能优化 | [[#⚡ 性能优化]] |
| 函数速查表 | [[#📋 函数速查表]] |

---

## 📦 环境安装

```python
# ============================================================
# pandas + 生信 Python 全家桶
# ============================================================

# 核心数据处理
# pip install pandas numpy scipy

# 生信增强
# pip install scanpy anndata           # 单细胞分析
# pip install biopython                # 生物信息
# pip install gseapy                   # 富集分析
# pip install mygene                   # 基因ID转换

# 可视化
# pip install matplotlib seaborn plotly

# 数据读取
# pip install openpyxl xlrd           # Excel
# pip install pyarrow fastparquet     # Parquet
# pip install h5py                    # HDF5

# 验证安装
import pandas as pd
import numpy as np
print(f"pandas版本: {pd.__version__}")
print(f"numpy版本: {np.__version__}")

# 常用设置
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', '{:.4f}'.format)
pd.set_option('display.width', 200)
```

---

## 📂 数据读取与导出

```python
# ============================================================
# 通用读取函数 —— 自动识别格式
# ============================================================
import pandas as pd
import os

def smart_read(file_path, **kwargs):
    """根据文件扩展名自动选择读取方式"""
    ext = os.path.splitext(file_path)[1].lower()
    readers = {
        '.csv':  lambda: pd.read_csv(file_path, **kwargs),
        '.tsv':  lambda: pd.read_csv(file_path, sep='\t', **kwargs),
        '.txt':  lambda: pd.read_csv(file_path, sep='\t', **kwargs),
        '.xlsx': lambda: pd.read_excel(file_path, **kwargs),
        '.xls':  lambda: pd.read_excel(file_path, **kwargs),
        '.parquet': lambda: pd.read_parquet(file_path, **kwargs),
        '.feather': lambda: pd.read_feather(file_path, **kwargs),
        '.h5':   lambda: pd.read_hdf(file_path, **kwargs),
        '.hdf5': lambda: pd.read_hdf(file_path, **kwargs),
        '.json': lambda: pd.read_json(file_path, **kwargs),
        '.pkl':  lambda: pd.read_pickle(file_path, **kwargs),
    }
    if ext not in readers:
        raise ValueError(f"不支持的格式: {ext}")
    return readers[ext]()

# 使用
# df = smart_read("counts.csv")
# df = smart_read("data.xlsx", sheet_name="Sheet1")
# df = smart_read("results.tsv")

# ============================================================
# 通用导出函数
# ============================================================
def smart_write(df, file_path, **kwargs):
    """根据文件扩展名自动选择导出方式"""
    ext = os.path.splitext(file_path)[1].lower()
    writers = {
        '.csv':  lambda: df.to_csv(file_path, index=False, **kwargs),
        '.tsv':  lambda: df.to_csv(file_path, sep='\t', index=False, **kwargs),
        '.xlsx': lambda: df.to_excel(file_path, index=False, **kwargs),
        '.parquet': lambda: df.to_parquet(file_path, index=False, **kwargs),
        '.feather': lambda: df.to_feather(file_path, **kwargs),
        '.json': lambda: df.to_json(file_path, **kwargs),
        '.pkl':  lambda: df.to_pickle(file_path, **kwargs),
    }
    if ext not in writers:
        raise ValueError(f"不支持的格式: {ext}")
    writers[ext]()
    print(f"✅ 已保存: {file_path}")

# ============================================================
# 批量读取
# ============================================================
def batch_read(directory, pattern="*.csv", merge=True, add_source=True):
    """批量读取同一目录下的文件"""
    import glob
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        raise FileNotFoundError(f"未找到匹配 {pattern} 的文件")
    
    print(f"找到 {len(files)} 个文件")
    dfs = {}
    for f in files:
        name = os.path.basename(f)
        df = smart_read(f)
        if add_source:
            df['_source_file'] = name
        dfs[name] = df
    
    if merge:
        return pd.concat(dfs.values(), ignore_index=True)
    return dfs

# ============================================================
# 生信特殊格式读取
# ============================================================

def read_gmt(gmt_file):
    """读取 GSEA GMT 基因集文件"""
    genesets = []
    with open(gmt_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            genesets.append({
                'geneset': parts[0],
                'description': parts[1],
                'genes': parts[2:]
            })
    return pd.DataFrame(genesets).explode('genes')

def read_fasta(fasta_file):
    """读取 FASTA 文件"""
    records = []
    current_header = None
    current_seq = []
    
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_header:
                    records.append({
                        'header': current_header,
                        'sequence': ''.join(current_seq)
                    })
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
        
        if current_header:
            records.append({
                'header': current_header,
                'sequence': ''.join(current_seq)
            })
    
    return pd.DataFrame(records)

def read_gtf(gtf_file, feature_type='gene'):
    """读取 GTF 基因注释文件"""
    df = pd.read_csv(gtf_file, sep='\t', comment='#',
                     header=None,
                     names=['seqname','source','feature','start','end','score','strand','frame','attribute'])
    
    # 筛选特征类型
    if feature_type:
        df = df[df['feature'] == feature_type]
    
    # 解析 attribute 列
    def parse_attribute(attr_str):
        attrs = {}
        for item in attr_str.split(';'):
            item = item.strip()
            if ' ' in item:
                key, value = item.split(' ', 1)
                attrs[key] = value.strip('"')
        return attrs
    
    attr_df = df['attribute'].apply(parse_attribute).apply(pd.Series)
    return pd.concat([df.drop('attribute', axis=1), attr_df], axis=1)

def read_vcf(vcf_file):
    """读取 VCF 变异文件（简化版）"""
    # 跳过注释行
    with open(vcf_file, 'r') as f:
        header = None
        for line in f:
            if line.startswith('#CHROM'):
                header = line.strip().lstrip('#').split('\t')
                break
    
    return pd.read_csv(vcf_file, sep='\t', comment='#', header=None,
                       names=header if header else None)
```

---

## 🔧 DataFrame 基础操作

```python
# ============================================================
# 创建 DataFrame
# ============================================================

# 从字典
df = pd.DataFrame({
    'gene': ['TP53', 'BRCA1', 'EGFR', 'MYC', 'KRAS'],
    'log2FC': [2.3, -1.8, 3.1, 1.5, -0.8],
    'pvalue': [1e-10, 5e-8, 1e-15, 1e-4, 0.3],
    'cluster': ['A', 'B', 'A', 'C', 'B']
})

# 从 NumPy 数组
df = pd.DataFrame(np.random.randn(100, 5), columns=['PC1','PC2','PC3','PC4','PC5'])

# 从文件
df = smart_read("expression.csv", index_col=0)  # 第一列作为索引

# ============================================================
# 查看数据
# ============================================================
df.head()                    # 前5行
df.head(10)                  # 前10行
df.tail()                    # 后5行
df.shape                     # (行数, 列数)
df.columns.tolist()          # 列名列表
df.index.tolist()            # 索引列表
df.dtypes                    # 数据类型
df.info()                    # 概览（类型+非空数+内存）
df.describe()                # 数值统计
df.describe(include='all')   # 所有列统计
df.nunique()                 # 每列唯一值数
df.memory_usage()            # 内存占用

# 快速概览封装
def quick_overview(df, name="DataFrame"):
    """数据框快速概览"""
    print(f"=== {name} 概览 ===")
    print(f"形状: {df.shape[0]} 行 × {df.shape[1]} 列")
    print(f"内存: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print(f"\n数据类型:\n{df.dtypes.value_counts()}")
    print(f"\n缺失值:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\n数值列统计:\n{df.describe().round(2)}")

# ============================================================
# 选择列
# ============================================================
df['gene']                           # 单列（Series）
df[['gene', 'log2FC']]              # 多列
df.gene                              # 属性访问（列名无空格时）

# 按条件选列
df.select_dtypes(include='number')          # 数值列
df.select_dtypes(include='object')          # 字符串列
df.select_dtypes(exclude='number')          # 非数值列
df.filter(like='count')                      # 列名含count
df.filter(regex='^PC\\d+$')                  # 正则匹配
df.filter(items=['gene', 'log2FC'])          # 指定列

# ============================================================
# 选择行
# ============================================================
df.iloc[0]                    # 第0行（按位置）
df.iloc[0:5]                  # 前5行
df.loc['TP53']                # 按索引标签
df.loc[:, 'gene':'pvalue']   # 按标签切片

# ============================================================
# 同时选行列
# ============================================================
df.loc[df['cluster'] == 'A', ['gene', 'log2FC']]    # 筛选+选列
df.iloc[0:10, 0:3]                                   # 按位置切片
df.at[0, 'gene']                                     # 单个值（最快）
df.iat[0, 0]                                         # 按位置取单个值

# ============================================================
# 重命名
# ============================================================
df.rename(columns={'log2FC': 'log2_fold_change'})           # 列重命名
df.rename(columns=str.upper)                                  # 全部大写
df.rename(columns=lambda x: x.replace('.', '_'))              # 点换下划线
df.set_index('gene')                                          # 设置索引
df.reset_index()                                              # 重置索引
df.reset_index(drop=True)                                     # 重置索引不保留
```

---

## 🔍 数据筛选与过滤

```python
# ============================================================
# 条件筛选
# ============================================================

# 单条件
df[df['pvalue'] < 0.05]
df[df['cluster'] == 'A']
df[df['gene'].str.contains('MT-')]            # 字符串包含

# 多条件
df[(df['pvalue'] < 0.05) & (df['log2FC'] > 1)]          # 且
df[(df['cluster'] == 'A') | (df['cluster'] == 'B')]      # 或
df[~df['gene'].str.startswith('RP')]                      # 非（排除核糖体基因）

# isin 多值匹配
df[df['gene'].isin(['TP53', 'BRCA1', 'EGFR'])]
df[~df['gene'].isin(['ACTB', 'GAPDH'])]                   # 排除

# between 范围
df[df['log2FC'].between(-1, 1)]

# query 方法（更可读）
df.query("pvalue < 0.05 and log2FC > 1")
df.query("cluster in ['A', 'B']")
df.query("log2FC.abs() > 1")

# ============================================================
# 按索引筛选
# ============================================================
genes_of_interest = ['TP53', 'BRCA1', 'EGFR']
df_filtered = df.loc[df.index.intersection(genes_of_interest)]    # 索引匹配

# ============================================================
# 分组取 Top N
# ============================================================
def group_top_n(df, group_col, value_col, n=5, ascending=False):
    """每组取 top N"""
    return df.groupby(group_col, group_keys=False).apply(
        lambda x: x.nlargest(n, value_col) if not ascending else x.nsmallest(n, value_col)
    ).reset_index(drop=True)

# 使用: group_top_n(df, 'cluster', 'log2FC', n=3)

# ============================================================
# 去重
# ============================================================
df.drop_duplicates()                          # 完全去重
df.drop_duplicates(subset='gene')             # 按列去重（保留第一个）
df.drop_duplicates(subset='gene', keep='last') # 保留最后一个
df.drop_duplicates(subset=['gene', 'cluster']) # 多列去重

# 去重后保留所有信息
df.drop_duplicates(subset='gene', keep=False)   # 只保留不重复的

# ============================================================
# 采样
# ============================================================
df.sample(n=100)                     # 随机抽100行
df.sample(frac=0.1)                  # 随机抽10%
df.sample(n=100, random_state=42)    # 可重复采样
```

---

## 🧹 数据清洗与预处理

```python
# ============================================================
# 缺失值处理
# ============================================================

# 检测
df.isnull().sum()                           # 每列缺失数
df.isnull().mean() * 100                    # 每列缺失百分比
df.isnull().any(axis=1).sum()               # 有缺失的行数

# 删除
df.dropna()                                  # 删除有缺失的行
df.dropna(subset=['pvalue', 'log2FC'])       # 指定列
df.dropna(how='all')                         # 全部为NA才删除
df.dropna(thresh=3)                          # 至少3个非NA才保留
df.dropna(axis=1)                            # 删除有缺失的列
df.dropna(axis=1, thresh=len(df)*0.8)        # 保留≥80%非NA的列

# 填充
df.fillna(0)                                 # 用0填充
df.fillna({'pvalue': 1, 'log2FC': 0})        # 按列指定填充值
df.fillna(df.median(numeric_only=True))       # 用中位数填充
df.fillna(method='ffill')                     # 前向填充
df.fillna(method='bfill')                     # 后向填充

# ============================================================
# 类型转换
# ============================================================
df['pvalue'] = df['pvalue'].astype(float)              # 转浮点
df['count'] = df['count'].astype(int)                  # 转整数
df['cluster'] = df['cluster'].astype('category')       # 转分类（省内存）
df['sample_id'] = df['sample_id'].astype(str)          # 转字符串

# 智能类型转换
df = df.convert_dtypes()                               # 自动推断最优类型

# ============================================================
# 异常值处理
# ============================================================

# MAD 法去除离群值
def remove_outliers_mad(df, col, k=3, group_col=None):
    """MAD法去除离群值"""
    if group_col:
        def _remove(group):
            med = group[col].median()
            mad = (group[col] - med).abs().median() * 1.4826
            return group[(group[col] - med).abs() <= k * mad]
        return df.groupby(group_col, group_keys=False).apply(_remove).reset_index(drop=True)
    else:
        med = df[col].median()
        mad = (df[col] - med).abs().median() * 1.4826
        return df[(df[col] - med).abs() <= k * mad]

# IQR 法去除离群值
def remove_outliers_iqr(df, col, k=1.5, group_col=None):
    """IQR法去除离群值"""
    if group_col:
        def _remove(group):
            q1, q3 = group[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            return group[group[col].between(q1 - k*iqr, q3 + k*iqr)]
        return df.groupby(group_col, group_keys=False).apply(_remove).reset_index(drop=True)
    else:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        return df[df[col].between(q1 - k*iqr, q3 + k*iqr)]

# ============================================================
# 自动 QC 过滤
# ============================================================
def auto_qc_filter(df, count_col='nCount_RNA', feature_col='nFeature_RNA',
                    mt_col='percent_mt', mt_cutoff=20, k=3):
    """自动 QC 过滤（MAD法）"""
    original = len(df)
    
    # 去除极端值
    for col in [count_col, feature_col]:
        df = remove_outliers_mad(df, col, k=k)
    
    # 线粒体阈值
    if mt_col in df.columns:
        df = df[df[mt_col] < mt_cutoff]
    
    print(f"QC过滤: {original} → {len(df)} (去除 {original - len(df)} 个细胞)")
    return df

# ============================================================
# 去除低表达基因
# ============================================================
def filter_low_expression(df, min_cells=3, min_count=10):
    """过滤低表达基因
    df: 行=基因, 列=样本 的表达矩阵
    """
    mask = (df >= min_count).sum(axis=1) >= min_cells
    filtered = df[mask]
    print(f"低表达过滤: {len(df)} → {len(filtered)} 基因")
    return filtered
```

---

## 📊 分组聚合

```python
# ============================================================
# groupby 核心操作
# ============================================================

# 单列分组 + 单一聚合
df.groupby('cluster')['log2FC'].mean()
df.groupby('cluster')['log2FC'].median()
df.groupby('cluster')['gene'].count()
df.groupby('cluster')['log2FC'].std()

# 单列分组 + 多种聚合
df.groupby('cluster')['log2FC'].agg(['mean', 'median', 'std', 'count'])

# 多列分组
df.groupby(['cluster', 'direction'])['log2FC'].mean()

# 多列 + 多种聚合
df.groupby('cluster').agg({
    'log2FC': ['mean', 'median', 'std'],
    'pvalue': ['min', 'median'],
    'gene': 'count'
})

# 命名聚合（推荐！）
df.groupby('cluster').agg(
    mean_fc=('log2FC', 'mean'),
    median_fc=('log2FC', 'median'),
    n_genes=('gene', 'count'),
    n_up=('log2FC', lambda x: (x > 0).sum())
)

# ============================================================
# 高级聚合
# ============================================================

# 自定义聚合函数
df.groupby('cluster')['log2FC'].agg(
    mad=lambda x: (x - x.median()).abs().median() * 1.4826,
    cv=lambda x: x.std() / x.mean() if x.mean() != 0 else 0,
    pct_positive=lambda x: (x > 0).mean() * 100
)

# transform —— 保持原始形状（最常用！）
# 每个值减去组内均值（组内中心化）
df['log2FC_centered'] = df.groupby('cluster')['log2FC'].transform(lambda x: x - x.mean())

# 组内Z-score
df['z_score'] = df.groupby('cluster')['log2FC'].transform(lambda x: (x - x.mean()) / x.std())

# 组内排名
df['rank'] = df.groupby('cluster')['log2FC'].rank(ascending=False)

# 组内累积和
df['cumsum'] = df.groupby('cluster')['log2FC'].cumsum()

# ============================================================
# apply —— 分组后应用任意函数
# ============================================================

# 每组取 top 5
df.groupby('cluster').apply(lambda x: x.nlargest(5, 'log2FC'), include_groups=False)

# 每组做 t 检验
from scipy import stats
def group_ttest(group):
    treat = group[group['condition'] == 'Treat']['value']
    ctrl = group[group['condition'] == 'Control']['value']
    if len(treat) < 2 or len(ctrl) < 2:
        return pd.Series({'t_stat': np.nan, 'p_value': np.nan})
    t, p = stats.ttest_ind(treat, ctrl)
    return pd.Series({'t_stat': t, 'p_value': p})

results = df.groupby('gene').apply(group_ttest).reset_index()

# ============================================================
# 交叉表
# ============================================================
pd.crosstab(df['cluster'], df['direction'])                    # 频数表
pd.crosstab(df['cluster'], df['direction'], normalize='index') # 行百分比
pd.crosstab(df['cluster'], df['direction'], normalize='columns') # 列百分比
pd.crosstab(df['cluster'], df['direction'], values=df['log2FC'], aggfunc='mean')  # 透视

# ============================================================
# 透视表
# ============================================================
pd.pivot_table(df, values='log2FC', index='cluster', columns='direction', aggfunc='mean')
pd.pivot_table(df, values='log2FC', index='cluster', aggfunc=['mean', 'std'])
```

---

## 🔗 合并连接与重塑

```python
# ============================================================
# merge —— 表连接
# ============================================================

# 四种连接
pd.merge(df1, df2, on='gene')                             # 内连接（交集）
pd.merge(df1, df2, on='gene', how='left')                 # 左连接
pd.merge(df1, df2, on='gene', how='right')                # 右连接
pd.merge(df1, df2, on='gene', how='outer')                # 全连接

# 列名不同时
pd.merge(df1, df2, left_on='gene_symbol', right_on='symbol')

# 多列连接
pd.merge(df1, df2, on=['gene', 'cluster'])

# 去除重复列
pd.merge(df1, df2, on='gene', suffixes=('_ctrl', '_treat'))

# ============================================================
# concat —— 纵向/横向合并
# ============================================================
pd.concat([df1, df2], axis=0)              # 纵向（行合并）
pd.concat([df1, df2], axis=1)              # 横向（列合并）
pd.concat([df1, df2], keys=['ctrl', 'treat'])  # 带标签

# ============================================================
# 批量合并
# ============================================================
def batch_merge(df_list, on='gene', how='left'):
    """批量左连接"""
    from functools import reduce
    return reduce(lambda left, right: pd.merge(left, right, on=on, how=how), df_list)

# ============================================================
# melt —— 宽变长
# ============================================================
# 原始: gene | sample1 | sample2 | sample3
# 目标: gene | sample | expression
df_long = df_wide.melt(id_vars='gene', var_name='sample', value_name='expression')

# ============================================================
# pivot —— 长变宽
# ============================================================
df_wide = df_long.pivot(index='gene', columns='sample', values='expression')

# ============================================================
# pivot_table —— 长变宽+聚合
# ============================================================
pd.pivot_table(df_long, values='expression', index='gene', columns='cluster', aggfunc='mean')

# ============================================================
# stack / unstack —— 层次索引操作
# ============================================================
df.stack()         # 列→行（宽→长）
df.unstack()       # 行→列（长→宽）
```

---

## ✂️ 字符串与文本处理

```python
# ============================================================
# .str 访问器 —— 向量化字符串操作
# ============================================================

# 检测
df['gene'].str.contains('TP')               # 是否包含
df['gene'].str.startswith('RP')             # 前缀
df['gene'].str.endswith('1')                # 后缀
df['gene'].str.match(r'^MT-')               # 正则匹配
df['gene'].str.isnumeric()                  # 是否数字

# 提取
df['gene'].str.extract(r'(ENSG\d+)')               # 提取第一个匹配
df['gene'].str.extractall(r'(\d+)')                  # 提取所有匹配
df['gene'].str.split('_', expand=True)               # 分割为多列
df['gene'].str.split('_').str[0]                     # 分割取第一个

# 替换
df['gene'].str.replace('MT-', 'mito_')              # 替换
df['gene'].str.replace(r'\.\d+$', '', regex=True)   # 正则替换（去版本号）
df['gene'].str.strip()                                # 去首尾空白
df['gene'].str.lower()                                # 小写
df['gene'].str.upper()                                # 大写

# 长度
df['gene'].str.len()

# ============================================================
# 生信常用字符串处理
# ============================================================

# 基因ID处理
df['gene_short'] = df['gene_id'].str.replace(r'\.\d+$', '', regex=True)  # 去版本号
df['chr'] = df['chrom'].str.removeprefix('chr')                          # 去chr前缀
df['gene_type'] = df['gene_id'].str.extract(r'^(ENSG|ENST)')            # 提取ID类型

# 批量列名清洗
df.columns = (df.columns
    .str.replace(' ', '_')
    .str.replace('.', '_')
    .str.replace('-', '_')
    .str.lower()
)
```

---

## 🧬 生信实战封装

### 1. 表达矩阵处理

```python
# ============================================================
# 表达矩阵标准化
# ============================================================
def normalize_expression(mat, method='cpm'):
    """表达矩阵标准化
    mat: 行=基因, 列=样本 的 DataFrame
    """
    if method == 'cpm':
        lib_sizes = mat.sum(axis=0)
        return mat.div(lib_sizes, axis=1) * 1e6
    
    elif method == 'log2cpm':
        lib_sizes = mat.sum(axis=0)
        cpm = mat.div(lib_sizes, axis=1) * 1e6
        return np.log2(cpm + 1)
    
    elif method == 'tpm':
        # 需要 gene_length 列
        if 'gene_length' not in mat.columns:
            raise ValueError("TPM需要基因长度信息")
        lengths = mat['gene_length']
        counts = mat.drop('gene_length', axis=1)
        rpk = counts.div(lengths, axis=0)
        rpk_sum = rpk.sum(axis=0)
        return rpk.div(rpk_sum, axis=1) * 1e6
    
    elif method == 'zscore':
        return mat.apply(lambda x: (x - x.mean()) / x.std(), axis=1)
    
    elif method == 'quantile':
        from scipy import stats
        ranked = mat.rank(method='min').stack()
        quantiles = ranked.groupby(ranked).apply(lambda x: x.mean())
        return mat.rank(method='min').stack().map(quantiles).unstack()
    
    else:
        raise ValueError(f"不支持的方法: {method}")

# ============================================================
# 差异基因筛选
# ============================================================
def filter_degs(df, fc_col='log2FoldChange', padj_col='padj',
                fc_cutoff=1.0, padj_cutoff=0.05):
    """筛选差异基因"""
    result = df.copy()
    result['direction'] = 'NS'
    result.loc[(result[fc_col] > fc_cutoff) & (result[padj_col] < padj_cutoff), 'direction'] = 'Up'
    result.loc[(result[fc_col] < -fc_cutoff) & (result[padj_col] < padj_cutoff), 'direction'] = 'Down'
    
    up = (result['direction'] == 'Up').sum()
    down = (result['direction'] == 'Down').sum()
    print(f"差异基因: 上调 {up}, 下调 {down}, 总计 {up+down}")
    return result

# ============================================================
# 基因ID转换
# ============================================================
def convert_gene_ids(genes, from_type='symbol', to_type='entrez', species='human'):
    """使用 mygene 包转换基因ID"""
    import mygene
    mg = mygene.MyGeneInfo()
    
    scopes_map = {
        'symbol': 'symbol',
        'entrez': 'entrezgene',
        'ensembl': 'ensembl.gene',
        'refseq': 'refseq'
    }
    fields_map = {
        'symbol': 'symbol',
        'entrez': 'entrezgene',
        'ensembl': 'ensembl.gene',
        'refseq': 'refseq'
    }
    
    result = mg.querymany(genes,
                          scopes=scopes_map.get(from_type, from_type),
                          fields=fields_map.get(to_type, to_type),
                          species=species,
                          as_dataframe=True)
    return result

# ============================================================
# Venn图数据准备
# ============================================================
def prepare_venn(dfs_dict, gene_col='gene'):
    """准备 Venn 图数据（多组基因列表）"""
    sets = {name: set(df[gene_col]) for name, df in dfs_dict.items()}
    
    from itertools import combinations
    overlaps = {}
    for i in range(1, len(sets) + 1):
        for combo in combinations(sets.keys(), i):
            if i == 1:
                overlaps[combo[0]] = len(sets[combo[0]])
            else:
                overlap = set.intersection(*[sets[c] for c in combo])
                overlaps[' ∩ '.join(combo)] = len(overlap)
    
    return sets, overlaps

# ============================================================
# 批量统计检验
# ============================================================
def batch_ttest(df, value_col, group_col, group1, group2, gene_col='gene'):
    """批量 t 检验"""
    from scipy import stats
    
    results = []
    for gene, group in df.groupby(gene_col):
        g1 = group[group[group_col] == group1][value_col]
        g2 = group[group[group_col] == group2][value_col]
        
        if len(g1) >= 2 and len(g2) >= 2:
            t_stat, p_value = stats.ttest_ind(g1, g2)
            results.append({
                gene_col: gene,
                f'mean_{group1}': g1.mean(),
                f'mean_{group2}': g2.mean(),
                'log2FC': np.log2(g1.mean() / g2.mean()) if g2.mean() > 0 else np.nan,
                't_stat': t_stat,
                'p_value': p_value
            })
    
    result_df = pd.DataFrame(results)
    
    # BH校正
    from statsmodels.stats.multitest import multipletests
    if len(result_df) > 0:
        _, result_df['padj'], _, _ = multipletests(result_df['p_value'], method='fdr_bh')
    
    return result_df

# ============================================================
# 富集分析（Python版）
# ============================================================
def run_gsea_py(gene_list, gene_sets='MSigDB_H.all.v2023.1.Hs.symbol.gmt',
                outdir='gsea_results', species='human'):
    """使用 gseapy 运行 GSEA"""
    import gseapy as gp
    
    # 需要排序列表 (gene: score)
    pre_res = gp.prerank(
        rnk=gene_list,
        gene_sets=gene_sets,
        outdir=outdir,
        permutation_num=1000,
        no_plot=False,
        seed=42,
        min_size=10,
        max_size=500
    )
    
    return pre_res.res2d

def run_ora_py(gene_list, gene_sets='MSigDB_H.all.v2023.1.Hs.symbol.gmt',
               outdir='ora_results', species='human'):
    """使用 gseapy 运行 ORA"""
    import gseapy as gp
    
    enr = gp.enrichr(
        gene_list=gene_list,
        gene_sets=gene_sets,
        outdir=outdir,
        no_plot=False
    )
    
    return enr.results
```

---

## 🚀 一键数据处理流水线

```python
# ============================================================
# run_rnaseq_pipeline_py —— Python版 RNA-seq 数据处理
# ============================================================
def run_rnaseq_pipeline(count_file, sample_file,
                         group_col='condition', ref_group='Control',
                         fc_cutoff=1.0, padj_cutoff=0.05,
                         save_dir='rnaseq_results'):
    """Python版 RNA-seq 处理流水线"""
    import os
    from scipy import stats
    from statsmodels.stats.multitest import multipletests
    
    os.makedirs(save_dir, exist_ok=True)
    print("🚀 RNA-seq Python 流水线启动")
    
    # 1. 读取数据
    print("📂 读取数据...")
    counts = smart_read(count_file, index_col=0)
    samples = smart_read(sample_file)
    
    print(f"  基因数: {counts.shape[0]}, 样本数: {counts.shape[1]}")
    
    # 2. 预过滤
    print("🔧 预过滤...")
    min_samples = max(1, counts.shape[1] * 0.1)
    keep = (counts >= 10).sum(axis=1) >= min_samples
    counts = counts[keep]
    print(f"  保留基因: {len(counts)}")
    
    # 3. CPM标准化
    print("📐 CPM标准化...")
    cpm = normalize_expression(counts, method='log2cpm')
    
    # 4. 差异分析（简化版Wald检验）
    print("🧬 差异分析...")
    groups = samples.set_index(samples.columns[0])[group_col]
    
    all_groups = groups.unique()
    if ref_group not in all_groups:
        ref_group = all_groups[0]
    
    treat_group = [g for g in all_groups if g != ref_group][0]
    
    ctrl_samples = groups[groups == ref_group].index
    treat_samples = groups[groups == treat_group].index
    
    deg_results = []
    for gene in counts.index:
        ctrl_vals = counts.loc[gene, ctrl_samples].values.astype(float)
        treat_vals = counts.loc[gene, treat_samples].values.astype(float)
        
        try:
            t_stat, p_value = stats.ttest_ind(treat_vals, ctrl_vals)
            mean_ctrl = ctrl_vals.mean()
            mean_treat = treat_vals.mean()
            log2fc = np.log2((mean_treat + 1) / (mean_ctrl + 1))
        except:
            t_stat, p_value, log2fc = np.nan, np.nan, np.nan
        
        deg_results.append({
            'gene': gene,
            'baseMean': (mean_ctrl + mean_treat) / 2,
            'log2FoldChange': log2fc,
            't_stat': t_stat,
            'pvalue': p_value
        })
    
    deg_df = pd.DataFrame(deg_results)
    
    # BH校正
    valid_mask = deg_df['pvalue'].notna()
    deg_df.loc[valid_mask, 'padj'] = multipletests(
        deg_df.loc[valid_mask, 'pvalue'], method='fdr_bh'
    )[1]
    
    # 5. 筛选差异基因
    deg_df = filter_degs(deg_df, fc_cutoff=fc_cutoff, padj_cutoff=padj_cutoff)
    
    # 6. 保存
    smart_write(deg_df, os.path.join(save_dir, 'DEG_results.csv'))
    
    up_genes = deg_df[deg_df['direction'] == 'Up']['gene'].tolist()
    down_genes = deg_df[deg_df['direction'] == 'Down']['gene'].tolist()
    
    print(f"\n✅ 分析完成！上调: {len(up_genes)}, 下调: {len(down_genes)}")
    print(f"结果保存在: {save_dir}")
    
    return {
        'results': deg_df,
        'up_genes': up_genes,
        'down_genes': down_genes,
        'cpm': cpm
    }

# 使用示例：
# result = run_rnaseq_pipeline("counts.csv", "samples.csv", group_col="condition")
```

---

## ⚡ 性能优化

```python
# ============================================================
# pandas 性能优化技巧
# ============================================================

# 1. 类型优化（省内存）
def optimize_dtypes(df):
    """自动优化 DataFrame 数据类型，减少内存"""
    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type == 'object':
            # 字符串 → category（唯一值 < 50% 时）
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
        
        elif col_type in ['int64', 'int32']:
            c_min, c_max = df[col].min(), df[col].max()
            if c_min >= 0:
                if c_max < 255: df[col] = df[col].astype('uint8')
                elif c_max < 65535: df[col] = df[col].astype('uint16')
                elif c_max < 4294967295: df[col] = df[col].astype('uint32')
            else:
                if c_min > -128 and c_max < 127: df[col] = df[col].astype('int8')
                elif c_min > -32768 and c_max < 32767: df[col] = df[col].astype('int16')
                elif c_min > -2147483648 and c_max < 2147483647: df[col] = df[col].astype('int32')
        
        elif col_type in ['float64', 'float32']:
            df[col] = df[col].astype('float32')
    
    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    print(f"内存: {start_mem:.1f} MB → {end_mem:.1f} MB ({100*(start_mem-end_mem)/start_mem:.1f}% 减少)")
    return df

# 2. 向量化操作（避免 for 循环）
# ❌ 慢
# for i in range(len(df)):
#     df.loc[i, 'new'] = df.loc[i, 'a'] * df.loc[i, 'b']
# ✅ 快
df['new'] = df['a'] * df['b']

# 3. 使用 .values 获取 NumPy 数组（加速计算）
values = df['column'].values  # 比 df['column'] 快

# 4. 大文件读取
# 只读需要的列
df = pd.read_csv("huge_file.csv", usecols=['gene', 'log2FC', 'pvalue'])

# 分块读取
chunks = pd.read_csv("huge_file.csv", chunksize=10000)
result = pd.concat([process(chunk) for chunk in chunks])

# 指定类型
df = pd.read_csv("file.csv", dtype={'gene': 'category', 'count': 'int32'})

# 5. 使用 Parquet 格式（比CSV快10x+）
df.to_parquet("data.parquet")     # 保存
df = pd.read_parquet("data.parquet")  # 读取

# 6. query() 比 布尔索引快（大数据集）
df.query("pvalue < 0.05 and log2FC > 1")  # 比	df[(df['pvalue'] < 0.05) & (df['log2FC'] > 1)]  快

# 7. eval() 加速复杂运算
df.eval("z = (x + y) / 2", inplace=True)

# 8. 多进程分组
from concurrent.futures import ProcessPoolExecutor

def parallel_groupby(df, group_col, func, n_workers=4):
    """并行分组操作"""
    groups = [g for _, g in df.groupby(group_col)]
    
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(func, groups))
    
    return pd.concat(results, ignore_index=True)
```

---

## 📋 函数速查表

### 封装函数速查

| 函数 | 用途 | 调用示例 |
|------|------|----------|
| `smart_read()` | 智能读取 | `smart_read("data.csv")` |
| `smart_write()` | 智能导出 | `smart_write(df, "out.xlsx")` |
| `batch_read()` | 批量读取 | `batch_read("./data/")` |
| `quick_overview()` | 快速概览 | `quick_overview(df)` |
| `remove_outliers_mad()` | MAD去离群 | `remove_outliers_mad(df, "value")` |
| `remove_outliers_iqr()` | IQR去离群 | `remove_outliers_iqr(df, "value")` |
| `auto_qc_filter()` | 自动QC | `auto_qc_filter(df)` |
| `filter_low_expression()` | 过滤低表达 | `filter_low_expression(mat)` |
| `filter_degs()` | 差异基因筛选 | `filter_degs(df, fc_cutoff=1)` |
| `convert_gene_ids()` | 基因ID转换 | `convert_gene_ids(genes)` |
| `normalize_expression()` | 表达标准化 | `normalize_expression(mat, "cpm")` |
| `prepare_venn()` | Venn图数据 | `prepare_venn({"up":df1,"down":df2})` |
| `batch_ttest()` | 批量t检验 | `batch_ttest(df, "expr", "cond", "A", "B")` |
| `run_gsea_py()` | Python GSEA | `run_gsea_py(ranked_list)` |
| `run_rnaseq_pipeline()` | RNA-seq流水线 | `run_rnaseq_pipeline("c.csv","s.csv")` |
| `optimize_dtypes()` | 内存优化 | `optimize_dtypes(df)` |
| `group_top_n()` | 分组取TopN | `group_top_n(df, "cluster", "log2FC", 5)` |

### pandas 核心方法速查

```
# 读取/导出
read_csv() read_excel() read_parquet() read_hdf() read_json()
to_csv() to_excel() to_parquet() to_hdf() to_json()

# 查看
head() tail() info() describe() shape columns index dtypes nunique()

# 选择
[] loc[] iloc[] at[] iat[] filter() select_dtypes()

# 筛选
query() isin() between() mask() where()

# 清洗
dropna() fillna() drop_duplicates() replace() astype() strip()

# 变换
assign() apply() map() applymap() transform() pipe()

# 聚合
groupby() agg() sum() mean() median() count() value_counts()

# 合并
merge() join() concat() combine_first()

# 重塑
melt() pivot() pivot_table() stack() unstack() explode()

# 排序
sort_values() sort_index() nlargest() nsmallest() rank()

# 字符串
str.contains() str.replace() str.extract() str.split() str.startswith()

# 时间
to_datetime() dt.year dt.month dt.day dt.strftime() resample()

# 统计
corr() cov() cumsum() cummax() diff() pct_change()
```

### Python vs R 对比速查

```
# R (dplyr)                    → Python (pandas)
filter(df, condition)          → df[df['col'] > value]
select(df, col1, col2)         → df[['col1', 'col2']]
mutate(df, new = old*2)        → df.assign(new=df['old']*2)
summarise(df, m=mean(x))       → df.agg({'x': 'mean'})
group_by(df, col) %>%          → df.groupby('col').agg(...)
arrange(df, desc(col))         → df.sort_values('col', ascending=False)
left_join(df1, df2, by="x")    → pd.merge(df1, df2, on='x', how='left')
pivot_longer()                 → df.melt()
pivot_wider()                  → df.pivot()
count(df, col)                 → df['col'].value_counts()
distinct(df, col)              → df['col'].unique()
rename(df, new=old)            → df.rename(columns={'old': 'new'})
slice_head(n=5)                → df.head(5)
```

---

> 📌 **核心原则**：向量化操作替代 for 循环，`groupby().agg()` 替代逐行计算，`merge()` 替代手动匹配。
> 一行运行：`run_rnaseq_pipeline("counts.csv", "samples.csv")` 完成 Python 版 RNA-seq 全流程。
