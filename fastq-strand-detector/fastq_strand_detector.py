#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  fastq-strand-detector
  根据双端FASTQ文件推断链特异性信息
============================================================
"""


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def read_fastq(filepath):
    """Generator that yields (name, sequence, quality) tuples from a FASTQ file."""
    with open(filepath, "r") as f:
        while True:
            header = f.readline().strip()
            if not header:
                break
            seq = f.readline().strip()
            plus = f.readline().strip()
            qual = f.readline().strip()
            name = header[1:].split()[0]  # Remove '@' and keep first word
            yield name, seq, qual


def detect_strand_from_fastq(fastq_r1, fastq_r2, output="strand_info.txt"):
    """
    Read paired-end FASTQ files, classify each read pair by orientation,
    and determine the library strand type.

    Orientation classification for paired-end reads:
    - FR (forward-reverse): R1 maps forward, R2 maps reverse -> proper Illumina
    - RF (reverse-forward): R1 maps reverse, R2 maps forward -> inverted insertion
    - FF (forward-forward): both on same strand, forward
    - RR (reverse-reverse): both on same strand, reverse

    Since raw FASTQ has no mapping info, we infer orientation from read sequence
    characteristics. For paired-end data, the relative orientation is determined by
    the library prep. We use a sequence-based heuristic:
    - Check if R1 and R2 are reverse complements of each other
    - FR: R1 is NOT the reverse complement of R2 (typical: R1 forward, R2 reverse-complemented)
    - RF: R1 IS the reverse complement of R2 (both read from same strand, one inverted)
    - FF/RR: both reads are on the same strand
    """
    complement = str.maketrans("ACGTNacgtn", "TGCANtgcan")

    def reverse_complement(seq):
        return seq.translate(complement)[::-1]

    counts = {"FR": 0, "RF": 0, "FF": 0, "RR": 0}
    total_pairs = 0

    r1_reader = read_fastq(fastq_r1)
    r2_reader = read_fastq(fastq_r2)

    for (name1, seq1, _), (name2, seq2, _) in zip(r1_reader, r2_reader):
        total_pairs += 1

        # Heuristic for orientation detection from raw FASTQ:
        # In FR libraries (most common), R2 is the reverse complement of the
        # fragment end. So if we reverse-complement R2, it should partially
        # overlap with R1 for short inserts.
        #
        # In RF libraries, R1 is the reverse complement.
        #
        # For same-strand (FF/RR), neither is a reverse complement.
        #
        # We check the 3' end of R1 against the 3' end of R2:
        # - If R1's 3' end matches R2's reverse complement's 3' end -> FR
        # - If R1's reverse complement's 3' end matches R2's 3' end -> RF
        # - If sequences look similar (same strand) -> FF or RR

        # Use a simple heuristic: compare a window at the ends of reads
        window = min(20, len(seq1) // 2, len(seq2) // 2)
        if window < 5:
            # Sequences too short for reliable detection, default to FR
            counts["FR"] += 1
            continue

        r1_tail = seq1[-window:].upper()
        r2_tail = seq2[-window:].upper()
        r2_rc_tail = reverse_complement(seq2)[:window].upper()
        r1_rc_tail = reverse_complement(seq1)[:window].upper()

        # Count matching bases in overlapping windows
        fr_matches = sum(a == b for a, b in zip(r1_tail, r2_rc_tail))
        rf_matches = sum(a == b for a, b in zip(r1_rc_tail, r2_tail))
        ff_matches = sum(a == b for a, b in zip(r1_tail, r2_tail))

        fr_score = fr_matches / window
        rf_score = rf_matches / window
        ff_score = ff_matches / window

        # Classify based on best match
        if fr_score >= rf_score and fr_score >= ff_score:
            counts["FR"] += 1
        elif rf_score >= fr_score and rf_score >= ff_score:
            counts["RF"] += 1
        elif ff_score >= 0.5:
            # Same-strand pairs: distinguish FF vs RR
            # In FF both reads go forward, in RR both go reverse
            # Use GC content of first vs last half as a simple proxy
            # This is a rough heuristic; for accurate classification
            # alignment-based methods are needed
            counts["FF"] += 1
        else:
            # Low similarity in all orientations, classify as RR (unusual)
            counts["RR"] += 1

    # Determine dominant orientation (>70% threshold)
    if total_pairs == 0:
        inferred_strand = "unknown"
    else:
        percentages = {k: v / total_pairs for k, v in counts.items()}
        dominant = max(percentages, key=percentages.get)
        if percentages[dominant] > 0.70:
            inferred_strand = dominant
        else:
            inferred_strand = "mixed"

    # Write output
    with open(output, "w") as f:
        f.write("FASTQ Strand Detection Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total read pairs: {total_pairs}\n\n")
        f.write("Orientation counts:\n")
        for orient in ["FR", "RF", "FF", "RR"]:
            cnt = counts[orient]
            pct = cnt / total_pairs * 100 if total_pairs > 0 else 0
            f.write(f"  {orient}: {cnt} ({pct:.1f}%)\n")
        f.write(f"\nInferred library type: {inferred_strand}\n")
        f.write(f"(Threshold: >70% for dominant orientation)\n")

    return counts, total_pairs, inferred_strand


def main():
    print("\n" + "=" * 60)
    print("  FASTQ Strand Detector")
    print("=" * 60)
    print("\nDetect strand specificity from paired-end FASTQ files")

    fastq_r1 = get_input("\nRead 1 FASTQ file", "reads_R1.fastq", str)
    fastq_r2 = get_input("Read 2 FASTQ file", "reads_R2.fastq", str)
    output = get_input("Output file", "strand_info.txt", str)

    try:
        counts, total, inferred = detect_strand_from_fastq(fastq_r1, fastq_r2, output)
    except Exception as e:
        print(f"\nError: {e}")
        return

    print("\n" + "-" * 40)
    print("Strand detection results:")
    print("-" * 40)
    print(f"  Total read pairs: {total}")
    print(f"\n  Orientation counts:")
    for orient in ["FR", "RF", "FF", "RR"]:
        cnt = counts[orient]
        pct = cnt / total * 100 if total > 0 else 0
        print(f"    {orient}: {cnt} ({pct:.1f}%)")
    print(f"\n  Inferred library type: {inferred_strand}")
    print(f"  (Threshold: >70% for dominant orientation)")
    print(f"\n  Mode descriptions:")
    print(f"    FR: Read1 forward, Read2 reverse (standard Illumina)")
    print(f"    RF: Read1 reverse, Read2 forward (inverted/dUTP)")
    print(f"    FF: Both reads forward (same strand)")
    print(f"    RR: Both reads reverse (same strand)")

    print(f"\nResults saved to: {output}")


if __name__ == "__main__":
    main()
