#!/usr/bin/env python3
"""
脚本2：CSV缺列自动识别+NCBI填补
功能：自动识别CSV表格中缺了哪一列，然后从NCBI抓取数据填补。

用法：
  python fill_csv_from_ncbi.py -c mapping.csv -o mapping_filled.csv
  python fill_csv_from_ncbi.py -c mapping.csv --email your@email.com

参数：
  -c, --csv       CSV表格路径（可能缺一列的表格）
  -o, --output    输出文件路径（默认在原文件名后加_filled）
  --email         NCBI Entrez要求的邮箱（首次使用必须提供）
  --gene          目标基因名（用于缺序列号时的搜索，如 COI, Cytb, 16S, 18S, ITS）
  --gene-length   目标基因的标准长度（用于选择最接近长度的序列）
  --encoding      文件编码（默认utf-8）

NCBI标准基因长度参考：
  COI (线粒体): ~1550 bp (动物), ~1500 bp (植物 matK 附近)
  Cytb (线粒体): ~1140 bp
  16S rRNA (线粒体): ~600 bp
  18S rRNA (核糖体): ~1800 bp
  28S rRNA (核糖体): ~800-900 bp (D2-D3区)
  ITS (核糖体): ~600-700 bp
"""

import argparse
import csv
import re
import os
import sys
import time

# NCBI Entrez 需要 BioPython
try:
    from Bio import Entrez
    from Bio import SeqIO
    from Bio.Seq import Seq
    HAS_BIOPYTHON = True
except ImportError:
    HAS_BIOPYTHON = False


# 常用基因的标准长度参考
GENE_LENGTH_REF = {
    'COI': 1550, 'CO1': 1550, 'cox1': 1550,
    'Cytb': 1140, 'cytb': 1140, 'COB': 1140,
    '16S': 600, '16s': 600,
    '18S': 1800, '18s': 1800,
    '28S': 850, '28s': 850,
    'ITS': 650, 'ITS1': 250, 'ITS2': 300,
    '12S': 950, '12s': 950,
    'ND1': 950, 'ND2': 1040, 'ND4': 1380, 'ND5': 1820,
}


