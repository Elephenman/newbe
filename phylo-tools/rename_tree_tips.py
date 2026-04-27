#!/usr/bin/env python3
"""
脚本1：树文件枝名批量替换
功能：读取CSV表格（第1列=序列号，第2列=物种名），识别树文件中的序列号，
     将枝名替换为物种名（或整齐的序列号），支持Newick/Nexus格式。

用法：
  python rename_tree_tips.py -t tree.nwk -c mapping.csv --column 2 -o tree_renamed.nwk
  python rename_tree_tips.py -t tree.nwk -c mapping.csv --column 1 -o tree_clean.nwk

参数：
  -t, --tree      树文件路径（Newick或Nexus格式）
  -c, --csv       CSV表格路径（第1列=序列号，第2列=物种名）
  --column        替换为第几列的内容（1=整齐序列号，2=物种名，默认2）
  -o, --output    输出文件路径（默认在原文件名后加_renamed）
  --italic        在物种名前后加下划线标记斜体（Newick中用_表示空格，此选项会包裹italic标记）
  --encoding      文件编码（默认utf-8）
"""

import argparse
import csv
import re
import os
import sys


def read_csv_mapping(csv_path, encoding='utf-8'):
    """读取CSV，返回 {序列号: {1: 序列号, 2: 物种名}} 的映射字典"""
    mapping = {}
    with open(csv_path, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        header = next(reader, None)  # 跳过表头
        
        for row in reader:
            if len(row) < 2:
                continue
            accession = row[0].strip()
            species = row[1].strip()
            if accession:
                mapping[accession] = {1: accession, 2: species}
    return mapping


def find_accession_in_label(label, known_accessions):
    """
    在枝名中查找匹配的序列号。
    枝名可能是 "AB123456.1_Species_name_other_stuff" 这样的格式，
    需要从已知序列号列表中匹配。
    """
    # 策略1：直接匹配整个label（清理后）
    clean_label = label.strip().strip("'").strip('"')
    if clean_label in known_accessions:
        return clean_label
    
    # 策略2：在label中搜索已知序列号
    for acc in known_accessions:
        # 去掉版本号的匹配（AB123456.1 → 也匹配 AB123456）
        acc_base = acc.split('.')[0]
        if acc in label or acc_base in label:
            return acc
    
    # 策略3：用正则提取可能的序列号，然后匹配
    # NCBI序列号格式：字母2-4个+数字5-8个+.+版本号，如 AB123456.1, PP987654.1, MW_123456
    patterns = [
        r'[A-Za-z]{1,4}\d{5,8}(?:\.\d+)?',  # 标准NCBI格式
        r'[A-Za-z]{1,2}_?\d{5,8}(?:\.\d+)?',  # 带下划线格式
    ]
    
    for pattern in patterns:
        found = re.findall(pattern, label)
        for match in found:
            match_base = match.split('.')[0]
            for acc in known_accessions:
                acc_base = acc.split('.')[0]
                if match == acc or match_base == acc_base:
                    return acc
    
    return None


def replace_tips_in_newick(newick_str, mapping, column=2, italic=False):
    """
    在Newick字符串中替换枝名。
    找到所有枝名，匹配序列号，替换为目标名称。
    """
    known_accessions = list(mapping.keys())
    
    # 提取所有枝名（在逗号/左括号后，冒号/逗号/右括号/分号前的部分）
    # Newick枝名可能被引号包裹，也可能包含下划线
    tip_pattern = re.compile(
        r'(?<=[,\(])'           # 前面是逗号或左括号
        r'\s*'                   # 可能有空格
        r'([\'"]?[^,:;\(\)]+?)' # 枝名（可能被引号包裹）
        r'(?='                   # 后面是以下之一
        r'[:,\);]'              # 冒号、逗号、右括号、分号
        r'|$'                   # 或字符串结尾
        r')'
    )
    
    # 更健壮的方案：直接按位置提取和替换
    result = newick_str
    replacements = []
    
    # 找到所有可能的枝名位置
    # 枝名在 ( 或 , 之后，: 或 , 或 ) 或 ; 之前
    i = 0
    while i < len(result):
        # 找到枝名的开始位置
        start = -1
        while i < len(result) and result[i] in ' \t':
            i += 1
        
        if i < len(result) and result[i] not in '(),;:':
            # 可能是枝名的开始
            start = i
            # 找到枝名的结束
            in_quotes = False
            quote_char = None
            if result[i] in '\'"':
                in_quotes = True
                quote_char = result[i]
                i += 1
            
            while i < len(result):
                if in_quotes:
                    if result[i] == quote_char:
                        i += 1
                        break
                else:
                    if result[i] in ':,);':
                        break
                i += 1
            
            tip_label = result[start:i].strip().strip("'").strip('"')
            if tip_label:
                matched_acc = find_accession_in_label(tip_label, known_accessions)
                if matched_acc:
                    new_name = mapping[matched_acc][column]
                    if italic and column == 2:
                        # 在物种名前后加标记，用于后续渲染斜体
                        new_name = f'_italic_{new_name}_italic_'
                    replacements.append((start, i, new_name))
        else:
            i += 1
    
    # 从后向前替换，避免偏移
    for start, end, new_name in reversed(replacements):
        # 检查原始文本是否被引号包裹
        original = result[start:end]
        if original.startswith("'") or original.startswith('"'):
            quote = original[0]
            result = result[:start] + f"{quote}{new_name}{quote}" + result[end:]
        else:
            result = result[:start] + new_name + result[end:]
    
    return result


def process_tree_file(tree_path, csv_path, column=2, output_path=None, italic=False, encoding='utf-8'):
    """主处理流程"""
    # 读取CSV映射
    mapping = read_csv_mapping(csv_path, encoding)
    if not mapping:
        print("错误：CSV文件中没有有效数据")
        sys.exit(1)
    print(f"已读取 {len(mapping)} 条映射记录")
    
    # 读取树文件
    with open(tree_path, 'r', encoding=encoding) as f:
        tree_content = f.read()
    
    # 判断格式
    is_nexus = tree_content.strip().startswith('#NEXUS')
    
    if is_nexus:
        # Nexus格式：提取Newick部分
        translate_block = None
        tree_block = None
        
        # 提取Translate块（如果有）
        trans_match = re.search(r'Translate\s*(.*?)\s*;', tree_content, re.IGNORECASE | re.DOTALL)
        if trans_match:
            translate_block = trans_match.group(1)
        
        # 提取Tree块
        tree_match = re.search(r'Tree\s+\S+\s*=\s*(.*?;)', tree_content, re.IGNORECASE | re.DOTALL)
        if tree_match:
            tree_block = tree_match.group(1)
    else:
        tree_block = tree_content.strip()
    
    if not tree_block:
        print("错误：无法从树文件中提取Newick字符串")
        sys.exit(1)
    
    # 替换枝名
    new_tree = replace_tips_in_newick(tree_block, mapping, column, italic)
    
    # 统计替换结果
    replaced = sum(1 for acc in mapping if any(acc in tip for tip in re.findall(r'[^,:;\(\)]+', tree_block)))
    print(f"已替换 {len(mapping)} 个枝名")
    
    # 输出
    if output_path is None:
        base, ext = os.path.splitext(tree_path)
        output_path = f"{base}_renamed{ext}"
    
    if is_nexus:
        # 重新组装Nexus文件
        output_content = tree_content
        if tree_match:
            output_content = tree_content[:tree_match.start(1)] + new_tree + tree_content[tree_match.end(1):]
    else:
        output_content = new_tree
    
    with open(output_path, 'w', encoding=encoding) as f:
        f.write(output_content)
    
    print(f"已输出到: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='树文件枝名批量替换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  # 替换为物种名
  python rename_tree_tips.py -t tree.nwk -c mapping.csv --column 2 -o tree_species.nwk
  
  # 替换为整齐序列号
  python rename_tree_tips.py -t tree.nwk -c mapping.csv --column 1 -o tree_clean.nwk
  
  # 物种名加斜体标记
  python rename_tree_tips.py -t tree.nwk -c mapping.csv --column 2 --italic
        '''
    )
    parser.add_argument('-t', '--tree', required=True, help='树文件路径（Newick或Nexus）')
    parser.add_argument('-c', '--csv', required=True, help='CSV映射表路径（第1列=序列号，第2列=物种名）')
    parser.add_argument('--column', type=int, default=2, choices=[1, 2],
                        help='替换为第几列（1=序列号，2=物种名，默认2）')
    parser.add_argument('-o', '--output', default=None, help='输出文件路径')
    parser.add_argument('--italic', action='store_true', help='物种名加斜体标记')
    parser.add_argument('--encoding', default='utf-8', help='文件编码（默认utf-8）')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.tree):
        print(f"错误：树文件不存在: {args.tree}")
        sys.exit(1)
    if not os.path.exists(args.csv):
        print(f"错误：CSV文件不存在: {args.csv}")
        sys.exit(1)
    
    process_tree_file(args.tree, args.csv, args.column, args.output, args.italic, args.encoding)


if __name__ == '__main__':
    main()
