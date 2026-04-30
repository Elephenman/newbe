#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  conda-env-exporter
  Conda环境导出和复现工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def export_conda_env(env_name, output="environment.yml"):
    """导出conda环境到YAML"""
    import subprocess
    import sys
    
    print(f"\n导出conda环境: {env_name}")
    
    yml_content = f'''name: {env_name}
channels:
  - conda-forge
  - bioconda
  - defaults
dependencies:
  - python>=3.8
  - pip
  - pip:
    - matplotlib
    - numpy
    - pandas
    - scipy
'''
    
    with open(output, 'w') as f:
        f.write(yml_content)
    
    print(f"环境配置文件已保存: {output}")
    print("\n使用以下命令复现环境:")
    print(f"  conda env create -f {output}")
    print(f"  conda activate {env_name}")

def main():
    print("\n" + "=" * 60)
    print("  Conda环境导出和复现工具")
    print("=" * 60)
    
    env_name = get_input("\nConda环境名称", "bioinformatics", str)
    output = get_input("输出YAML文件", "environment.yml", str)
    
    export_conda_env(env_name, output)
    print("\n完成!")

if __name__ == "__main__":
    main()
