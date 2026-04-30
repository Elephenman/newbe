#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  haplotype-phaser
  单倍型分型工具 - Reads VCF, phases heterozygous variants
  by phase set, and writes phased VCF with HP tags
============================================================
"""


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def phase_haplotypes(vcf_file, output="phased.vcf"):
    """
    Read VCF file, group heterozygous variants by chromosome and phase set (PS tag),
    assign alternating alleles to haplotype 1 and haplotype 2, and write phased VCF
    with HP (haplotype phase) tags.

    Phasing algorithm:
    1. Collect all heterozygous variants (GT = 0/1 or 1/0)
    2. Group by chromosome and PS tag (or by proximity if no PS tag)
    3. Within each phase set, alternate allele assignment:
       - Even-indexed variants: REF -> HP1, ALT -> HP2
       - Odd-indexed variants: ALT -> HP1, REF -> HP2
    4. Write phased GT fields (0|1 or 1|0) and HP tags
    """
    import pysam

    stats = {
        "total_variants": 0,
        "heterozygous": 0,
        "homozygous": 0,
        "phase_sets": 0,
        "phased_variants": 0,
    }

    # Collect variants by chromosome and phase set
    phase_groups = {}  # (chrom, ps) -> list of (record_index, record)

    vcf_in = pysam.VariantFile(vcf_file)

    # Add HP and PS format fields if not present
    header = vcf_in.header
    if "HP" not in header.formats:
        header.formats.add("HP", "A", "Integer", "Haplotype phase (1 or 2)")
    if "PS" not in header.formats and "PS" not in header.formats:
        pass  # PS may already exist

    vcf_out = pysam.VariantFile(output, "w", header=header)

    all_records = []
    rec_idx = 0

    for rec in vcf_in.fetch():
        stats["total_variants"] += 1
        all_records.append(rec)

        # Get genotype for first sample
        samples = list(rec.samples.keys())
        if not samples:
            continue

        sample = rec.samples[samples[0]]
        gt = sample.get("GT", None)

        if gt is None:
            continue

        # Check if heterozygous
        is_het = False
        if len(gt) == 2 and gt[0] is not None and gt[1] is not None:
            if gt[0] != gt[1]:
                is_het = True
                stats["heterozygous"] += 1
            else:
                stats["homozygous"] += 1

        if not is_het:
            continue

        # Get phase set (PS tag) or use chromosome position for grouping
        ps = sample.get("PS", None)
        if ps is None:
            # Group by chromosome; variants within 100kb get same phase set
            # Use position-based binning
            ps = rec.pos // 100000

        key = (rec.contig, ps)
        if key not in phase_groups:
            phase_groups[key] = []
        phase_groups[key].append(rec_idx)

        rec_idx += 1

    stats["phase_sets"] = len(phase_groups)

    # Create a set of records that were phased, with their haplotype assignments
    phased_assignments = {}  # rec_index -> (hap1_allele, hap2_allele)

    for (chrom, ps), indices in phase_groups.items():
        # Sort by position within phase set
        sorted_indices = sorted(indices, key=lambda i: all_records[i].pos)

        for i, rec_idx in enumerate(sorted_indices):
            rec = all_records[rec_idx]
            samples = list(rec.samples.keys())
            sample = rec.samples[samples[0]]
            gt = sample.get("GT", (0, 1))

            # Alternate phasing: even -> 0|1, odd -> 1|0
            if i % 2 == 0:
                phased_assignments[rec_idx] = (0, 1)
            else:
                phased_assignments[rec_idx] = (1, 0)

    # Write output with phasing
    for idx, rec in enumerate(all_records):
        if idx in phased_assignments:
            hap1, hap2 = phased_assignments[idx]
            stats["phased_variants"] += 1

            # Set phased GT (using | instead of /)
            samples = list(rec.samples.keys())
            sample = rec.samples[samples[0]]

            # Determine HP tag value
            # HP=1 means this allele belongs to haplotype 1
            # For 0|1: REF on HP1, ALT on HP2
            # For 1|0: ALT on HP1, REF on HP2
            sample["GT"] = (hap1, hap2)
            sample["HP"] = (1, 2)

        vcf_out.write(rec)

    vcf_in.close()
    vcf_out.close()

    return stats


def main():
    print("\n" + "=" * 60)
    print("  Haplotype Phaser")
    print("=" * 60)

    vcf_file = get_input("\nInput VCF file", "variants.vcf", str)
    output = get_input("Output phased VCF", "phased.vcf", str)

    try:
        stats = phase_haplotypes(vcf_file, output)
    except Exception as e:
        print(f"\nError: {e}")
        return

    print(f"\nPhasing complete!")
    print(f"  Total variants: {stats['total_variants']}")
    print(f"  Heterozygous: {stats['heterozygous']}")
    print(f"  Homozygous: {stats['homozygous']}")
    print(f"  Phase sets: {stats['phase_sets']}")
    print(f"  Phased variants: {stats['phased_variants']}")
    if stats["heterozygous"] > 0:
        print(
            f"  Phasing rate: {stats['phased_variants'] / stats['heterozygous'] * 100:.1f}%"
        )
    print(f"\nResults saved to: {output}")


if __name__ == "__main__":
    main()
