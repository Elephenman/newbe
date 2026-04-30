#!/usr/bin/env python3
"""论文图片自动重命名与整理(按Figure编号)"""
import os

def main():
    input_dir = input("图片所在目录 [.]: ") or "."
    output_dir = input("整理输出目录 [organized_figures]: ") or "organized_figures"
    pattern = input("文件匹配模式 [*.png]: ") or "*.png"
    import glob, shutil, re
    os.makedirs(output_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(input_dir, pattern)))
    fig_map = {}
    for fp in files:
        bn = os.path.basename(fp)
        m = re.search(r"[Ff]igur[e]?\s*(\d+)", bn)
        if m:
            fig_num = int(m.group(1))
            fig_map.setdefault(fig_num, []).append(fp)
        else:
            fig_map.setdefault(0, []).append(fp)
    for fig_num, fps in sorted(fig_map.items()):
        for i, fp in enumerate(fps):
            ext = os.path.splitext(fp)[1]
            if fig_num == 0:
                new_name = f"Supplementary_{i+1}{ext}"
            else:
                suffix = chr(97+i) if len(fps) > 1 else ""
                new_name = f"Figure{fig_num}{suffix}{ext}"
            shutil.copy2(fp, os.path.join(output_dir, new_name))
            print(f"  {bn} -> {new_name}")
    print(f"图片整理完成: {len(files)} 个 -> {output_dir}")


if __name__ == "__main__":
    main()
