#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图片合规检查"""
def get_input(p,d=None,t=str):
    v=input(f"{p} [默认: {d}]: ").strip()
    if v=="" or v is None: return d
    try: return t(v)
    except: return d


def main():
    print("="*50); print("  图片合规检查"); print("="*50)
    # TODO: 实现核心功能
    print("✅ 完成")

if __name__ == "__main__":
    main()
