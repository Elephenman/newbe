#!/usr/bin/env python3
"""Conference abstract formatting + word count compliance check"""

import os
import sys
import re


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def format_abstract(input_file, output_file, max_words=300, format_style="structured"):
    """Format conference abstract and check word count compliance.

    Args:
        input_file: Text file containing the abstract
        output_file: Formatted output file
        max_words: Maximum word limit
        format_style: 'structured' (Background/Methods/Results/Conclusion) or 'plain'
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if not content:
        print("[ERROR] Input file is empty")
        sys.exit(1)

    # Word count
    words = content.split()
    word_count = len(words)
    is_compliant = word_count <= max_words

    # Check for common abstract sections
    section_keywords = {
        "Background": ["background", "introduction", "aim", "objective", "purpose"],
        "Methods": ["methods", "methodology", "materials", "approach", "design"],
        "Results": ["results", "findings", "outcome", "observations"],
        "Conclusion": ["conclusion", "conclusions", "summary", "implications", "significance"],
    }

    detected_sections = {}
    lines = content.split('\n')
    current_section = "Header"
    section_lines = {current_section: []}

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_section in section_lines:
                section_lines[current_section].append("")
            continue

        # Check if line is a section header
        found_section = None
        for section, keywords in section_keywords.items():
            if any(stripped.lower().startswith(kw) for kw in keywords):
                if stripped.endswith(':') or stripped.endswith('.') or len(stripped) < 50:
                    found_section = section
                    break

        if found_section:
            current_section = found_section
            detected_sections[current_section] = True
            section_lines[current_section] = []
        else:
            if current_section not in section_lines:
                section_lines[current_section] = []
            section_lines[current_section].append(stripped)

    # Format output
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("=" * 60 + "\n")
        out.write("FORMATTED CONFERENCE ABSTRACT\n")
        out.write("=" * 60 + "\n\n")

        if format_style == "structured":
            for section in ["Background", "Methods", "Results", "Conclusion"]:
                if section in section_lines:
                    out.write(f"**{section}:**\n")
                    text = " ".join(l for l in section_lines[section] if l)
                    out.write(f"{text}\n\n")
            # Any remaining sections
            for section, lines_list in section_lines.items():
                if section not in ["Background", "Methods", "Results", "Conclusion", "Header"]:
                    out.write(f"**{section}:**\n")
                    text = " ".join(l for l in lines_list if l)
                    out.write(f"{text}\n\n")
        else:
            out.write(content + "\n")

        out.write("\n" + "=" * 60 + "\n")
        out.write("COMPLIANCE CHECK\n")
        out.write("=" * 60 + "\n")
        out.write(f"Word count: {word_count}\n")
        out.write(f"Word limit: {max_words}\n")
        if is_compliant:
            out.write(f"Status: COMPLIANT ({max_words - word_count} words remaining)\n")
        else:
            out.write(f"Status: OVER LIMIT by {word_count - max_words} words\n")
        out.write(f"Sections detected: {', '.join(detected_sections.keys()) if detected_sections else 'None (unstructured)'}\n")

        missing = [s for s in ["Background", "Methods", "Results", "Conclusion"]
                   if s not in detected_sections]
        if missing:
            out.write(f"Missing sections: {', '.join(missing)}\n")
        else:
            out.write("All standard sections present: Yes\n")

    return {
        "word_count": word_count,
        "max_words": max_words,
        "is_compliant": is_compliant,
        "sections": list(detected_sections.keys()),
    }


def main():
    print("=" * 60)
    print("  Conference Abstract Formatter + Word Count Check")
    print("=" * 60)
    print()

    input_file = get_input("Input abstract text file", "abstract.txt")
    output_file = get_input("Output formatted file", "abstract_formatted.txt")
    max_words = get_input("Max word limit", "300", int)
    format_style = get_input("Format style (structured/plain)", "structured")

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    stats = format_abstract(input_file, output_file, max_words, format_style)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Word count:      {stats['word_count']}")
    print(f"  Word limit:      {stats['max_words']}")
    print(f"  Compliant:       {'Yes' if stats['is_compliant'] else 'No (over by ' + str(stats['word_count'] - stats['max_words']) + ' words)'}")
    print(f"  Sections found:  {', '.join(stats['sections']) if stats['sections'] else 'None'}")
    print(f"  Output saved to: {output_file}")
    print("=" * 60)
    print()
    print("[Done] Abstract formatting completed successfully!")


if __name__ == "__main__":
    main()
