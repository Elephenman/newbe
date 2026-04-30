#!/usr/bin/env python3
"""CSV/TSV/JSON/Excel format converter"""

import os
import sys
import json
import csv


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def detect_format(filepath):
    """Detect file format from extension."""
    ext = os.path.splitext(filepath)[1].lower()
    format_map = {
        '.csv': 'csv', '.tsv': 'tsv', '.txt': 'tsv',
        '.json': 'json', '.xlsx': 'excel', '.xls': 'excel',
    }
    return format_map.get(ext, None)


def read_data(filepath, input_format=None):
    """Read tabular data from file, return list of dicts."""
    if input_format is None:
        input_format = detect_format(filepath)
    if input_format is None:
        # Try to detect by content
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        if '\t' in first_line:
            input_format = 'tsv'
        elif ',' in first_line:
            input_format = 'csv'
        else:
            input_format = 'csv'

    if input_format == 'json':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Could be column-oriented
            if all(isinstance(v, list) for v in data.values()):
                keys = list(data.keys())
                n = len(data[keys[0]])
                return [{k: data[k][i] for k in keys} for i in range(n)]
            return [data]

    elif input_format == 'excel':
        try:
            import pandas as pd
            df = pd.read_excel(filepath)
            return df.to_dict('records')
        except ImportError:
            print("[ERROR] pandas and openpyxl are required for Excel: pip install pandas openpyxl")
            sys.exit(1)

    else:
        # CSV or TSV
        delimiter = '\t' if input_format == 'tsv' else ','
        rows = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                rows.append(dict(row))
        return rows


def write_data(data, filepath, output_format=None):
    """Write tabular data to file."""
    if output_format is None:
        output_format = detect_format(filepath)
    if output_format is None:
        output_format = 'csv'

    if not data:
        print("[ERROR] No data to write")
        sys.exit(1)

    if output_format == 'json':
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    elif output_format == 'excel':
        try:
            import pandas as pd
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
        except ImportError:
            print("[ERROR] pandas and openpyxl required for Excel output")
            sys.exit(1)

    else:
        delimiter = '\t' if output_format == 'tsv' else ','
        fieldnames = list(data[0].keys())
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)


def main():
    print("=" * 60)
    print("  CSV/TSV/JSON/Excel Format Converter")
    print("=" * 60)
    print()

    input_file = get_input("Input file path", "input.csv")
    output_file = get_input("Output file path", "output.tsv")
    input_format = get_input("Input format (auto/csv/tsv/json/excel)", "auto")
    output_format = get_input("Output format (auto/csv/tsv/json/excel)", "auto")

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    ifmt = None if input_format == "auto" else input_format
    ofmt = None if output_format == "auto" else output_format

    print("[Processing] Reading input file...")
    data = read_data(input_file, ifmt)
    print(f"[Processing] Read {len(data)} records")

    print("[Processing] Writing output file...")
    write_data(data, output_file, ofmt)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Input:  {input_file}")
    print(f"  Output: {output_file}")
    print(f"  Records: {len(data)}")
    print(f"  Columns: {len(data[0].keys()) if data else 0}")
    print("=" * 60)
    print()
    print("[Done] Format conversion completed successfully!")


if __name__ == "__main__":
    main()
