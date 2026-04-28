#!/usr/bin/env python3
"""VCF INFO字段批量解析到表格"""

# VCF INFO字段批量解析
import gzip

print("=" * 60)
print("  🧬 VCF INFO字段解析器")
print("=" * 60)

input_vcf = get_input("输入VCF文件路径", "variants.vcf")
fields_str = get_input("要解析的INFO字段(逗号分隔)", "AF,DP,AC")
output_file = get_input("输出表格路径", "vcf_info_table.tsv")
filter_expr = get_input("过滤条件(如DP>10或none)", "none")

fields = [f.strip() for f in fields_str.split(',') if f.strip()]

opener = gzip.open if input_vcf.endswith('.gz') else open
mode = 'rt' if input_vcf.endswith('.gz') else 'r'

header_cols = ['#CHROM', 'POS', 'ID', 'REF', 'ALT'] + fields
rows = []

with opener(input_vcf, mode) as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        info = parts[7]
        info_dict = {}
        for item in info.split(';'):
            if '=' in item:
                k, v = item.split('=', 1)
                info_dict[k] = v
            else:
                info_dict[item] = 'True'
        
        row = parts[:5]
        for field in fields:
            row.append(info_dict.get(field, 'NA'))
        
        if filter_expr != "none":
            try:
                field_name = filter_expr.split('>')[0].split('<')[0].split('=')[0]
                threshold = float(filter_expr.split('>')[1].split('<')[1].split('=')[1] if '=' in filter_expr else filter_expr.split('>')[1] if '>' in filter_expr else filter_expr.split('<')[1])
                val = info_dict.get(field_name, 'NA')
                if val == 'NA':
                    continue
                if '>' in filter_expr and float(val) <= threshold:
                    continue
                if '<' in filter_expr and float(val) >= threshold:
                    continue
            except:
                pass
        rows.append(row)

with open(output_file, 'w') as f:
    f.write('\t'.join(header_cols) + '\n')
    for row in rows:
        f.write('\t'.join(row) + '\n')

print(f"\n✅ 解析完成: {len(rows)} 条变异记录")
print(f"  提取字段: {', '.join(fields)}")
print(f"📄 结果已保存到: {output_file}")
