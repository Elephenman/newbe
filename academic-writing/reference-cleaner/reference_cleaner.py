#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""参考文献格式统一清洗器"""
import os, sys, re
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def clean_references(filepath, target_format="APA", check_doi=True, fill_missing=True):
    try: import requests
    except: requests = None
    
    entries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 识别文件类型并解析
    if filepath.endswith('.bib'):
        # BibTeX解析
        bib_entries = re.findall(r'@\w+\{([^,]+),\s*(.*?)\n\}', content, re.DOTALL)
        for key, fields in bib_entries:
            entry = {"type": "bibtex", "key": key}
            for field_match in re.finditer(r'(\w+)\s*=\s*\{(.*?)\}', fields):
                entry[field_match.group(1)] = field_match.group(2)
            entries.append(entry)
    elif filepath.endswith('.ris'):
        # RIS解析
        ris_entries = []; current = {}
        for line in content.split('\n'):
            if line.startswith('TY '): current = {"type": "ris"}
            elif line.startswith('ER '): ris_entries.append(current); current = {}
            elif line.strip():
                tag, val = line[:6].strip(), line[6:].strip()
                current[tag] = val
        entries = ris_entries
    else:
        # CSV/TSV
        import csv
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader: entries.append({"type": "csv", **row})
    
    # DOI验证+补全
    for entry in entries:
        doi = entry.get("doi", entry.get("DOI", ""))
        if doi and check_doi and requests:
            try:
                r = requests.get(f"https://doi.org/{doi}", timeout=5, allow_redirects=True)
                if r.status_code == 200: entry["doi_valid"] = True
                else: entry["doi_valid"] = False
            except: entry["doi_valid"] = "timeout"
        
        if fill_missing and doi and requests:
            try:
                r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=10)
                data = r.json()["message"]
                if not entry.get("title"): entry["title"] = data.get("title",[""])[0]
                if not entry.get("author"): entry["author"] = "; ".join([f"{a.get('given','')} {a.get('family','')}" for a in data.get("author",[])])
                if not entry.get("journal"): entry["journal"] = data.get("container-title",[""])[0]
                if not entry.get("year"): entry["year"] = str(data.get("published-print",data.get("published-online",{})).get("date-parts",[[0]])[0][0])
            except: pass
    
    # 格式化输出
    formatted = []
    for entry in entries:
        title = entry.get("title", "")
        author = entry.get("author", entry.get("Author", ""))
        journal = entry.get("journal", entry.get("Journal", ""))
        year = entry.get("year", entry.get("Year", ""))
        doi = entry.get("doi", entry.get("DOI", ""))
        
        if target_format == "APA":
            cite = f"{author} ({year}). {title}. {journal}. https://doi.org/{doi}"
        elif target_format == "MLA":
            cite = f"{author}. \"{title}.\" {journal} ({year})."
        elif target_format == "GB-T7714":
            cite = f"{author}. {title}[J]. {journal}, {year}. DOI:{doi}"
        elif target_format == "BibTeX":
            key = author.split()[0] if author else "anon"
            cite = f"@article{{{key}{year},\n  title={{{title}}},\n  author={{{author}}},\n  journal={{{journal}}},\n  year={{{year}}},\n  doi={{{doi}}}\n}}"
        formatted.append(cite)
    
    # 保存
    out_path = filepath.replace('.bib','').replace('.ris','') + f"_cleaned_{target_format}.txt"
    with open(out_path, 'w', encoding='utf-8') as f: f.write("\n\n".join(formatted))
    
    # 报告
    invalid_doi = sum(1 for e in entries if e.get("doi_valid") == False)
    print(f"引文清洗完成")
    print(f"  条目数: {len(entries)}")
    print(f"  目标格式: {target_format}")
    if check_doi: print(f"  DOI无效: {invalid_doi}")
    print(f"  输出: {out_path}")

def main():
    print("="*50); print("  引文格式清洗器"); print("="*50)
    fp = get_input("引文文件路径(bib/ris/csv)", "references.bib")
    tf = get_input("目标格式(APA/MLA/GB-T7714/BibTeX)", "APA")
    cd = get_input("检查DOI有效性(yes/no)", "yes")
    fm = get_input("补全缺失字段(yes/no)", "yes")
    clean_references(fp, tf, cd.lower() in ('yes','y'), fm.lower() in ('yes','y'))

if __name__ == "__main__": main()