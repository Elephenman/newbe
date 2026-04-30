#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  dna-structural-aligner
  DNA结构比对工具 - Needleman-Wunsch global alignment
============================================================
"""


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def needleman_wunsch(seq1, seq2, match_score=1, mismatch_score=-1, gap_score=-2):
    """
    Needleman-Wunsch global alignment algorithm.

    Returns:
        alignment_score: the optimal alignment score
        aligned_seq1: aligned sequence 1 (with gaps)
        aligned_seq2: aligned sequence 2 (with gaps)
    """
    n = len(seq1)
    m = len(seq2)

    # Initialize score matrix
    score = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize traceback matrix
    # 0 = match/mismatch (diagonal), 1 = gap in seq2 (up), 2 = gap in seq1 (left)
    traceback = [[0] * (m + 1) for _ in range(n + 1)]

    # Fill first row and column with gap penalties
    for i in range(1, n + 1):
        score[i][0] = i * gap_score
        traceback[i][0] = 1  # up
    for j in range(1, m + 1):
        score[0][j] = j * gap_score
        traceback[0][j] = 2  # left

    # Fill the score and traceback matrices
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Match or mismatch
            if seq1[i - 1].upper() == seq2[j - 1].upper():
                diag = score[i - 1][j - 1] + match_score
            else:
                diag = score[i - 1][j - 1] + mismatch_score

            up = score[i - 1][j] + gap_score      # gap in seq2
            left = score[i][j - 1] + gap_score     # gap in seq1

            # Take maximum score
            if diag >= up and diag >= left:
                score[i][j] = diag
                traceback[i][j] = 0  # diagonal
            elif up >= left:
                score[i][j] = up
                traceback[i][j] = 1  # up
            else:
                score[i][j] = left
                traceback[i][j] = 2  # left

    alignment_score = score[n][m]

    # Traceback to build aligned sequences
    aligned1 = []
    aligned2 = []
    i, j = n, m

    while i > 0 or j > 0:
        if i > 0 and j > 0 and traceback[i][j] == 0:
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and traceback[i][j] == 1:
            aligned1.append(seq1[i - 1])
            aligned2.append("-")
            i -= 1
        else:
            aligned1.append("-")
            aligned2.append(seq2[j - 1])
            j -= 1

    aligned1.reverse()
    aligned2.reverse()

    return alignment_score, "".join(aligned1), "".join(aligned2)


def read_fasta(filepath):
    """Read a single sequence from a FASTA file."""
    sequence = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                continue
            sequence.append(line)
    return "".join(sequence)


def structural_align(seq1, seq2, output="alignment.txt"):
    """
    Perform Needleman-Wunsch global alignment between two DNA sequences.
    """
    # Run alignment
    score, aligned1, aligned2 = needleman_wunsch(seq1, seq2)

    # Calculate statistics
    alignment_length = len(aligned1)
    matches = sum(1 for a, b in zip(aligned1, aligned2) if a == b and a != "-")
    mismatches = sum(
        1 for a, b in zip(aligned1, aligned2) if a != b and a != "-" and b != "-"
    )
    gaps_in_seq1 = sum(1 for a in aligned1 if a == "-")
    gaps_in_seq2 = sum(1 for b in aligned2 if b == "-")
    total_gaps = gaps_in_seq1 + gaps_in_seq2

    identity = matches / alignment_length * 100 if alignment_length > 0 else 0

    # Build match line
    match_line = []
    for a, b in zip(aligned1, aligned2):
        if a == b and a != "-":
            match_line.append("|")
        elif a == "-" or b == "-":
            match_line.append(" ")
        else:
            match_line.append(".")

    results = {
        "alignment_score": score,
        "alignment_length": alignment_length,
        "matches": matches,
        "mismatches": mismatches,
        "gaps": total_gaps,
        "identity_percent": identity,
        "seq1_length": len(seq1),
        "seq2_length": len(seq2),
        "aligned_seq1": aligned1,
        "aligned_seq2": aligned2,
        "match_line": "".join(match_line),
    }

    # Write output file
    with open(output, "w") as f:
        f.write("DNA Structural Alignment Results\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Sequence 1 length: {len(seq1)}\n")
        f.write(f"Sequence 2 length: {len(seq2)}\n\n")
        f.write(f"Alignment score: {score}\n")
        f.write(f"Alignment length: {alignment_length}\n")
        f.write(f"Matches: {matches}\n")
        f.write(f"Mismatches: {mismatches}\n")
        f.write(f"Gaps: {total_gaps}\n")
        f.write(f"Identity: {identity:.2f}%\n\n")
        f.write("Scoring: match=+1, mismatch=-1, gap=-2\n\n")
        f.write("Alignment:\n")

        # Print alignment in 80-character blocks
        block_size = 60
        for i in range(0, len(aligned1), block_size):
            block_a = aligned1[i : i + block_size]
            block_m = results["match_line"][i : i + block_size]
            block_b = aligned2[i : i + block_size]
            f.write(f"Seq1: {block_a}\n")
            f.write(f"      {block_m}\n")
            f.write(f"Seq2: {block_b}\n\n")

    return results


def main():
    print("\n" + "=" * 60)
    print("  DNA Structural Aligner")
    print("  (Needleman-Wunsch Global Alignment)")
    print("=" * 60)

    mode = get_input("\nInput mode (seq/file)", "seq", str)

    if mode == "file":
        fasta1 = get_input("Sequence 1 FASTA file", "seq1.fasta", str)
        fasta2 = get_input("Sequence 2 FASTA file", "seq2.fasta", str)
        try:
            seq1 = read_fasta(fasta1)
            seq2 = read_fasta(fasta2)
        except Exception as e:
            print(f"\nError reading FASTA files: {e}")
            return
    else:
        seq1 = get_input("Sequence 1", "ATGCGATCGATCGATCG", str)
        seq2 = get_input("Sequence 2", "ATGCGATCGATCGA", str)

    output = get_input("Output file", "alignment.txt", str)

    results = structural_align(seq1, seq2, output)

    print("\nAlignment results:")
    print(f"  Alignment score: {results['alignment_score']}")
    print(f"  Alignment length: {results['alignment_length']}")
    print(f"  Matches: {results['matches']}")
    print(f"  Mismatches: {results['mismatches']}")
    print(f"  Gaps: {results['gaps']}")
    print(f"  Identity: {results['identity_percent']:.2f}%")
    print(f"\n  Scoring: match=+1, mismatch=-1, gap=-2")

    # Show first part of alignment
    print(f"\n  Alignment preview:")
    preview_len = min(60, len(results["aligned_seq1"]))
    print(f"  Seq1: {results['aligned_seq1'][:preview_len]}")
    print(f"        {results['match_line'][:preview_len]}")
    print(f"  Seq2: {results['aligned_seq2'][:preview_len]}")

    print(f"\nFull results saved to: {output}")


if __name__ == "__main__":
    main()
