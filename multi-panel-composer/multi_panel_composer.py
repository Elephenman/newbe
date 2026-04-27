#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多子图组合排版"""
import os, sys
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def compose_panels(file_list, layout="2x2", unify_font=True, spacing=0.05, output_size="10x8"):
    try:
        from PIL import Image
    except: print("需要Pillow"); return
    
    # 解析布局
    rows, cols = layout.lower().split('x')
    rows = int(rows); cols = int(cols)
    
    # 加载图片
    images = []
    for fp in file_list:
        try:
            img = Image.open(fp)
            images.append(img)
        except: print(f"无法打开: {fp}")
    
    if len(images) == 0: print("无有效图片"); return
    
    # 计算输出尺寸
    ow, oh = output_size.lower().split('x')
    out_w = int(ow) * 100; out_h = int(oh) * 100  # 近似像素
    
    # 单图尺寸
    cell_w = out_w // cols; cell_h = out_h // rows
    
    # 创建组合画布
    canvas = Image.new('RGB', (out_w, out_h), 'white')
    
    for i, img in enumerate(images):
        row = i // cols; col = i % cols
        if row >= rows: break
        
        # 缩放图片到cell尺寸
        img_resized = img.resize((cell_w - int(spacing*cell_w), cell_h - int(spacing*cell_h)), Image.LANCZOS)
        
        x = col * cell_w + int(spacing * cell_w // 2)
        y = row * cell_h + int(spacing * cell_h // 2)
        canvas.paste(img_resized, (x, y))
    
    # 添加标签(A/B/C...)
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(canvas)
    try: font = ImageFont.truetype("arial.ttf", 24)
    except: font = ImageFont.load_default()
    
    labels = [chr(65+i) for i in range(min(len(images), rows*cols))]  # A, B, C...
    for i, label in enumerate(labels):
        row = i // cols; col = i % cols
        x = col * cell_w + 10; y = row * cell_h + 5
        draw.text((x, y), label, fill='black', font=font)
    
    # 保存
    out_path = "composed_panels.png"
    canvas.save(out_path, dpi=(300, 300))
    print(f"组合排版完成")
    print(f"  子图数: {len(images)}")
    print(f"  布局: {layout}")
    print(f"  输出: {out_path}")

def main():
    print("="*50); print("  多子图排版"); print("="*50)
    fl = get_input("子图文件路径(逗号分隔)", "fig1.png,fig2.png,fig3.png,fig4.png")
    la = get_input("布局(如2x2/3x1)", "2x2")
    uf = get_input("统一字体(yes/no)", "yes")
    sp = get_input("间距(0.0-0.2)", 0.05, float)
    sz = get_input("输出尺寸(如10x8)", "10x8")
    files = [f.strip() for f in fl.split(',') if f.strip()]
    compose_panels(files, la, uf.lower() in ('yes','y'), sp, sz)

if __name__ == "__main__": main()