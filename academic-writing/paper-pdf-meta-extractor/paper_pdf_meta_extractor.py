#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF论文元数据自动提取"""
import os, sys, re
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def extract_pdf_meta(filepath, dims="all", obsidian_note=False, vault_path=None):
    try: import pdfplumber
    except: print("需要pdfplumber"); return
    
    results = []
    if os.path.isdir(filepath):
        files = [f for f in os.listdir(filepath) if f.endswith('.pdf')]
    else:
        files = [filepath]
    
    for pdf_path in files:
        meta = {"file": os.path.basename(pdf_path)}
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # 从PDF元数据提取
                pdf_meta = pdf.metadata or {}
                meta["title"] = pdf_meta.get("Title", "")
                meta["authors"] = pdf_meta.get("Author", "")
                meta["doi"] = ""
                
                # 从第一页文本提取(补充)
                first_page = pdf.pages[0].extract_text() or ""
                # DOI提取
                doi_match = re.search(r'(10\.\d{4,}/[^\s]+)', first_page)
                if doi_match: meta["doi"] = doi_match.group(1).rstrip('.')
                # Title补充(如果PDF元数据空)
                if not meta["title"]:
                    lines = first_page.split('\n')[:5]
                    meta["title"] = lines[0].strip() if lines else ""
                # Abstract提取
                abs_match = re.search(r'(?:Abstract|ABSTRACT)[:\s]*(.*?)(?:\n\n|Introduction|1\.|Keywords)', first_page, re.DOTALL)
                meta["abstract"] = abs_match.group(1).strip()[:500] if abs_match else ""
                # Keywords
                kw_match = re.search(r'(?:Keywords|KEYWORDS)[:\s]*(.*?)(?:\n|\.)', first_page)
                meta["keywords"] = kw_match.group(1).strip() if kw_match else ""
        except Exception as e: meta["error"] = str(e)
        results.append(meta)
    
    # 输出
    print(f"PDF元数据提取完成: {len(results)}个文件")
    for m in results:
        print(f"  {m['file']}")
        print(f"    标题: {m.get('title','')[:80]}")
        print(f"    作者: {m.get('authors','')[:60]}")
        print(f"    DOI: {m.get('doi','')}")
    
    # CSV
    import csv
    with open("pdf_metadata.csv", 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=["file","title","authors","doi","abstract","keywords"])
        w.writeheader(); w.writerows(results)
    print("元数据CSV: pdf_metadata.csv")
    
    # Obsidian笔记
    if obsidian_note:
        vault = vault_path or "."
        for m in results:
            if m.get("error"): continue
            note_path = os.path.join(vault, f"{m.get('title','untitled')[:50].replace(' ','_')}.md")
            tags = m.get("keywords","").replace(",","/").replace(";","/")
            note = f"""---
title: "{m.get('title','')}"
authors: "{m.get('authors','')}"
doi: "{m.get('doi','')}"
tags: [paper, {tags}]
date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}
---

# {m.get('title','')}

**Authors**: {m.get('authors','')}
**DOI**: {m.get('doi','')}

## Abstract
{m.get('abstract','')}

## Keywords
{m.get('keywords','')}

## Notes
- 
"""
            with open(note_path, 'w', encoding='utf-8') as f: f.write(note)
            print(f"Obsidian笔记: {note_path}")

def main():
    print("="*50); print("  PDF元数据提取"); print("="*50)
    fp = get_input("PDF文件/目录路径", "paper.pdf")
    dm = get_input("提取维度(all/title/authors/doi/abstract)", "all")
    ob = get_input("生成Obsidian笔记(yes/no)", "no")
    vp = get_input("Obsidian vault路径", ".")
    extract_pdf_meta(fp, dm, ob.lower() in ('yes','y'), vp)

if __name__ == "__main__": main()