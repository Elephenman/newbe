#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""实验样本表格式校验器"""
import os, sys
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def validate_sample_sheet(filepath, required_cols="sample_id,group,condition", species="human", make_report=True):
    try: import pandas as pd
    except: print("需要pandas"); return
    
    df = pd.read_csv(filepath)
    warnings = []; errors = []; checks_passed = 0
    
    # 必填列检查
    req = required_cols.split(',')
    for col in req:
        if col.strip() not in df.columns:
            errors.append(f"缺少必填列: '{col.strip()}' ❌")
        else:
            checks_passed += 1
    
    # ID唯一性
    id_cols = [c for c in df.columns if 'id' in c.lower() or 'name' in c.lower() or 'sample' in c.lower()]
    for col in id_cols:
        duplicates = df[col].duplicated().sum()
        if duplicates > 0:
            errors.append(f"{col}有{duplicates}个重复值 ❌")
        else: checks_passed += 1
    
    # 分组合法性
    group_cols = [c for c in df.columns if 'group' in c.lower() or 'condition' in c.lower() or 'type' in c.lower()]
    for col in group_cols:
        unique_vals = df[col].nunique()
        if unique_vals < 2:
            warnings.append(f"{col}只有{unique_vals}个分组(建议至少2个) ⚠️")
        else: checks_passed += 1
    
    # 缺失值
    missing_pct = df.isnull().mean() * 100
    for col, pct in missing_pct.items():
        if pct > 50:
            warnings.append(f"{col}缺失{pct:.0f}% ⚠️")
        elif pct > 0:
            warnings.append(f"{col}缺失{pct:.0f}% (轻微)")
    
    # 样本数合理性
    min_samples_per_group = 3
    for col in group_cols:
        for grp, count in df[col].value_counts().items():
            if count < min_samples_per_group:
                warnings.append(f"{col}={grp}只有{count}个样本(建议≥{min_samples_per_group}) ⚠️")
    
    # 输出报告
    print(f"\n{'='*60}")
    print(f"  样本表校验报告")
    print(f"{'='*60}")
    print(f"  文件: {filepath}")
    print(f"  行数: {len(df)}, 列数: {len(df.columns)}")
    print(f"  检查通过: {checks_passed}")
    
    if errors:
        print(f"\n  【错误 ❌】")
        for e in errors: print(f"    {e}")
    if warnings:
        print(f"\n  【警告 ⚠️】")
        for w in warnings: print(f"    {w}")
    
    status = "PASS ✅" if not errors else "FAIL ❌"
    print(f"\n  总体状态: {status}")
    
    # 保存报告
    if make_report:
        with open("sample_validation_report.csv", 'w') as out:
            out.write("类型,消息\n")
            for e in errors: out.write(f"ERROR,{e}\n")
            for w in warnings: out.write(f"WARNING,{w}\n")
        print("校验报告: sample_validation_report.csv")

def main():
    print("="*50); print("  样本表校验器"); print("="*50)
    fp = get_input("样本表CSV路径", "sample_sheet.csv")
    rc = get_input("必填列(逗号分隔)", "sample_id,group,condition")
    sp = get_input("物种(human/mouse)", "human")
    mr = get_input("出校验报告(yes/no)", "yes")
    validate_sample_sheet(fp, rc, sp, mr.lower() in ('yes','y'))

if __name__ == "__main__": main()