def detect_csv_structure(csv_path, encoding='utf-8'):
    """
    自动检测CSV的结构：
    - 两列都有 → 不需要填补
    - 只有第1列（序列号）→ 缺物种名
    - 只有第2列（物种名）→ 缺序列号
    - 无法判断 → 报错
    
    判断逻辑：
    - 序列号列：包含标准NCBI格式（字母+数字+.+版本号）
    - 物种名列：包含拉丁学名格式（属名+种加词，可能含空格）
    """
    with open(csv_path, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        return None, [], "CSV文件为空"
    
    # 检测列数
    num_cols = max(len(row) for row in rows)
    
    if num_cols == 2:
        # 检查两列是否都有内容
        col1_filled = sum(1 for row in rows[1:] if len(row) > 0 and row[0].strip())
        col2_filled = sum(1 for row in rows[1:] if len(row) > 1 and row[1].strip())
        total = len(rows) - 1  # 减去表头
        
        if col1_filled > total * 0.5 and col2_filled > total * 0.5:
            return 'both', rows, "两列都有数据，不需要填补"
        elif col1_filled > total * 0.5:
            return 'missing_col2', rows, f"第2列缺失（{col2_filled}/{total}有数据），需要从NCBI获取物种名"
        elif col2_filled > total * 0.5:
            return 'missing_col1', rows, f"第1列缺失（{col1_filled}/{total}有数据），需要从NCBI获取序列号"
        else:
            return 'unknown', rows, "无法判断列内容"
    
    elif num_cols == 1:
        # 只有一列，判断是序列号还是物种名
        col1_data = [row[0].strip() for row in rows[1:] if row[0].strip()]
        
        # 检测是否像序列号
        acc_pattern = re.compile(r'^[A-Za-z]{1,4}\d{5,8}(?:\.\d+)?$')
        acc_count = sum(1 for d in col1_data if acc_pattern.match(d))
        
        # 检测是否像物种名（至少两个词，首字母大写）
        species_pattern = re.compile(r'^[A-Z][a-z]+\s+[a-z]+')
        species_count = sum(1 for d in col1_data if species_pattern.match(d))
        
        if acc_count > len(col1_data) * 0.5:
            return 'missing_col2', rows, "只有序列号列，需要获取物种名"
        elif species_count > len(col1_data) * 0.5:
            return 'missing_col1', rows, "只有物种名列，需要获取序列号"
        else:
            # 尝试另一种判断：如果内容包含空格→更可能是物种名
            has_space = sum(1 for d in col1_data if ' ' in d)
            if has_space > len(col1_data) * 0.3:
                return 'missing_col1', rows, "推断为物种名列，需要获取序列号"
            else:
                return 'missing_col2', rows, "推断为序列号列，需要获取物种名"
    
    else:
        return None, rows, f"CSV有{num_cols}列，期望1-2列"


def fetch_species_from_accession(accession, email):
    """从NCBI通过序列号获取物种名"""
    if not HAS_BIOPYTHON:
        print("错误：需要安装BioPython (pip install biopython)")
        return None
    
    Entrez.email = email
    
    try:
        # 先获取GI号
        handle = Entrez.esearch(db="nucleotide", term=accession, retmax=1)
        record = Entrez.read(handle)
        handle.close()
        
        if not record['IdList']:
            # 尝试去掉版本号
            acc_base = accession.split('.')[0]
            handle = Entrez.esearch(db="nucleotide", term=acc_base, retmax=1)
            record = Entrez.read(handle)
            handle.close()
        
        if not record['IdList']:
            return None
        
        gi = record['IdList'][0]
        
        # 获取物种信息
        handle = Entrez.efetch(db="nucleotide", id=gi, rettype="gb", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        
        if records:
            organism = str(records[0].get('GBSeq_organism', ''))
            return organism
        
    except Exception as e:
        print(f"  警告：获取 {accession} 的物种名失败: {e}")
    
    return None


def fetch_accession_from_species(species, email, gene_name=None, target_length=None):
    """
    从NCBI通过物种名获取序列号。
    优先选择参考序列(RefSeq)，其次选择最接近目标长度的序列。
    """
    if not HAS_BIOPYTHON:
        print("错误：需要安装BioPython (pip install biopython)")
        return None
    
    Entrez.email = email
    
    # 构建搜索词
    search_term = f'{species}[Organism]'
    if gene_name:
        search_term += f' AND {gene_name}[Gene]'
    
    try:
        # 搜索
        handle = Entrez.esearch(db="nucleotide", term=search_term, retmax=20)
        record = Entrez.read(handle)
        handle.close()
        
        if not record['IdList']:
            # 放宽搜索条件，只用物种名
            handle = Entrez.esearch(db="nucleotide", term=f'{species}[Organism]', retmax=20)
            record = Entrez.read(handle)
            handle.close()
        
        if not record['IdList']:
            return None
        
        gi_list = record['IdList']
        
        # 获取序列详情
        handle = Entrez.efetch(db="nucleotide", id=','.join(gi_list[:10]), rettype="gb", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        
        best_acc = None
        best_score = -1
        
        for rec in records:
            accession = rec.get('GBSeq_primary-accession', '')
            length = int(rec.get('GBSeq_length', 0))
            is_refseq = accession.startswith(('NM_', 'NC_', 'XR_', 'XM_', 'AP_', 'NP_'))
            
            # 评分：RefSeq加分，长度接近目标加分
            score = 0
            if is_refseq:
                score += 1000  # RefSeq优先
            
            if target_length and length > 0:
                length_diff = abs(length - target_length)
                score += max(0, 500 - length_diff)  # 越接近标准长度分越高
            
            if score > best_score:
                best_score = score
                best_acc = accession
        
        return best_acc
        
    except Exception as e:
        print(f"  警告：获取 {species} 的序列号失败: {e}")
        return None


def fill_missing_col1(rows, email, gene_name=None, target_length=None):
    """填补缺失的第1列（序列号）"""
    print(f"\n正在从NCBI获取序列号（共{len(rows)-1}条）...")
    
    filled = 0
    for i, row in enumerate(rows):
        if i == 0:
            # 表头
            if len(row) < 2:
                row.append('Accession')
            continue
        
        if len(row) >= 2 and row[0].strip() == '' and row[1].strip():
            species = row[1].strip()
            print(f"  [{i}/{len(rows)-1}] 搜索: {species}", end='')
            
            acc = fetch_accession_from_species(species, email, gene_name, target_length)
            if acc:
                row[0] = acc
                filled += 1
                print(f" → {acc}")
            else:
                print(f" → 未找到")
            
            time.sleep(0.5)  # 避免NCBI限速
    
    print(f"\n已完成，成功填补 {filled}/{len(rows)-1} 条")
    return rows


def fill_missing_col2(rows, email):
    """填补缺失的第2列（物种名）"""
    print(f"\n正在从NCBI获取物种名（共{len(rows)-1}条）...")
    
    filled = 0
    for i, row in enumerate(rows):
        if i == 0:
            # 表头
            if len(row) < 2:
                row.append('Species')
            continue
        
        if len(row) >= 1 and row[0].strip():
            accession = row[0].strip()
            
            # 确保第二列存在
            while len(row) < 2:
                row.append('')
            
            if row[1].strip() == '':
                print(f"  [{i}/{len(rows)-1}] 查询: {accession}", end='')
                
                species = fetch_species_from_accession(accession, email)
                if species:
                    row[1] = species
                    filled += 1
                    print(f" → {species}")
                else:
                    print(f" → 未找到")
                
                time.sleep(0.5)  # 避免NCBI限速
    
    print(f"\n已完成，成功填补 {filled}/{len(rows)-1} 条")
    return rows


def save_csv(rows, output_path, encoding='utf-8'):
    """保存CSV文件"""
    with open(output_path, 'w', encoding=encoding, newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
    print(f"已保存到: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='CSV缺列自动识别+NCBI填补工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  # 自动检测并填补
  python fill_csv_from_ncbi.py -c mapping.csv --email your@email.com
  
  # 指定目标基因（用于缺序列号时）
  python fill_csv_from_ncbi.py -c mapping.csv --email your@email.com --gene COI --gene-length 1550
  
  # 指定输出路径
  python fill_csv_from_ncbi.py -c mapping.csv --email your@email.com -o filled.csv

常用基因长度参考：
  COI: 1550bp  Cytb: 1140bp  16S: 600bp  18S: 1800bp  28S: 850bp  ITS: 650bp
        '''
    )
    parser.add_argument('-c', '--csv', required=True, help='CSV表格路径')
    parser.add_argument('-o', '--output', default=None, help='输出文件路径')
    parser.add_argument('--email', required=True, help='NCBI Entrez邮箱')
    parser.add_argument('--gene', default=None, help='目标基因名（如COI, Cytb, 16S）')
    parser.add_argument('--gene-length', type=int, default=None,
                        help='目标基因标准长度（bp），不指定则自动查参考表')
    parser.add_argument('--encoding', default='utf-8', help='文件编码')
    
    args = parser.parse_args()
    
    if not HAS_BIOPYTHON:
        print("错误：需要安装BioPython")
        print("运行: pip install biopython")
        sys.exit(1)
    
    if not os.path.exists(args.csv):
        print(f"错误：CSV文件不存在: {args.csv}")
        sys.exit(1)
    
    # 确定基因标准长度
    target_length = args.gene_length
    if target_length is None and args.gene:
        target_length = GENE_LENGTH_REF.get(args.gene)
        if target_length:
            print(f"已自动匹配 {args.gene} 标准长度: {target_length} bp")
    
    # 检测CSV结构
    status, rows, message = detect_csv_structure(args.csv, args.encoding)
    print(f"检测结果: {message}")
    
    if status == 'both':
        print("两列都有数据，无需填补。如需强制填补空缺行，请使用 --force 参数")
        sys.exit(0)
    
    if status == 'missing_col1':
        rows = fill_missing_col1(rows, args.email, args.gene, target_length)
    elif status == 'missing_col2':
        rows = fill_missing_col2(rows, args.email)
    else:
        print(f"错误：{message}")
        sys.exit(1)
    
    # 保存
    if args.output is None:
        base, ext = os.path.splitext(args.csv)
        args.output = f"{base}_filled{ext}"
    
    save_csv(rows, args.output, args.encoding)


if __name__ == '__main__':
    main()
