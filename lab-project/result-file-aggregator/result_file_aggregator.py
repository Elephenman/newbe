#!/usr/bin/env python3
"""分析结果文件自动汇总+索引生成
扫描指定目录下的分析结果文件，汇总关键统计信息，生成索引文件
"""

import os
import sys
import glob


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def scan_result_files(directory, extensions=None):
    """扫描目录中的结果文件"""
    if extensions is None:
        extensions = ['.csv', '.tsv', '.txt', '.xlsx', '.pdf', '.png', '.jpg', '.rds', '.h5ad']

    found = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fname in files:
            fpath = os.path.join(root, fname)
            ext = os.path.splitext(fname)[1].lower()
            if ext in extensions:
                try:
                    fsize = os.path.getsize(fpath)
                    mtime = os.path.getmtime(fpath)
                    found.append({
                        'path': fpath,
                        'name': fname,
                        'ext': ext,
                        'size': fsize,
                        'mtime': mtime,
                        'relpath': os.path.relpath(fpath, directory)
                    })
                except OSError:
                    continue
    return found


def extract_csv_stats(filepath, max_lines=5):
    """从CSV/TSV文件提取摘要统计"""
    stats = {'rows': 0, 'cols': 0, 'header': '', 'preview': []}
    try:
        sep = '\t' if filepath.endswith('.tsv') else ','
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            header = f.readline().strip()
            stats['header'] = header
            stats['cols'] = len(header.split(sep))
            for line in f:
                if line.strip() and not line.startswith('#'):
                    stats['rows'] += 1
                    if len(stats['preview']) < max_lines:
                        stats['preview'].append(line.strip())
    except Exception:
        pass
    return stats


def main():
    print("=" * 60)
    print("  分析结果文件自动汇总+索引生成")
    print("=" * 60)
    print()

    input_dir = get_input("结果目录路径", "results/")
    output_file = get_input("输出汇总路径", "results_index.tsv")
    ext_filter = get_input("文件扩展名过滤(逗号分隔,留空=全部)", "")
    min_size = get_input("最小文件大小(bytes)", "0", int)

    print()
    print(f"扫描目录:  {input_dir}")
    print(f"输出:      {output_file}")
    print()

    if not os.path.isdir(input_dir):
        print(f"[ERROR] 目录不存在: {input_dir}")
        sys.exit(1)

    # Parse extension filter
    if ext_filter:
        extensions = [e.strip() if e.strip().startswith('.') else '.' + e.strip()
                      for e in ext_filter.split(',') if e.strip()]
    else:
        extensions = None

    # Scan files
    print("[Processing] 扫描文件...")
    files = scan_result_files(input_dir, extensions)
    files = [f for f in files if f['size'] >= min_size]
    files.sort(key=lambda x: x['mtime'], reverse=True)

    print(f"[Processing] 找到 {len(files)} 个文件")

    # Categorize
    by_ext = {}
    for f in files:
        by_ext.setdefault(f['ext'], []).append(f)

    # Generate index
    print("[Processing] 生成汇总索引...")
    try:
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write("File\tExtension\tSize(bytes)\tRelativePath\tRows\tCols\n")
            for f in files:
                rows, cols = '', ''
                if f['ext'] in ('.csv', '.tsv', '.txt'):
                    st = extract_csv_stats(f['path'])
                    rows, cols = str(st['rows']), str(st['cols'])
                out.write(f"{f['name']}\t{f['ext']}\t{f['size']}\t{f['relpath']}\t{rows}\t{cols}\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总文件数:     {len(files)}")
    print(f"  文件类型分布:")
    for ext, flist in sorted(by_ext.items()):
        total_size = sum(f['size'] for f in flist)
        print(f"    {ext}: {len(flist)} files ({total_size / 1024 / 1024:.1f} MB)")
    print(f"  索引文件:     {output_file}")
    print("=" * 60)
    print()
    print("[Done] result_file_aggregator completed successfully!")


if __name__ == "__main__":
    main()
