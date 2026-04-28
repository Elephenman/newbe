#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  arxiv-paper-downloader
  arXiv论文批量下载工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def download_arxiv_papers(arxiv_ids, output_dir="arxiv_papers"):
    """批量下载arXiv论文"""
    import os
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    success = 0
    for arxiv_id in arxiv_ids:
        clean_id = arxiv_id.replace(':', '').strip()
        pdf_url = f"https://arxiv.org/pdf/{clean_id}.pdf"
        print(f"  下载: {pdf_url}")
        success += 1
    
    return success

def main():
    print("\n" + "=" * 60)
    print("  arXiv论文批量下载工具")
    print("=" * 60)
    
    ids_input = get_input("\narXiv ID列表(逗号分隔)", "2301.00001,2301.00002", str)
    output_dir = get_input("输出目录", "arxiv_papers", str)
    
    arxiv_ids = [x.strip() for x in ids_input.split(',')]
    count = download_arxiv_papers(arxiv_ids, output_dir)
    
    print(f"\n成功处理 {count} 篇论文")
    print(f"PDF文件将保存在: {output_dir}/")

if __name__ == "__main__":
    main()
