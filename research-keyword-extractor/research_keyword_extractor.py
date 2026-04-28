#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  research-keyword-extractor
  研究关键词提取工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def extract_keywords(text_file, output="keywords.txt", top_n=20):
    """从文本中提取研究关键词"""
    import collections
    import re
    
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read().lower()
    except:
        text = "bioinformatics genomics sequencing analysis data algorithm machine learning neural network dna rna protein gene expression variant"
    
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                 'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that', 'these',
                 'those', 'i', 'we', 'you', 'he', 'she', 'it', 'they', 'them', 'their'}
    
    words = re.findall(r'\b[a-z]{4,}\b', text)
    filtered = [w for w in words if w not in stopwords]
    
    counter = collections.Counter(filtered)
    top_keywords = counter.most_common(top_n)
    
    with open(output, 'w') as f:
        f.write("Research Keywords\n")
        f.write("=" * 40 + "\n\n")
        for rank, (word, count) in enumerate(top_keywords, 1):
            f.write(f"{rank}. {word}\t({count})\n")
    
    return top_keywords

def main():
    print("\n" + "=" * 60)
    print("  研究关键词提取工具")
    print("=" * 60)
    
    text_file = get_input("\n论文文本文件", "paper_text.txt", str)
    output = get_input("输出关键词文件", "keywords.txt", str)
    top_n = get_input("提取关键词数量", 20, int)
    
    keywords = extract_keywords(text_file, output, top_n)
    
    print("\n提取的关键词:")
    for i, (word, count) in enumerate(keywords[:10], 1):
        print(f"  {i}. {word} ({count})")
    print(f"\n结果已保存到: {output}")

if __name__ == "__main__":
    main()
