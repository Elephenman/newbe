#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PubMed批量检索+结果导出"""
import os, sys, json
def get_input(p,d=None,t=str):
    v=input(f"{p} [默认: {d}]: ").strip()
    if v=="" or v is None: return d
    try: return t(v)
    except: return d

def search_pubmed(query, max_results=20, date_range=None, free_fulltext=False, format="csv"):
    try:
        from Bio import Entrez
        Entrez.email = "user@example.com"
    except:
        print("需要biopython: pip install biopython"); return
    
    search_term = query
    if date_range:
        search_term += f" AND {date_range}[dp]"
    if free_fulltext:
        search_term += " AND free full text[filter]"
    
    handle = Entrez.esearch(db="pubmed", term=search_term, retmax=max_results, retmode="json")
    results = json.loads(handle.read()); handle.close()
    id_list = results["esearchresult"]["idlist"]
    
    if not id_list: print("无结果"); return
    
    # 获取详情
    handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="text")
    abstracts = handle.read(); handle.close()
    
    # 获取摘要详情
    handle = Entrez.esummary(db="pubmed", id=id_list, retmode="json")
    summaries = json.loads(handle.read()); handle.close()
    
    rows = []
    for uid in id_list:
        s = summaries.get(uid, {})
        rows.append({
            "pmid": uid, "title": s.get("Title",""), "authors": "; ".join([a.get("Name","") for a in s.get("AuthorList",[])]),
            "doi": s.get("DOI",""), "journal": s.get("FullJournalName",""), "year": s.get("PubDate","").split()[0] if s.get("PubDate") else ""
        })
    
    # 保存
    out_path = "pubmed_search_results." + format
    if format == "csv":
        import csv
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=["pmid","title","authors","doi","journal","year"])
            w.writeheader(); w.writerows(rows)
    elif format == "bibtex":
        with open(out_path, 'w', encoding='utf-8') as f:
            for r in rows:
                f.write(f"@article{{pmid{r['pmid']},\n  title={{{{{r['title']}}}}},\n  author={{{{{r['authors']}}}}},\n  journal={{{{{r['journal']}}}}},\n  year={{{{{r['year']}}}}},\n  doi={{{{{r['doi']}}}}}\n}}\n\n")
    
    print(f"PubMed检索完成: {len(rows)} 条结果 -> {out_path}")
    for r in rows[:5]: print(f"  {r['pmid']}: {r['title'][:60]}...")

def main():
    print("="*50); print("  PubMed批量检索器"); print("="*50)
    q=get_input("搜索关键词","DNA damage repair")
    mr=get_input("最大返回数",20,int)
    dr=get_input("日期范围(如2020:2025[dp])","")
    ff=get_input("只取free-fulltext(yes/no)","no")
    fmt=get_input("导出格式(csv/bibtex)","csv")
    search_pubmed(q, mr, dr or None, ff.lower() in ('yes','y'), fmt)
if __name__=="__main__": main()