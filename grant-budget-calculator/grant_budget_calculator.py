#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基金预算自动计算+分项汇总"""
import os, sys, csv

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def calculate_grant_budget(budget_file, output_file=None):
    """从预算表CSV自动计算分项汇总和总预算

    输入格式: category,item,unit_price,quantity,notes
    """
    categories = {}
    items = []
    total = 0

    with open(budget_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row.get('category', row.get('Category', 'Other'))
            item = row.get('item', row.get('Item', ''))
            try:
                unit_price = float(row.get('unit_price', row.get('UnitPrice', 0)))
                quantity = float(row.get('quantity', row.get('Quantity', 1)))
            except ValueError:
                continue
            notes = row.get('notes', row.get('Notes', ''))

            subtotal = unit_price * quantity
            total += subtotal

            categories.setdefault(category, 0)
            categories[category] += subtotal

            items.append({
                'category': category,
                'item': item,
                'unit_price': unit_price,
                'quantity': quantity,
                'subtotal': subtotal,
                'notes': notes
            })

    # 输出
    out_path = output_file or os.path.splitext(budget_file)[0] + "_summary.tsv"

    with open(out_path, 'w', encoding='utf-8') as out:
        out.write("=== 基金预算分项汇总 ===\n\n")
        out.write("## 分项汇总\n")
        out.write("Category\tAmount\tPercentage\n")
        for cat, amount in sorted(categories.items(), key=lambda x: -x[1]):
            pct = amount / total * 100 if total > 0 else 0
            out.write(f"{cat}\t{amount:.2f}\t{pct:.1f}%\n")
        out.write(f"TOTAL\t{total:.2f}\t100.0%\n")

        out.write(f"\n## 详细明细\n")
        out.write("Category\tItem\tUnitPrice\tQuantity\tSubtotal\tNotes\n")
        for item in items:
            out.write(f"{item['category']}\t{item['item']}\t{item['unit_price']:.2f}\t{item['quantity']}\t{item['subtotal']:.2f}\t{item['notes']}\n")

    print(f"Grant budget calculation complete")
    print(f"  Items: {len(items)}")
    print(f"  Categories: {len(categories)}")
    print(f"  Total budget: {total:.2f}")
    for cat, amount in sorted(categories.items(), key=lambda x: -x[1]):
        pct = amount / total * 100 if total > 0 else 0
        print(f"    {cat}: {amount:.2f} ({pct:.1f}%)")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  基金预算自动计算+分项汇总")
    print("=" * 60)
    budget_file = get_input("预算表CSV路径(category/item/unit_price/quantity/notes)", "budget.csv")
    output = get_input("输出文件路径", "")
    calculate_grant_budget(budget_file, output or None)

if __name__ == "__main__":
    main()
