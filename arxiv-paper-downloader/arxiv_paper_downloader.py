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
    import urllib.request
    import urllib.error

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    success = 0
    failed = 0

    for arxiv_id in arxiv_ids:
        clean_id = arxiv_id.replace(':', '').strip()
        filename = os.path.join(output_dir, f"{clean_id}.pdf")

        # Try arxiv.org first, then ar5iv.org as fallback
        urls = [
            f"https://arxiv.org/pdf/{clean_id}.pdf",
            f"https://ar5iv.org/pdf/{clean_id}",
        ]

        downloaded = False
        for url in urls:
            try:
                print(f"  正在下载: {url}")
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; arxiv-downloader/1.0)'
                })
                with urllib.request.urlopen(req, timeout=60) as response:
                    if response.status == 200:
                        # Verify it looks like a PDF (starts with %PDF)
                        data = response.read()
                        if data[:4] == b'%PDF' or len(data) > 1000:
                            with open(filename, 'wb') as f:
                                f.write(data)
                            file_size = os.path.getsize(filename)
                            print(f"    -> 成功: {filename} ({file_size:,} bytes)")
                            success += 1
                            downloaded = True
                            break
                        else:
                            print(f"    -> 响应非PDF格式, 尝试下一个URL")
            except urllib.error.HTTPError as e:
                print(f"    -> HTTP错误 {e.code}: {e.reason}")
            except urllib.error.URLError as e:
                print(f"    -> 网络错误: {e.reason}")
            except Exception as e:
                print(f"    -> 下载失败: {e}")

        if not downloaded:
            print(f"    -> 全部URL失败, 跳过 {clean_id}")
            failed += 1

    return success, failed

def main():
    print("\n" + "=" * 60)
    print("  arXiv论文批量下载工具")
    print("=" * 60)

    ids_input = get_input("\narXiv ID列表(逗号分隔)", "2301.00001,2301.00002", str)
    output_dir = get_input("输出目录", "arxiv_papers", str)

    arxiv_ids = [x.strip() for x in ids_input.split(',') if x.strip()]
    success, failed = download_arxiv_papers(arxiv_ids, output_dir)

    print(f"\n下载完成: {success} 篇成功, {failed} 篇失败 (共 {len(arxiv_ids)} 篇)")
    print(f"PDF文件保存在: {output_dir}/")

if __name__ == "__main__":
    main()
