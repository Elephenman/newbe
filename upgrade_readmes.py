#!/usr/bin/env python3
"""
批量升级 newbe 子工具 README
自动读取脚本提取参数，生成详细 README
"""
import os, re, glob, json

BASE = r"A:\claudeworks\newbe-temp"

# 工具分类映射（编号 -> 目录名）
TOOL_CATEGORIES = {
    "测序数据处理": list(range(1,11)),
    "测序数据处理扩展": list(range(51,61)),
    "测序数据处理进阶": list(range(111,121)),
    "转录组/表达分析": list(range(11,21)),
    "转录组/表达分析扩展": list(range(61,71)),
    "转录组/表达分析进阶": list(range(121,131)),
    "单细胞/空间组学": list(range(21,29)),
    "单细胞/空间组学扩展": list(range(71,81)),
    "单细胞/空间组学进阶": list(range(131,141)),
    "基因组/变异/调控": list(range(29,36)),
    "基因组/变异/调控扩展": list(range(81,91)),
    "基因组/变异/调控进阶": list(range(141,151)),
    "文献/学术工具": list(range(36,44)),
    "文献/学术工具扩展": list(range(91,101)),
    "绘图/数据/流程工具": list(range(44,51)),
    "绘图/数据/流程工具扩展": list(range(101,111)),
    "文献/学术/绘图/流程进阶": list(range(151,161)),
}

# 读取主 README 获取工具名映射
def get_tool_dirs():
    """从目录结构获取所有工具目录"""
    dirs = []
    for d in sorted(os.listdir(BASE)):
        full = os.path.join(BASE, d)
        if os.path.isdir(full) and d not in ('.git',):
            dirs.append(d)
    return dirs

def find_main_script(tool_dir):
    """找到工具的主脚本"""
    for ext in ['.py', '.R']:
        files = glob.glob(os.path.join(tool_dir, f'*{ext}'))
        # 排除 __init__.py, setup.py 等
        files = [f for f in files if not os.path.basename(f).startswith('__') and not os.path.basename(f).startswith('setup')]
        if files:
            return files[0]
    return None

def extract_py_params(filepath):
    """从Python脚本提取get_input参数"""
    params = []
    desc = ""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # 提取docstring
        doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if doc_match:
            desc = doc_match.group(1).strip()
        # 提取 get_input 调用
        # 模式1: get_input("提示文字", default="xxx")  或  get_input("提示文字", "xxx")
        # 模式2: get_input("提示文字", default=20, int)
        pattern = r'get_input\s*\(\s*["\']([^"\']+)["\']\s*,\s*(?:default\s*=\s*)?["\']?([^,"\')\]]*)["\']?'
        for m in re.finditer(pattern, content):
            prompt = m.group(1)
            default = m.group(2).strip().rstrip(',')
            if default.startswith('default='):
                default = default[8:]
            params.append((prompt, default))
    except:
        pass
    return desc, params

def extract_r_params(filepath):
    """从R脚本提取get_input参数"""
    params = []
    desc = ""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # 提取注释中的功能描述（跳过shebang行、coding行、分隔线）
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('#') and not line.startswith('#!') and not line.startswith('# -*-') and not re.match(r'^#\s*=+', line) and not re.match(r'^#\s*-+', line):
                desc = line.lstrip('#').strip()
                if len(desc) > 3:  # 忽略过短的注释
                    break
        # 提取 get_input 调用
        # R模式: get_input("提示文字", default = "值") 或 get_input("提示文字", "值", type = "numeric")
        # 先提取完整括号内容
        pattern = r'get_input\s*\(\s*["\']([^"\']+)["\']\s*,\s*default\s*=\s*["\']?([^,"\')\]]*?)["\']?\s*[,)]'
        for m in re.finditer(pattern, content):
            prompt = m.group(1)
            default = m.group(2).strip().rstrip(',')
            # 清理 type = 残留
            default = re.sub(r',?\s*type\s*=.*', '', default).strip()
            params.append((prompt, default))
        # 如果上面的模式没匹配，尝试更宽松的匹配
        if not params:
            pattern2 = r'get_input\s*\(\s*["\']([^"\']+)["\']\s*,\s*(?:default\s*=\s*)?["\']([^"\']+)["\']'
            for m in re.finditer(pattern2, content):
                prompt = m.group(1)
                default = m.group(2).strip()
                params.append((prompt, default))
    except:
        pass
    return desc, params

