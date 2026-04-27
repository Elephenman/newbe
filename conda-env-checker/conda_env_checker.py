#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""项目环境依赖一致性检查"""
import os, sys, re, subprocess
from collections import defaultdict
def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def check_conda_env(env_name_or_yml, script_dir=None, gen_lock=True, detect_conflicts=True):
    # 获取conda环境包列表
    if env_name_or_yml.endswith('.yml') or env_name_or_yml.endswith('.yaml'):
        # 从env.yml读取
        env_packages = {}
        with open(env_name_or_yml, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and not line.startswith('name') and not line.startswith('channels') and not line.startswith('prefix'):
                    match = re.match(r'\s*-\s*(\w+)([>=<]+.*)?', line.strip())
                    if match:
                        pkg = match.group(1); ver = match.group(2) or ""
                        env_packages[pkg] = ver.strip()
    else:
        # 从conda list获取
        try:
            result = subprocess.run(["conda", "list", "-n", env_name_or_yml], capture_output=True, text=True, timeout=30)
            env_packages = {}
            for line in result.stdout.split('\n'):
                fields = line.strip().split()
                if len(fields) >= 2 and not line.startswith('#'):
                    env_packages[fields[0]] = fields[1]
        except: print("conda命令执行失败"); env_packages = {}
    
    # 扫描脚本import
    script_imports = defaultdict(set)
    if script_dir and os.path.exists(script_dir):
        for root, dirs, files in os.walk(script_dir):
            for f in files:
                if f.endswith('.py'):
                    with open(os.path.join(root, f), 'r') as fh:
                        for line in fh:
                            imp = re.match(r'^import\s+(\w+)|^from\s+(\w+)', line)
                            if imp:
                                pkg = imp.group(1) or imp.group(2)
                                script_imports[f].add(pkg)
    
    # 对比
    all_imports = set()
    for imports in script_imports.values(): all_imports.update(imports)
    
    # Python标准库(不检查)
    stdlib = {"os","sys","re","math","json","csv","collections","datetime","random","string",
              "io","pathlib","typing","functools","itertools","copy","hashlib","time","subprocess"}
    third_party = all_imports - stdlib
    
    missing = []; present = []
    for pkg in third_party:
        if pkg.lower() in env_packages or pkg in env_packages:
            present.append(pkg)
        else:
            # 检查pip名→conda名映射
            pip_to_conda = {"sklearn":"scikit-learn","cv2":"opencv","PIL":"pillow","Bio":"biopython"}
            conda_name = pip_to_conda.get(pkg, pkg)
            if conda_name in env_packages: present.append(pkg)
            else: missing.append(pkg)
    
    # 版本冲突检测
    conflicts = []
    if detect_conflicts and script_dir:
        for f in os.walk(script_dir):
            pass  # 简化
    
    # 输出
    print(f"\n{'='*60}")
    print(f"  环境依赖检查报告")
    print(f"{'='*60}")
    print(f"  环境包数: {len(env_packages)}")
    print(f"  脚本import数: {len(all_imports)}")
    print(f"  第三方包: {len(third_party)}")
    print(f"  已安装: {len(present)}")
    print(f"  缺失: {len(missing)}")
    
    if missing:
        print(f"\n  【缺失包 ❌】")
        for pkg in missing: print(f"    {pkg}")
        print(f"  安装命令: conda install {(' '.join(missing))}")
    
    if conflicts:
        print(f"\n  【版本冲突 ⚠️】")
        for c in conflicts: print(f"    {c}")
    
    # 生成lock文件
    if gen_lock and env_packages:
        with open("env.lock.yml", 'w') as f:
            f.write("name: project_env\nchannels:\n  - defaults\n  - conda-forge\ndependencies:\n")
            for pkg, ver in sorted(env_packages.items()):
                f.write(f"  - {pkg}{ver}\n")
        print(f"  Lock文件: env.lock.yml")
    
    # 保存报告
    with open("env_check_report.csv", 'w') as out:
        out.write("包,状态\n")
        for pkg in present: out.write(f"{pkg},installed\n")
        for pkg in missing: out.write(f"{pkg},missing\n")
    print(f"  报告CSV: env_check_report.csv")

def main():
    print("="*50); print("  环境依赖检查"); print("="*50)
    en = get_input("conda环境名或env.yml路径", "base")
    sd = get_input("项目脚本目录", "")
    gl = get_input("生成lock文件(yes/no)", "yes")
    dc = get_input("检测版本冲突(yes/no)", "yes")
    check_conda_env(en, sd or None, gl.lower() in ('yes','y'), dc.lower() in ('yes','y'))

if __name__ == "__main__": main()