#!/usr/bin/env python3
"""
脚本3：FASTA头解析+序列号提取+可选重命名
功能：解析从NCBI下载的FASTA文件，提取序列号和物种名，生成CSV，
     可选择将序列名替换为物种名或整齐的序列号。

NCBI FASTA头格式示例：
  >AB123456.1 Species name mitochondrial gene for COI, complete cds
  >PP987654.1 Organism name 16S ribosomal RNA gene, partial sequence
  >MW_123456.1 Species name isolate xxx gene for Cytb, complete cds

用法：
  # 仅解析生成CSV
  python parse_fasta_headers.py -f sequences.fasta -o mapping.csv
  
  # 解析+重命名为物种名
  python parse_fasta_headers.py -f sequences.fasta --rename-species -o renamed.fasta
  
  # 解析+重命名为整齐序列号
  python parse_fasta_headers.py -f sequences.fasta --rename-accession -o clean.fasta

参数：
  -f, --fasta           FASTA文件路径
  -o, --output          输出文件路径（默认根据操作类型自动命名）
  --csv                 单独指定CSV输出路径
  --rename-species      将序列名替换为物种名
  --rename-accession    将序列名替换为整齐的序列号（默认行为，如果启用重命名）
  --encoding            文件编码（默认utf-8）
"""

import argparse
import csv
import re
import os
import sys


def parse_ncbi_header(header_line):
    """
    解析NCBI FASTA头行，提取序列号和物种名。
    
    NCBI头格式：
    >accession.version Organism_name gene description...
    
    返回: (accession, species, full_header)
    """
    # 去掉 > 号
    header = header_line.lstrip('>').strip()
    
    if not header:
        return None, None, header
    
    # 提取序列号（第一个空格前的部分）
    # NCBI序列号格式：AB123456.1, PP987654.1, NM_123456.1, NC_012345.1
    parts = header.split(None, 1)  # 最多分2部分
    accession = parts[0].strip()
    rest = parts[1].strip() if len(parts) > 1 else ''
    
    # 清理序列号（确保是标准格式）
    acc_pattern = re.compile(r'^([A-Za-z]{1,4}_?\d{5,8}(?:\.\d+)?)')
    acc_match = acc_pattern.match(accession)
    if acc_match:
        clean_accession = acc_match.group(1)
    else:
        clean_accession = accession
    
    # 从rest中提取物种名
    # 物种名通常是前两个词（属名+种加词），可能包含var., subsp.等
    species = None
    
    # 策略1：标准拉丁学名格式（Genus species）
    # 物种名在序列号之后，基因描述之前
    # 常见模式：Species_name  gene_name 或 Species_name  mitochondrial ...
    species_pattern = re.compile(
        r'^([A-Z][a-z]+\s+[a-z]+(?:\s+(?:var\.|subsp\.)\s+[a-z]+)?)'
    )
    sp_match = species_pattern.match(rest)
    if sp_match:
        species = sp_match.group(1).strip()
    else:
        # 策略2：下划线分隔的物种名（NCBI有时用下划线代替空格）
        species_pattern2 = re.compile(
            r'^([A-Z][a-z]+_[a-z]+(?:_(?:var|subsp)_[a-z]+)?)'
        )
        sp_match2 = species_pattern2.match(rest)
        if sp_match2:
            species = sp_match2.group(1).replace('_', ' ').strip()
        else:
            # 策略3：尝试取前两个词
            words = rest.split()
            if len(words) >= 2:
                candidate = f"{words[0]} {words[1]}"
                # 验证：第一个词首字母大写，第二个词全小写
                if words[0][0].isupper() and words[1][0].islower():
                    species = candidate
    
    return clean_accession, species, header


