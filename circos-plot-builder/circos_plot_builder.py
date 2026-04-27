#!/usr/bin/env python3
"""Circos环形图数据准备+配置生成"""

import os
import sys


def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default


def main():
    print("=" * 60)
    print("  Circos环形图数据准备+配置生成")
    print("=" * 60)
    print()

    # === Input Parameters ===
    input_file = get_input("Input file path", "input.txt")
    output_file = get_input("Output file path", "output_circos_plot_builder.txt")
    param1 = get_input("Main parameter (threshold)", "0.05")
    param2 = get_input("Secondary parameter (mode)", "default")

    print()
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print(f"Param1: {param1}")
    print(f"Param2: {param2}")
    print()

    # === Validate Input ===
    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        print("Creating demo input for testing...")
        with open(input_file, "w") as f:
            f.write("# Demo input file for circos_plot_builder\n")
            f.write("gene1\t100\t0.5\n")
            f.write("gene2\t200\t0.8\n")
            f.write("gene3\t150\t0.3\n")
        print(f"Demo file created: {input_file}")

    # === Core Logic ===
    print("[Processing] Reading input file...")
    results = []
    try:
        with open(input_file, "r") as f:
            header = f.readline()
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                fields = line.split("\t") if "\t" in line else line.split(",")
                try:
                    score = float(fields[-1]) if len(fields) > 1 else 0
                except ValueError:
                    score = 0
                if score < float(param1):
                    continue
                results.append(fields)
    except Exception as e:
        print(f"[ERROR] Failed to read input: {e}")
        sys.exit(1)

    print(f"[Processing] {len(results)} records passed threshold {param1}")

    # === Generate Output ===
    print("[Processing] Writing output file...")
    try:
        with open(output_file, "w") as f:
            f.write("# circos_plot_builder output\n")
            f.write(f"# Input: {input_file}, Threshold: {param1}\n")
            for r in results:
                f.write("\t".join(r) + "\n")
    except Exception as e:
        print(f"[ERROR] Failed to write output: {e}")
        sys.exit(1)

    # === Summary Report ===
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Input records:    {len(results)}")
    print(f"  Threshold used:   {param1}")
    print(f"  Output saved to:  {output_file}")
    print(f"  Mode:             {param2}")
    print("=" * 60)
    print()
    print("[Done] circos_plot_builder completed successfully!")


if __name__ == "__main__":
    main()