def detect_lang(filepath):
    if filepath.endswith('.R'):
        return 'R'
    return 'Python'

def get_run_cmd(filepath):
    fname = os.path.basename(filepath)
    if filepath.endswith('.R'):
        return f"Rscript {fname}"
    return f"python {fname}"

def get_deps(filepath, lang):
    """从脚本提取依赖"""
    deps = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if lang == 'Python':
            stdlib = {'os', 'sys', 're', 'json', 'csv', 'glob', 'collections', 'math', 'datetime', 'time', 'argparse', 'pathlib', 'itertools', 'functools', 'defaultdict', 'struct', 'gzip', 'zipfile', 'io', 'textwrap', 'typing', 'hashlib', 'shutil', 'subprocess', 'string', 'random', 'statistics', 'copy', 'operator'}
            for m in re.finditer(r'^import\s+(\w+)|^from\s+(\w+)', content, re.MULTILINE):
                dep = m.group(1) or m.group(2)
                if dep and dep not in stdlib and dep[0].islower():
                    deps.add(dep)
        else:  # R
            for m in re.finditer(r'library\((\w+)\)|require\((\w+)\)', content):
                dep = m.group(1) or m.group(2)
                if dep:
                    deps.add(dep)
    except:
        pass
    return sorted(deps)

def get_emoji(tool_dir_name, desc):
    """根据工具名和描述分配emoji"""
    name_and_desc = (tool_dir_name + ' ' + desc).lower()
    if any(k in name_and_desc for k in ['fastq','bam','sam','vcf','gtf','bed','fasta','sequenc','genome']):
        return "🧬"
    if any(k in name_and_desc for k in ['express','deseq','deg','tpm','fpkm','heatmap','volcano','pca','wgcna','enrich','gsea','count','boxplot','splicing','correlation']):
        return "📊"
    if any(k in name_and_desc for k in ['seurat','cell','spatial','single','doublet','pseudotime','cellchat','umap','trajectory','proportion','cluster','module','neighborhood','vega','velocity','cycle','mitochondria','niche','moran','subset','abundance','trend','deconvolution']):
        return "🔬"
    if any(k in name_and_desc for k in ['snp','motif','cnv','ld','variant','mutation','promoter','hi-c','atac','chip','methy','chromatin','repeat','codon','protein','ortholog','damage','germline','signature','enhancer','replication','tf-bind']):
        return "🧪"
    if any(k in name_and_desc for k in ['pubmed','doi','paper','keyword','literature','citation','reference','manuscript','thesis','grant','lab','conference','research','supplementary','figure-caption','word-count','reagent','timer','abstract','diary','minute','outline','organizer']):
        return "📖"
    if any(k in name_and_desc for k in ['color','palette','figure','plot','panel','circos','sankey','gantt','ridgeline','scatter','visual','heatmap-annotation','volcano-label','colorblind','boxplot-outlier','benchmark']):
        return "🎨"
    if any(k in name_and_desc for k in ['markdown','notebook','slide','convert','aggregat','data-type','pipeline-doc','coordinate','multi-omics','integration']):
        return "📝"
    if any(k in name_and_desc for k in ['project','sample','conda','log','init','validator','checker']):
        return "🛠️"
    return "🔧"

