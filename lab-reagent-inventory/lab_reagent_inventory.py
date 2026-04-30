#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""实验室试剂库存管理+过期预警"""
import os, sys, csv
from datetime import datetime, timedelta

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def manage_reagent_inventory(inventory_file, output_file=None, warn_days=30):
    """管理试剂库存，检查过期预警

    输入CSV格式: name,catalog,lot_number,expiry_date,quantity,unit,location,notes
    """
    reagents = []
    today = datetime.now()
    warn_date = today + timedelta(days=warn_days)

    with open(inventory_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            reagents.append(row)

    if not reagents:
        print("[ERROR] No reagent data found. Expected CSV with columns: name,catalog,lot_number,expiry_date,quantity,unit,location,notes")
        return

    # 分析库存状态
    expired = []
    expiring_soon = []
    low_stock = []
    active = []

    for r in reagents:
        name = r.get('name', r.get('Name', 'Unknown'))
        expiry_str = r.get('expiry_date', r.get('Expiry', r.get('expiry', '')))

        status = "active"
        if expiry_str:
            try:
                expiry = datetime.strptime(expiry_str.strip(), '%Y-%m-%d')
                if expiry < today:
                    status = "expired"
                    expired.append(r)
                elif expiry < warn_date:
                    status = "expiring_soon"
                    expiring_soon.append(r)
            except ValueError:
                pass

        # 检查低库存
        try:
            quantity = float(r.get('quantity', r.get('Quantity', '0')))
            if quantity <= 0:
                status = "low_stock"
                low_stock.append(r)
        except ValueError:
            pass

        r['status'] = status
        if status == "active":
            active.append(r)

    # 输出
    out_path = output_file or os.path.splitext(inventory_file)[0] + "_report.tsv"

    with open(out_path, 'w', encoding='utf-8') as out:
        out.write("name\tcatalog\tlot_number\texpiry_date\tquantity\tunit\tlocation\tstatus\tnotes\n")
        for r in reagents:
            out.write("\t".join([
                r.get('name', ''),
                r.get('catalog', ''),
                r.get('lot_number', ''),
                r.get('expiry_date', ''),
                r.get('quantity', ''),
                r.get('unit', ''),
                r.get('location', ''),
                r.get('status', ''),
                r.get('notes', '')
            ]) + "\n")

    # 报告
    print(f"Reagent inventory report")
    print(f"  Total reagents: {len(reagents)}")
    print(f"  Active: {len(active)}")
    print(f"  Expired: {len(expired)}")
    print(f"  Expiring soon (<{warn_days}d): {len(expiring_soon)}")
    print(f"  Low stock: {len(low_stock)}")

    if expired:
        print(f"\n  [EXPIRED] Reagents:")
        for r in expired[:10]:
            print(f"    - {r.get('name', '?')} (expired: {r.get('expiry_date', '?')})")

    if expiring_soon:
        print(f"\n  [EXPIRING SOON] Reagents:")
        for r in expiring_soon[:10]:
            print(f"    - {r.get('name', '?')} (expires: {r.get('expiry_date', '?')})")

    print(f"\n  Report: {out_path}")

def main():
    print("=" * 60)
    print("  实验室试剂库存管理+过期预警")
    print("=" * 60)
    inventory_file = get_input("试剂库存CSV路径", "inventory.csv")
    output = get_input("输出报告路径", "")
    warn = get_input("过期预警天数", "30")
    manage_reagent_inventory(inventory_file, output or None, int(warn))

if __name__ == "__main__":
    main()
