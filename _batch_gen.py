#!/usr/bin/env python3
"""批量生成23个工具的骨架文件"""
import os

GI = 'def get_input(p,d=None,t=str):\n    v=input(f"{p} [默认: {d}]: ").strip()\n    if v=="" or v is None: return d\n    try: return t(v)\n    except: return d\n\n'

base = 'A:/claudeworks/newbe-temp'
tools = [
    ('spatial-spot-annotator', 'spatial_spot_annotator.R', 'R', '空间转录组spot自动注释', 'Seurat'),
    ('sc-marker-finder', 'sc_marker_finder.R', 'R', '单细胞marker基因批量查找', 'Seurat'),
    ('snp-stats-reporter', 'snp_stats_reporter.py', 'py', 'SNP/InDel变异统计报告', ''),
    ('motif-scanner', 'motif_scanner.py', 'py', 'DNA序列motif扫描', ''),
    ('genome-density-plotter', 'genome_density_plotter.py', 'py', '染色体密度图', 'matplotlib'),
    ('ld-decay-calculator', 'ld_decay_calculator.py', 'py', 'LD衰减曲线', 'numpy,matplotlib'),
    ('promoter-extractor', 'promoter_extractor.py', 'py', '批量提取启动子序列', ''),
    ('cnv-segment-plotter', 'cnv_segment_plotter.py', 'py', 'CNV分段可视化', 'matplotlib'),
    ('pubmed-batch-searcher', 'pubmed_batch_searcher.py', 'py', 'PubMed批量检索', 'biopython'),
    ('doi-to-citation', 'doi_to_citation.py', 'py', 'DOI转多格式引用', 'requests'),
    ('paper-pdf-meta-extractor', 'paper_pdf_meta_extractor.py', 'py', 'PDF元数据提取', 'pdfplumber'),
    ('keyword-network-builder', 'keyword_network_builder.py', 'py', '关键词共现网络', 'networkx,matplotlib'),
    ('literature-review-matrix', 'literature_review_matrix.py', 'py', '文献综述矩阵', 'pandas'),
    ('citation-tracker', 'citation_tracker.py', 'py', '论文被引追踪', 'requests,matplotlib'),
    ('reference-cleaner', 'reference_cleaner.py', 'py', '引文格式清洗', 'requests'),
    ('obsidian-paper-note-generator', 'obsidian_paper_note_generator.py', 'py', '论文转Obsidian笔记', 'requests,pdfplumber'),
    ('sci-color-palette', 'sci_color_palette.py', 'py', '科研配色生成器', 'matplotlib'),
    ('figure-size-checker', 'figure_size_checker.py', 'py', '图片合规检查', 'Pillow'),
    ('multi-panel-composer', 'multi_panel_composer.py', 'py', '多子图排版', 'matplotlib'),
    ('project-dir-initializer', 'project_dir_initializer.py', 'py', '项目目录初始化', ''),
    ('sample-sheet-validator', 'sample_sheet_validator.py', 'py', '样本表校验', 'pandas'),
    ('conda-env-checker', 'conda_env_checker.py', 'py', '环境依赖检查', ''),
    ('pipeline-log-parser', 'pipeline_log_parser.py', 'py', '流程日志解析', 'matplotlib'),
]

for name, script, lang, desc, deps in tools:
    d = os.path.join(base, name)
    os.makedirs(d, exist_ok=True)
    
    if lang == 'R':
        content = f"""#!/usr/bin/env Rscript
# {desc}
get_input <- function(p, d=NULL) {{
  v <- readline(prompt=paste0(p, " [默认: ", d, "]: "))
  if (v == "" || is.null(v)) return(d)
  return(v)
}}
cat("============================================================\n")
cat("  {desc}\n")
cat("============================================================\n\n")
# TODO: 实现核心功能
cat("✅ 完成\n")
"""
    else:
        content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"{desc}\"\"\"
{GI}
def main():
    print("="*50); print("  {desc}"); print("="*50)
    # TODO: 实现核心功能
    print("✅ 完成")

if __name__ == "__main__":
    main()
"""
    
    with open(os.path.join(d, script), 'w', encoding='utf-8') as f:
        f.write(content)
    
    readme = f"""# {name}
**{desc}**

MIT License
"""
    with open(os.path.join(d, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme)
    
    req = deps + '\n' if deps else '# 无外部依赖\n'
    with open(os.path.join(d, 'requirements.txt'), 'w', encoding='utf-8') as f:
        f.write(req)

print(f'{len(tools)} tool skeletons created')