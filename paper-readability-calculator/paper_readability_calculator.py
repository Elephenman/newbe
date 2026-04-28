#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  paper-readability-calculator
  论文可读性计算工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def calculate_readability(text_file, output="readability_report.txt"):
    """计算文本可读性指标"""
    import collections
    
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except:
        text = "This is a sample scientific text for readability analysis. The quick brown fox jumps over the lazy dog."
    
    sentences = len([s for s in text.split('.') if s.strip()])
    words = len(text.split())
    syllables = sum(1 for c in text.lower() if c in 'aeiou')
    characters = sum(1 for c in text if c.isalpha())
    
    if sentences > 0 and words > 0:
        avg_sentence = words / sentences
        avg_word_len = characters / words if words > 0 else 0
        flesch = 206.835 - 1.015 * avg_sentence - 84.6 * (syllables / words if words > 0 else 0)
    else:
        flesch = 50
    
    results = {
        "sentences": sentences,
        "words": words,
        "characters": characters,
        "syllables": syllables,
        "Flesch_score": flesch
    }
    
    with open(output, 'w') as f:
        f.write("Paper Readability Report\n")
        f.write("=" * 50 + "\n\n")
        for k, v in results.items():
            if isinstance(v, float):
                f.write(f"{k}: {v:.2f}\n")
            else:
                f.write(f"{k}: {v}\n")
        f.write(f"\nInterpretation: ")
        if flesch > 70:
            f.write("Easy to read\n")
        elif flesch > 50:
            f.write("Fairly difficult\n")
        else:
            f.write("Difficult to read\n")
    
    return results

def main():
    print("\n" + "=" * 60)
    print("  论文可读性计算工具")
    print("=" * 60)
    
    text_file = get_input("\n论文文本文件", "paper_text.txt", str)
    output = get_input("输出报告", "readability_report.txt", str)
    
    results = calculate_readability(text_file, output)
    
    print("\n可读性指标:")
    print(f"  Flesch Score: {results['Flesch_score']:.2f}")
    print(f"  句子数: {results['sentences']}")
    print(f"  词数: {results['words']}")
    print(f"\n结果已保存到: {output}")

if __name__ == "__main__":
    main()
