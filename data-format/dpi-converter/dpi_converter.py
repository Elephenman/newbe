#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  dpi-converter
  图片DPI转换工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def convert_dpi(image_file, output="output_image.png", target_dpi=300):
    """转换图片DPI"""
    try:
        from PIL import Image
        img = Image.open(image_file)
        img.save(output, dpi=(target_dpi, target_dpi))
        print(f"图片DPI已转换为: {target_dpi}")
    except ImportError:
        print("Pillow未安装，无法处理图片")
    except Exception as e:
        print(f"处理出错: {e}")

def main():
    print("\n" + "=" * 60)
    print("  图片DPI转换工具")
    print("=" * 60)
    
    image_file = get_input("\n输入图片文件", "figure.png", str)
    output = get_input("输出图片文件", "output_image.png", str)
    target_dpi = get_input("目标DPI", 300, int)
    
    convert_dpi(image_file, output, target_dpi)
    print("\n完成!")

if __name__ == "__main__":
    main()
