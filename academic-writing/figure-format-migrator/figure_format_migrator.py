#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  figure-format-migrator
  图片格式批量转换工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def migrate_format(input_file, output_file, target_format):
    """图片格式转换"""
    try:
        from PIL import Image
        img = Image.open(input_file)
        img.save(output_file, format=target_format.upper())
        print(f"已转换为 {target_format.upper()} 格式")
    except ImportError:
        print("Pillow未安装")
    except Exception as e:
        print(f"转换出错: {e}")

def main():
    print("\n" + "=" * 60)
    print("  图片格式批量转换工具")
    print("=" * 60)
    
    input_file = get_input("\n输入图片文件", "figure.tiff", str)
    output_file = get_input("输出图片文件", "figure.png", str)
    target_format = get_input("目标格式(png/tiff/jpg)", "png", str)
    
    migrate_format(input_file, output_file, target_format)
    print("\n完成!")

if __name__ == "__main__":
    main()
