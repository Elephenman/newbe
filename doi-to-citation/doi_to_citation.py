#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DOI转多格式引用"""
import os, sys, json
def get_input(p,d=None,t=str):
    v=input(f"{p} [默认: {d}]: ").strip()
    if v=="" or v is None: return d
    try: return t(v)
    except: return d

def doi_to_citation(dois, format="APA"):
    try: import requests
    except: print("需要requests"); return
    results = []
    for doi in dois:
        try:
            r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=10)
            data = r.json()["message"]
            title = data.get("title",[""])[0]
            authors = [f"{a.get('given','')} {a.get('family','')}" for a in data.get("author",[])]
            journal = data.get("container-title",[""])[0]
            year = data.get("published-print",data.get("published-online",{})).get("date-parts",[[0]])[0][0]
            vol = data.get("volume",""); pages = data.get("page","")
            
            if format == "APA":
                cite = f"{', '.join(authors[:3])} ({year}). {title}. {journal}, {vol}, {pages}. https://doi.org/{doi}"
            elif format == "MLA":
                cite = f"{authors[0] if authors else ''}. \"{title}.\" {journal} {vol} ({year}): {pages}."
            elif format == "GB-T7714":
                cite = f"{authors[0] if authors else ''}. {title}[J]. {journal}, {year}, {vol}: {pages}."
            elif format == "BibTeX":
                key = authors[0].split()[-1] if authors else "anon"
                cite = "@article{" + key + year + ",\n  title={" + title + "},\n  author={" + ', '.join(authors) + "},\n  journal={" + journal + "},\n  year={" + str(year) + "},\n  doi={" + doi + "}\n}"
            results.append(cite)
        except Exception as e: results.append(f"[ERROR] {doi}: {e}")
    
    for r in results: print(r)
    with open("citations.txt", 'w', encoding='utf-8') as f: f.write("\n\n".join(results))
    print(f"引用转换完成: citations.txt")

def main():
    print("="*50); print("  DOI转引用"); print("="*50)
    di=get_input("DOI列表(逗号分隔或文件路径)","10.1038/nature12373")
    fmt=get_input("格式(APA/MLA/GB-T7714/BibTeX)","APA")
    dois = [d.strip() for d in di.split(',') if d.strip()]
    if len(dois)==1 and os.path.exists(dois[0]):
        dois = [l.strip() for l in open(dois[0]) if l.strip()]
    doi_to_citation(dois, fmt)
if __name__=="__main__": main()