def parse_fasta_file(fasta_path, encoding='utf-8'):
    """
    解析FASTA文件，返回序列列表。
    每条序列: {'accession': str, 'species': str, 'sequence': str, 'original_header': str}
    """
    sequences = []
    current = None
    
    with open(fasta_path, 'r', encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('>'):
                # 新序列
                if current is not None:
                    sequences.append(current)
                
                accession, species, full_header = parse_ncbi_header(line)
                current = {
                    'accession': accession or '',
                    'species': species or '',
                    'sequence': '',
                    'original_header': full_header,
                }
            else:
                if current is not None:
                    current['sequence'] += line
    
    # 最后一条
    if current is not None:
        sequences.append(current)
    
    return sequences


def save_csv(sequences, csv_path, encoding='utf-8'):
    """将解析结果保存为CSV"""
    with open(csv_path, 'w', encoding=encoding, newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Accession', 'Species'])
        for seq in sequences:
            writer.writerow([seq['accession'], seq['species']])
    print(f"CSV已保存到: {csv_path}")


def save_fasta(sequences, fasta_path, rename_mode=None, encoding='utf-8'):
    """
    保存FASTA文件。
    rename_mode: None=保持原样, 'species'=用物种名, 'accession'=用整齐序列号
    """
    with open(fasta_path, 'w', encoding=encoding) as f:
        for seq in sequences:
            if rename_mode == 'species' and seq['species']:
                # 用物种名作为序列名
                name = seq['species'].replace(' ', '_')
            elif rename_mode == 'accession' and seq['accession']:
                # 用整齐序列号
                name = seq['accession']
            else:
                # 保持原样
                name = seq['original_header']
            
            f.write(f">{name}\n")
            
            # 序列每行80字符
            seq_str = seq['sequence']
            for i in range(0, len(seq_str), 80):
                f.write(seq_str[i:i+80] + '\n')
    
    print(f"FASTA已保存到: {fasta_path}")


def print_summary(sequences):
    """打印解析摘要"""
    total = len(sequences)
    with_accession = sum(1 for s in sequences if s['accession'])
    with_species = sum(1 for s in sequences if s['species'])
    
    print(f"\n=== 解析摘要 ===")
    print(f"总序列数: {total}")
    print(f"成功提取序列号: {with_accession}/{total}")
    print(f"成功提取物种名: {with_species}/{total}")
    
    if with_species < total:
        missing = [s['accession'] or s['original_header'][:30] 
                   for s in sequences if not s['species']]
        print(f"\n未提取到物种名的序列（前5个）:")
        for m in missing[:5]:
            print(f"  - {m}")
        if len(missing) > 5:
            print(f"  ... 还有 {len(missing)-5} 个")


def interactive_rename(sequences):
    """交互式询问用户是否要重命名"""
    print("\n=== 重命名选项 ===")
    print("1. 将序列名替换为物种名（如 Species_name）")
    print("2. 将序列名替换为整齐序列号（如 AB123456.1）")
    print("3. 不重命名，仅输出CSV")
    
    choice = input("\n请选择 (1/2/3, 默认3): ").strip()
    
    if choice == '1':
        return 'species'
    elif choice == '2':
        return 'accession'
    else:
        return None


def main():
    parser = argparse.ArgumentParser(
        description='FASTA头解析+序列号提取+可选重命名工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  # 仅解析生成CSV
  python parse_fasta_headers.py -f sequences.fasta
  
  # 解析+重命名为物种名
  python parse_fasta_headers.py -f sequences.fasta --rename-species
  
  # 解析+重命名为整齐序列号
  python parse_fasta_headers.py -f sequences.fasta --rename-accession
  
  # 交互模式（会询问重命名选项）
  python parse_fasta_headers.py -f sequences.fasta --interactive
        '''
    )
    parser.add_argument('-f', '--fasta', required=True, help='FASTA文件路径')
    parser.add_argument('-o', '--output', default=None, help='输出文件路径')
    parser.add_argument('--csv', default=None, help='CSV输出路径（默认自动命名）')
    parser.add_argument('--rename-species', action='store_true',
                        help='将序列名替换为物种名')
    parser.add_argument('--rename-accession', action='store_true',
                        help='将序列名替换为整齐序列号')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='交互模式，询问重命名选项')
    parser.add_argument('--encoding', default='utf-8', help='文件编码')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.fasta):
        print(f"错误：FASTA文件不存在: {args.fasta}")
        sys.exit(1)
    
    # 解析FASTA
    print(f"正在解析: {args.fasta}")
    sequences = parse_fasta_file(args.fasta, args.encoding)
    
    if not sequences:
        print("错误：未找到任何序列")
        sys.exit(1)
    
    # 打印摘要
    print_summary(sequences)
    
    # 确定重命名模式
    rename_mode = None
    if args.rename_species:
        rename_mode = 'species'
    elif args.rename_accession:
        rename_mode = 'accession'
    elif args.interactive:
        rename_mode = interactive_rename(sequences)
    
    # 保存CSV（总是生成）
    base, ext = os.path.splitext(args.fasta)
    csv_path = args.csv or f"{base}_mapping.csv"
    save_csv(sequences, csv_path, args.encoding)
    
    # 保存FASTA（如果需要重命名）
    if rename_mode:
        fasta_path = args.output or f"{base}_renamed.fasta"
        save_fasta(sequences, fasta_path, rename_mode, args.encoding)
        
        if rename_mode == 'species':
            print(f"\n已将序列名替换为物种名")
            print("提示：物种名中的空格已替换为下划线，以兼容FASTA格式")
            print("在树图中显示时，可在绘图软件中设置下划线显示为空格+斜体")
        else:
            print(f"\n已将序列名替换为整齐序列号")
    else:
        print(f"\n仅生成CSV，未修改FASTA文件")
        print(f"如需重命名，请使用 --rename-species 或 --rename-accession 参数")


if __name__ == '__main__':
    main()
