#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""论文图片尺寸/格式合规检查"""
import os, sys
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

JOURNAL_SPECS = {
    "Nature": {"min_dpi": 300, "max_width_mm": 183, "max_height_mm": 247, "formats": ["TIFF","PDF","PNG"], "font_min_pt": 5},
    "Cell": {"min_dpi": 300, "max_width_mm": 170, "max_height_mm": 220, "formats": ["TIFF","PDF"], "font_min_pt": 6},
    "Science": {"min_dpi": 300, "max_width_mm": 89, "formats": ["TIFF","PDF","EPS"], "font_min_pt": 6},
    "custom": {"min_dpi": 300, "max_width_mm": 180, "formats": ["PNG","PDF"], "font_min_pt": 5},
}

def check_figure_size(filepath, journal="Nature", dims="all"):
    try: from PIL import Image
    except: print("需要Pillow"); return
    
    files = []
    if os.path.isdir(filepath):
        for f in os.listdir(filepath):
            if f.lower().endswith(('.png','.jpg','.jpeg','.tiff','.tif','.pdf','.eps')):
                files.append(os.path.join(filepath, f))
    else: files = [filepath]
    
    specs = JOURNAL_SPECS.get(journal, JOURNAL_SPECS["custom"])
    results = []
    
    for img_path in files:
        result = {"file": os.path.basename(img_path), "pass": True, "warnings": [], "errors": []}
        
        try:
            img = Image.open(img_path)
            w_px, h_px = img.size
            
            # DPI检查
            dpi = img.info.get("dpi", (72, 72))
            dpi_val = min(dpi)
            if dims in ["all", "DPI"]:
                if dpi_val < specs["min_dpi"]:
                    result["errors"].append(f"DPI={dpi_val} < {specs['min_dpi']} ❌")
                    result["pass"] = False
                else: result["warnings"].append(f"DPI={dpi_val} ✅")
            
            # 尺寸检查(像素→mm)
            w_mm = w_px / dpi_val * 25.4; h_mm = h_px / dpi_val * 25.4
            if dims in ["all", "尺寸"]:
                if "max_width_mm" in specs and w_mm > specs["max_width_mm"]:
                    result["errors"].append(f"宽度={w_mm:.0f}mm > {specs['max_width_mm']}mm ❌")
                    result["pass"] = False
                if "max_height_mm" in specs and h_mm > specs["max_height_mm"]:
                    result["errors"].append(f"高度={h_mm:.0f}mm > {specs['max_height_mm']}mm ❌")
                    result["pass"] = False
            
            # 格式检查
            fmt = img.format or os.path.splitext(img_path)[1][1:].upper()
            if dims in ["all", "格式"]:
                if fmt.upper() not in specs["formats"]:
                    result["warnings"].append(f"格式={fmt}不在推荐列表{specs['formats']}中 ⚠️")
            
            result["width"] = w_px; result["height"] = h_px
            result["dpi"] = dpi_val; result["format"] = fmt
        except Exception as e: result["errors"].append(f"无法打开: {e}"); result["pass"] = False
        
        results.append(result)
    
    # 输出报告
    print(f"\n{'='*60}")
    print(f"  图片合规检查报告 ({journal})")
    print(f"{'='*60}")
    for r in results:
        status = "✅ PASS" if r["pass"] else "❌ FAIL"
        print(f"  {r['file']}: {status}")
        for w in r["warnings"]: print(f"    {w}")
        for e in r["errors"]: print(f"    {e}")
    
    pass_count = sum(1 for r in results if r["pass"])
    print(f"  合格率: {pass_count}/{len(results)} ({round(pass_count/len(results)*100)}%)")
    
    # 保存
    import csv
    with open("figure_check_report.csv", 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=["file","pass","width","height","dpi","format","warnings","errors"])
        w.writeheader(); w.writerows(results)
    print(f"  报告CSV: figure_check_report.csv")

def main():
    print("="*50); print("  图片合规检查器"); print("="*50)
    fp = get_input("图片文件/目录路径", "figures/")
    jo = get_input("目标期刊(Nature/Cell/Science/custom)", "Nature")
    dm = get_input("检查维度(DPI/尺寸/格式/all)", "all")
    check_figure_size(fp, jo, dm)

if __name__ == "__main__": main()