def extract_title_from_script(filepath, lang, desc):
    """从脚本提取更友好的标题"""
    title_line = desc
    # 移除shebang残留
    title_line = re.sub(r'^!/', '', title_line).strip()
    title_line = re.sub(r'^/usr/bin.*', '', title_line).strip()
    title_line = re.sub(r'^#.*coding.*', '', title_line).strip()
    
    # 如果描述为空或无意义，从脚本中的打印标题提取
    if not title_line or title_line.startswith('#'):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if lang == 'Python':
                # 找第二个print（第一个通常是===分隔线）
                prints = re.findall(r'print\s*\(\s*["\']([^"\']+)["\']', content)
                for p in prints:
                    p = p.strip()
                    if len(p) > 5 and not p.startswith('=') and not p.startswith('-'):
                        title_line = p
                        break
            else:  # R
                cats = re.findall(r'cat\s*\(\s*["\']\s*([^"=\'\n]{5,}?)["\']', content)
                for c in cats:
                    c = c.strip()
                    if len(c) > 5 and not c.startswith('=') and not c.startswith('-') and not c.startswith('*'):
                        title_line = c
                        break
        except:
            pass
    
    # 最终fallback
    if not title_line:
        title_line = tool_dir_name.replace('-', ' ').title()
    
    return title_line

def generate_readme(tool_dir_name, filepath, lang, desc, params, deps):
    """生成 README 内容"""
    fname = os.path.basename(filepath)
    run_cmd = get_run_cmd(filepath)
    
    title_line = extract_title_from_script(filepath, lang, desc)
    emoji = get_emoji(tool_dir_name, desc + ' ' + title_line)
    
    lines = []
    lines.append(f"# {emoji} {tool_dir_name}")
    lines.append("")
    lines.append(f"**{title_line}**")
    lines.append("")
    
    # 使用方法
    lines.append("## 使用方法")
    lines.append("")
    lines.append("```bash")
    lines.append(f"cd {tool_dir_name}")
    lines.append(f"{run_cmd}")
    lines.append("```")
    lines.append("")
    lines.append("运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。")
    lines.append("")
    
    # 交互式参数
    if params:
        lines.append("### 参数说明")
        lines.append("")
        lines.append("| # | 参数 | 默认值 |")
        lines.append("|---|------|--------|")
        for i, (prompt, default) in enumerate(params, 1):
            lines.append(f"| {i} | `{prompt}` | `{default}` |")
        lines.append("")
    
    # 交互示例
    if params:
        lines.append("### 交互式输入示例")
        lines.append("")
        lines.append("```")
        for prompt, default in params:
            lines.append(f"{prompt} [默认: {default}]: ")
        lines.append("```")
        lines.append("")
    
    # 依赖
    lines.append("## 依赖")
    lines.append("")
    if deps:
        if lang == 'Python':
            lines.append("```bash")
            lines.append(f"pip install {' '.join(deps)}")
            lines.append("```")
        else:
            lines.append("```r")
            for d in deps:
                lines.append(f"install.packages('{d}')  # 或 BiocManager::install('{d}')")
            lines.append("```")
    else:
        if lang == 'Python':
            lines.append("无外部依赖，纯Python标准库")
        else:
            lines.append("请参考脚本中的 library() 调用")
    lines.append("")
    
    # 输出
    lines.append("## 输出")
    lines.append("")
    lines.append("脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。")
    lines.append("")
    
    # License
    lines.append("## License")
    lines.append("")
    lines.append("MIT")
    
    return '\n'.join(lines)

def main():
    tool_dirs = get_tool_dirs()
    # 排除5个原始子项目（它们有自己的README结构）
    original_projects = ['phylo-tools', 'r-plot-templates', 'paper-deep-read', 
                         'academic-group-meeting-pipeline', 'md2ipynb-sync']
    
    count = 0
    for d in tool_dirs:
        if d in original_projects:
            continue
        full_dir = os.path.join(BASE, d)
        filepath = find_main_script(full_dir)
        if not filepath:
            continue
        
        lang = detect_lang(filepath)
        if lang == 'Python':
            desc, params = extract_py_params(filepath)
        else:
            desc, params = extract_r_params(filepath)
        
        deps = get_deps(filepath, lang)
        readme_content = generate_readme(d, filepath, lang, desc, params, deps)
        
        readme_path = os.path.join(full_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        count += 1
        print(f"  OK {d} ({lang}, {len(params)} params)")
    
    print(f"\nDone! {count} README files updated")

if __name__ == "__main__":
    main()
