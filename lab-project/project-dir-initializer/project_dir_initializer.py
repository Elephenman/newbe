#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""科研项目目录一键初始化"""
import os, sys
def get_input(p,d=None,t=str):
    v=input(f"{p} [默认: {d}]: ").strip()
    if v=="" or v is None: return d
    try: return t(v)
    except: return d

TEMPLATES = {
    "RNA-seq": ["raw_data","clean_data","alignment","expression","deg","enrichment","figures","scripts","logs","results"],
    "scRNA-seq": ["raw_data","filtered","seurat","annotation","trajectory","figures","scripts","logs","results"],
    "WGS": ["raw_data","alignment","variant_calling","annotation","population","figures","scripts","logs","results"],
    "ChIP-seq": ["raw_data","alignment","peak_calling","annotation","motif","figures","scripts","logs","results"],
    "general": ["data","scripts","figures","results","docs","logs"],
}

def init_project(name, data_type="RNA-seq", make_readme=True, git_init=True):
    dirs = TEMPLATES.get(data_type, TEMPLATES["general"])
    for d in dirs:
        os.makedirs(os.path.join(name, d), exist_ok=True)
    
    if make_readme:
        readme = f"""# {name}

## 项目类型: {data_type}

## 目录结构
```
{name}/
{chr(10).join([f'  {d}/' for d in dirs])}
```

## 数据处理流程
- 1. 数据质控
- 2. 预处理
- 3. 核心分析
- 4. 结果输出

## 注意事项
- 原始数据不要修改，保留在 raw_data/
- 所有脚本放在 scripts/
- 结果图放在 figures/

Created: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}
"""
        with open(os.path.join(name, "README.md"), 'w', encoding='utf-8') as f: f.write(readme)
    
    if git_init:
        gitignore = """# Gitignore
raw_data/
*.bam
*.fastq
*.fastq.gz
*.RData
*.rds
__pycache__/
*.pyc
.ipynb_checkpoints/
results/*.pdf
"""
        with open(os.path.join(name, ".gitignore"), 'w') as f: f.write(gitignore)
        os.system(f"cd {name} && git init")
    
    print(f"项目目录初始化完成: {name}")
    print(f"   目录数: {len(dirs)}")
    for d in dirs: print(f"   {d}/")

def main():
    print("="*50); print("  🗂️ 项目目录初始化"); print("="*50)
    nm=get_input("项目名称","my_project")
    dt=get_input("数据类型(RNA-seq/scRNA-seq/WGS/ChIP-seq/general)","RNA-seq")
    mr=get_input("生成README(yes/no)","yes")
    gi=get_input("git init(yes/no)","yes")
    init_project(nm, dt, mr.lower() in ('yes','y'), gi.lower() in ('yes','y'))
if __name__=="__main__": main()