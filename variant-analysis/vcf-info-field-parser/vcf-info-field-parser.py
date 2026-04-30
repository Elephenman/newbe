#!/usr/bin/env python3
"""VCF INFO字段批量解析到表格 - 支持复杂过滤表达式"""

import gzip
import re

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def parse_filter_expr(expr):
    """
    Parse complex filter expressions with AND/OR operators and parentheses.
    Supports: field>value, field<value, field>=value, field<=value, field=value
    Combine with & (AND) or | (OR) and parentheses for grouping.

    Returns a function that takes an info_dict and returns True/False.
    """
    if not expr or expr.strip().lower() == 'none':
        return lambda info: True

    expr = expr.strip()

    # Tokenize: extract comparison expressions and logical operators
    # Match patterns like: DP>10, AF<=0.5, AC=2
    comparison_pattern = re.compile(
        r'(\w+)\s*(>=|<=|!=|>|<|=)\s*([0-9.eE+\-]+)'
    )

    # Find all comparisons and their positions
    comparisons = []
    for m in comparison_pattern.finditer(expr):
        field = m.group(1)
        op = m.group(2)
        value = m.group(3)
        try:
            if '.' in value or 'e' in value.lower():
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            value = float(value)
        comparisons.append({
            'field': field,
            'op': op,
            'value': value,
            'start': m.start(),
            'end': m.end(),
        })

    if not comparisons:
        print(f"警告: 无法解析过滤表达式 '{expr}'，将不过滤")
        return lambda info: True

    # Build a Python expression string for eval
    # Replace each comparison in the expression with a function call placeholder
    eval_parts = []
    last_end = 0
    for i, comp in enumerate(comparisons):
        # Add text between comparisons (logical operators, parentheses, etc.)
        between = expr[last_end:comp['start']].strip()
        # Convert logical operators
        between = between.replace('&', ' and ').replace('|', ' or ')
        # Handle word operators
        between = re.sub(r'\bAND\b', 'and', between, flags=re.IGNORECASE)
        between = re.sub(r'\bOR\b', 'or', between, flags=re.IGNORECASE)
        eval_parts.append(between)
        eval_parts.append(f"__cmp_{i}__")
        last_end = comp['end']

    # Add any trailing text
    trailing = expr[last_end:].strip()
    trailing = trailing.replace('&', ' and ').replace('|', ' or ')
    trailing = re.sub(r'\bAND\b', 'and', trailing, flags=re.IGNORECASE)
    trailing = re.sub(r'\bOR\b', 'or', trailing, flags=re.IGNORECASE)
    eval_parts.append(trailing)

    eval_expr = ' '.join(eval_parts)

    def filter_func(info_dict):
        # Evaluate each comparison
        local_vars = {}
        for i, comp in enumerate(comparisons):
            key = f"__cmp_{i}__"
            val_str = info_dict.get(comp['field'], 'NA')
            if val_str == 'NA' or val_str == 'True':
                local_vars[key] = False
                continue
            try:
                val = float(val_str)
            except (ValueError, TypeError):
                local_vars[key] = False
                continue

            op = comp['op']
            threshold = comp['value']
            if op == '>':
                local_vars[key] = val > threshold
            elif op == '>=':
                local_vars[key] = val >= threshold
            elif op == '<':
                local_vars[key] = val < threshold
            elif op == '<=':
                local_vars[key] = val <= threshold
            elif op == '=':
                local_vars[key] = val == threshold
            elif op == '!=':
                local_vars[key] = val != threshold
            else:
                local_vars[key] = False

        try:
            return bool(eval(eval_expr, {"__builtins__": {}}, local_vars))
        except Exception:
            return False

    return filter_func

def main():
    print("=" * 60)
    print("  VCF INFO字段解析器")
    print("=" * 60)

    input_vcf = get_input("输入VCF文件路径", "variants.vcf", str)
    fields_str = get_input("要解析的INFO字段(逗号分隔)", "AF,DP,AC", str)
    output_file = get_input("输出表格路径", "vcf_info_table.tsv", str)
    filter_expr = get_input("过滤条件(如DP>10&AF<0.5 或 none)", "none", str)

    fields = [f.strip() for f in fields_str.split(',') if f.strip()]
    filter_func = parse_filter_expr(filter_expr)

    opener = gzip.open if input_vcf.endswith('.gz') else open
    mode = 'rt' if input_vcf.endswith('.gz') else 'r'

    header_cols = ['#CHROM', 'POS', 'ID', 'REF', 'ALT'] + fields
    rows = []

    with opener(input_vcf, mode) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 8:
                continue
            info = parts[7]
            info_dict = {}
            for item in info.split(';'):
                if '=' in item:
                    k, v = item.split('=', 1)
                    info_dict[k] = v
                else:
                    info_dict[item] = 'True'

            # Apply filter
            if not filter_func(info_dict):
                continue

            row = parts[:5]
            for field in fields:
                row.append(info_dict.get(field, 'NA'))
            rows.append(row)

    with open(output_file, 'w') as f:
        f.write('\t'.join(header_cols) + '\n')
        for row in rows:
            f.write('\t'.join(row) + '\n')

    print(f"\n解析完成: {len(rows)} 条变异记录")
    print(f"  提取字段: {', '.join(fields)}")
    print(f"  过滤条件: {filter_expr}")
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
