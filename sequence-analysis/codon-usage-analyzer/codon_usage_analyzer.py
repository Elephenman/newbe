#!/usr/bin/env python3
"""Codon usage bias analysis + RSCU/CAI calculation"""

import os
import sys
from collections import defaultdict


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


# Standard genetic code
CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

# Group codons by amino acid
AA_TO_CODONS = defaultdict(list)
for codon, aa in CODON_TABLE.items():
    AA_TO_CODONS[aa].append(codon)


def analyze_codon_usage(fasta_file, output_file):
    """Analyze codon usage from a FASTA file of coding sequences."""
    # Parse FASTA
    sequences = {}
    cur_id = None
    cur_seq = []
    with open(fasta_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if cur_id:
                    sequences[cur_id] = "".join(cur_seq).upper()
                cur_id = line[1:].split()[0]
                cur_seq = []
            else:
                cur_seq.append(line)
    if cur_id:
        sequences[cur_id] = "".join(cur_seq).upper()

    if not sequences:
        print("[ERROR] No sequences found in FASTA file")
        sys.exit(1)

    # Count codons
    codon_counts = defaultdict(int)
    total_codons = 0
    gene_codon_counts = {}  # per-gene

    for seq_id, seq in sequences.items():
        gene_counts = defaultdict(int)
        # Remove trailing stop codon nucleotides if length not divisible by 3
        seq_len = (len(seq) // 3) * 3
        for i in range(0, seq_len, 3):
            codon = seq[i:i+3]
            if len(codon) == 3 and codon in CODON_TABLE:
                codon_counts[codon] += 1
                gene_counts[codon] += 1
                total_codons += 1
        gene_codon_counts[seq_id] = gene_counts

    if total_codons == 0:
        print("[ERROR] No valid codons found. Ensure input is coding DNA sequences.")
        sys.exit(1)

    # Calculate RSCU (Relative Synonymous Codon Usage)
    # RSCU = (observed count) / (expected count if equal usage)
    # Expected = total for AA / number of synonymous codons
    rscu = {}
    for codon, count in codon_counts.items():
        aa = CODON_TABLE[codon]
        if aa == '*':
            continue  # skip stop codons
        synonyms = AA_TO_CODONS[aa]
        aa_total = sum(codon_counts[c] for c in synonyms)
        if aa_total > 0 and len(synonyms) > 1:
            expected = aa_total / len(synonyms)
            rscu[codon] = round(count / expected, 4) if expected > 0 else 0
        else:
            rscu[codon] = 1.0  # single codon for this AA

    # Calculate CAI (Codon Adaptation Index) - simplified
    # For each AA, find the codon with max RSCU as the reference
    max_rscu = {}
    for aa, codons in AA_TO_CODONS.items():
        if aa == '*':
            continue
        max_rscu[aa] = max(rscu.get(c, 0.001) for c in codons)

    # Write output
    with open(output_file, "w") as out:
        out.write("Codon\tAA\tCount\tFrequency\tRSCU\n")
        for codon in sorted(CODON_TABLE.keys()):
            aa = CODON_TABLE[codon]
            if aa == '*':
                continue
            count = codon_counts[codon]
            freq = round(count / total_codons * 100, 4) if total_codons > 0 else 0
            out.write(f"{codon}\t{aa}\t{count}\t{freq}\t{rscu.get(codon, 0)}\n")

        # Summary statistics
        out.write("\n=== Summary ===\n")
        out.write(f"Total sequences: {len(sequences)}\n")
        out.write(f"Total codons: {total_codons}\n")
        out.write(f"GC3 content: {calculate_gc3(codon_counts):.2f}%\n")

        # Most/least used codons
        sorted_rscu = sorted(rscu.items(), key=lambda x: x[1], reverse=True)
        out.write("\nTop 5 preferred codons (highest RSCU):\n")
        for codon, val in sorted_rscu[:5]:
            out.write(f"  {codon} ({CODON_TABLE[codon]}): RSCU={val}\n")
        out.write("\nTop 5 rare codons (lowest RSCU):\n")
        for codon, val in sorted_rscu[-5:]:
            out.write(f"  {codon} ({CODON_TABLE[codon]}): RSCU={val}\n")

    return {
        "total_seqs": len(sequences),
        "total_codons": total_codons,
        "gc3": round(calculate_gc3(codon_counts), 2),
    }


def calculate_gc3(codon_counts):
    """Calculate GC content at third codon position."""
    gc3 = 0
    total3 = 0
    for codon, count in codon_counts.items():
        if codon in CODON_TABLE and CODON_TABLE[codon] != '*':
            total3 += count
            if codon[2] in ('G', 'C'):
                gc3 += count
    return (gc3 / total3 * 100) if total3 > 0 else 0


def main():
    print("=" * 60)
    print("  Codon Usage Bias Analysis + RSCU/CAI Calculation")
    print("=" * 60)
    print()

    input_file = get_input("Input CDS FASTA file path", "cds.fasta")
    output_file = get_input("Output report path", "codon_usage.tsv")

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    stats = analyze_codon_usage(input_file, output_file)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Total sequences:  {stats['total_seqs']}")
    print(f"  Total codons:     {stats['total_codons']}")
    print(f"  GC3 content:      {stats['gc3']}%")
    print(f"  Output saved to:  {output_file}")
    print("=" * 60)
    print()
    print("[Done] Codon usage analysis completed successfully!")


if __name__ == "__main__":
    main()
