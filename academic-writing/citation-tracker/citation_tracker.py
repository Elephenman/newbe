#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""论文被引追踪器"""
import os, sys
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def track_citations(dois_pmids, time_range="3y", max_results=100, make_plot=True):
    try: import requests
    except: print("需要requests"); return
    
    results = []
    for identifier in dois_pmids:
        # 使用Semantic Scholar API
        if identifier.startswith('10.'):
            url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{identifier}?fields=citations,citationCount,title"
        else:
            url = f"https://api.semanticscholar.org/graph/v1/paper/PMID:{identifier}?fields=citations,citationCount,title"
        
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            title = data.get("title", "")
            total_citations = data.get("citationCount", 0)
            citations = data.get("citations", [])
            
            # 按年份统计
            year_counts = {}
            for c in citations[:max_results]:
                year = c.get("year") or "unknown"
                year_counts[year] = year_counts.get(year, 0) + 1
            
            results.append({"id": identifier, "title": title, "total": total_citations, "by_year": year_counts})
        except Exception as e:
            results.append({"id": identifier, "error": str(e)})
    
    # 输出
    print("被引追踪结果:")
    for r in results:
        if "error" in r: print(f"  {r['id']}: 错误 - {r['error']}"); continue
        print(f"  {r['id']}: {r['title'][:60]}")
        print(f"    总被引: {r['total']}")
        for y, c in sorted(r["by_year"].items()):
            print(f"    {y}: {c}")
    
    # 绘趋势图
    if make_plot:
        try:
            import matplotlib; matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 6))
            for r in results:
                if "error" in r or not r["by_year"]: continue
                years = sorted(r["by_year"].keys())
                counts = [r["by_year"][y] for y in years]
                plt.plot(years, counts, marker='o', label=r["id"][:20])
            plt.xlabel('年份'); plt.ylabel('被引数'); plt.title('被引趋势')
            plt.legend(); plt.tight_layout()
            plt.savefig("citation_trend.png", dpi=300); plt.close()
            print("趋势图: citation_trend.png")
        except: pass
    
    # 保存
    import json
    with open("citation_results.json", 'w') as f: json.dump(results, f, indent=2)
    print("结果JSON: citation_results.json")

def main():
    print("="*50); print("  被引追踪器"); print("="*50)
    ids = get_input("DOI或PMID(逗号分隔)", "10.1038/nature12373")
    tr = get_input("时间范围(近1年/3年/5年)", "3y")
    mr = get_input("最大返回数", 100, int)
    mp = get_input("出趋势图(yes/no)", "yes")
    dois = [i.strip() for i in ids.split(',') if i.strip()]
    track_citations(dois, tr, mr, mp.lower() in ('yes','y'))

if __name__ == "__main__": main()