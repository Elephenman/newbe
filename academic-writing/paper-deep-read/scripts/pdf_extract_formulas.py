#!/usr/bin-env python3
"""Formula region detection and cropping from PDF documents.

Identifies formula regions by analyzing text patterns (equation numbers,
math symbol density, LaTeX patterns) and crops them as high-DPI PNG images.

Usage:
    python pdf_extract_formulas.py --pdf paper.pdf --output-dir ./formulas
"""

import sys
import os
import json
import argparse
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')


def _ensure_pymupdf():
    """Ensure pymupdf is installed, install if missing."""
    try:
        import fitz
        return fitz
    except ImportError:
        print("pymupdf not found, installing...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', 'pymupdf'],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        import fitz
        return fitz


# Math symbols commonly found in formulas
_MATH_SYMBOLS = set(
    "∫∂∇∑∏√±×÷∈∉⊂⊃⊆⊇∪∩∧∨¬∀∃⟹⟺≤≥≈≠∞∝⊥∠‖⊗⊕⊙"
    "αβγδεζηθικλμνξπρστυφχψω"
    "ΓΔΘΛΞΠΣΦΨΩ"
    "→←↑↓↔⇒⇐⇑⇓⇔"
)

# LaTeX patterns that indicate formula content
_LATEX_PATTERNS = [
    re.compile(r"\\frac\{"),
    re.compile(r"\\sqrt\{"),
    re.compile(r"\\sum_"),
    re.compile(r"\\int_"),
    re.compile(r"\\prod_"),
    re.compile(r"\\lim_"),
    re.compile(r"\\frac\b"),
    re.compile(r"\\mathrm\{"),
    re.compile(r"\\text\{"),
    re.compile(r"\\left[\\(\\[|]"),
    re.compile(r"\\right[\\)\\]|]"),
    re.compile(r"\\[a-zA-Z]+"),  # General LaTeX command
]

# Equation number patterns
_EQ_NUMBER_PATTERNS = [
    re.compile(r"\(\s*(\d+)\s*\)\s*$"),              # (1) at end of line
    re.compile(r"\(\s*Eq\.?\s*(\d+)\s*\)"),           # (Eq. 2)
    re.compile(r"\(\s*Equation\s*(\d+)\s*\)", re.IGNORECASE),  # (Equation 3)
    re.compile(r"Eq\.?\s*\(\s*(\d+)\s*\)"),           # Eq.(4)
    re.compile(r"Equation\s*\(\s*(\d+)\s*\)", re.IGNORECASE),  # Equation(5)
    re.compile(r"\[\s*(\d+)\s*\]\s*$"),               # [1] at end of line (less common)
]


def detect_formula_regions(text_blocks):
    """Identify formula regions from text blocks by pattern analysis.

    Looks for equation numbers, high density of mathematical symbols, and
    LaTeX-like patterns to identify formula regions.

    Args:
        text_blocks: List of dicts, each with keys:
            - text (str): The text content of the block.
            - bbox (tuple): (x0, y0, x1, y1) bounding box in PDF points.
            - page (int): Zero-based page number.

    Returns:
        List of dicts with keys:
            - page (int): Page number.
            - bbox (tuple): (x0, y0, x1, y1) bounding box.
            - equation_number (str or None): Detected equation number string.
            - confidence (str): "high" (equation number found) or "medium"
              (math symbols detected).
    """
    formula_regions = []

    for block in text_blocks:
        text = block.get("text", "").strip()
        if not text:
            continue

        bbox = block.get("bbox")
        page = block.get("page", 0)

        # Skip very short blocks (likely not formulas)
        if len(text) < 3:
            continue

        # Skip blocks that look like regular paragraph text (long sentences)
        words = text.split()
        if len(words) > 40:
            continue

        equation_number = None
        is_formula = False
        confidence = "medium"

        # Check for equation number patterns
        for pattern in _EQ_NUMBER_PATTERNS:
            match = pattern.search(text)
            if match:
                equation_number = match.group(1)
                is_formula = True
                confidence = "high"
                break

        # Check for high density of math symbols
        if not is_formula:
            math_char_count = sum(1 for ch in text if ch in _MATH_SYMBOLS)
            total_chars = len(text.replace(" ", ""))
            if total_chars > 0:
                math_ratio = math_char_count / total_chars
                if math_ratio > 0.1:  # >10% math symbols
                    is_formula = True
                    confidence = "medium"

        # Check for LaTeX patterns
        if not is_formula:
            latex_match_count = 0
            for pattern in _LATEX_PATTERNS:
                if pattern.search(text):
                    latex_match_count += 1
            if latex_match_count >= 1:
                is_formula = True
                confidence = "medium"

        # Check for common formula structural patterns
        if not is_formula:
            # Lines with operators and special characters typical of equations
            formula_indicators = 0
            if re.search(r"[=+−\-]\s*", text):
                formula_indicators += 1
            if re.search(r"[_^{]", text):
                formula_indicators += 1
            if re.search(r"\\[a-zA-Z]", text):
                formula_indicators += 1
            # Short lines centered on page (typical of display equations)
            if len(words) <= 10 and len(words) >= 2:
                formula_indicators += 1

            if formula_indicators >= 3:
                is_formula = True
                confidence = "medium"

        if is_formula:
            formula_regions.append({
                "page": page,
                "bbox": bbox,
                "equation_number": equation_number,
                "confidence": confidence,
            })

    return formula_regions


def crop_formula_to_image(pdf_path, page_num, bbox, output_path):
    """Crop a formula region from a PDF page as a high-DPI PNG image.

    Renders at 300 DPI for crisp formula output.

    Args:
        pdf_path: Path to the PDF file.
        page_num: Zero-based page number.
        bbox: Tuple (x0, y0, x1, y1) defining the formula region.
        output_path: Path to save the cropped PNG.

    Returns:
        True on success.

    Raises:
        FileNotFoundError: If pdf_path does not exist.
        ValueError: If page_num is out of range or bbox is invalid.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    try:
        if page_num < 0 or page_num >= len(doc):
            raise ValueError(
                f"page_num {page_num} out of range [0, {len(doc) - 1}]"
            )

        page = doc[page_num]
        clip_rect = fitz.Rect(bbox)

        if clip_rect.is_empty or clip_rect.is_infinite:
            raise ValueError(f"Invalid bbox: {bbox}")

        # 300 DPI rendering: PDF points are 72 DPI, so 300/72 ~ 4.167x zoom
        zoom = 300 / 72
        mat = fitz.Matrix(zoom, zoom)

        # Add small padding around the formula for better visual context
        padding = 4  # points
        padded_rect = fitz.Rect(
            clip_rect.x0 - padding,
            clip_rect.y0 - padding,
            clip_rect.x1 + padding,
            clip_rect.y1 + padding,
        )

        pix = page.get_pixmap(matrix=mat, clip=padded_rect)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        pix.save(output_path)
        return True

    finally:
        doc.close()


def _get_text_blocks_from_page(page, page_num):
    """Extract text blocks with bounding boxes from a PDF page.

    Args:
        page: A fitz.Page object.
        page_num: Zero-based page number for annotation.

    Returns:
        List of dicts with text, bbox, and page keys.
    """
    blocks_data = page.get_text("dict", flags=11)["blocks"]  # flags=11 preserves whitespace & ligatures
    text_blocks = []

    for block in blocks_data:
        if block["type"] != 0:  # Skip image blocks
            continue

        # Combine all lines in the block into one text string
        block_text = ""
        for line in block["lines"]:
            line_text = ""
            for span in line["spans"]:
                line_text += span["text"]
            block_text += line_text + "\n"

        block_text = block_text.strip()
        if block_text:
            text_blocks.append({
                "text": block_text,
                "bbox": tuple(block["bbox"]),
                "page": page_num,
            })

    return text_blocks


def process_all_formulas(pdf_path, output_dir):
    """Extract text from all pages, detect formulas, and crop each as an image.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save extracted formula images.

    Returns:
        List of dicts with keys:
            - page (int): Page number.
            - bbox (list): Bounding box [x0, y0, x1, y1].
            - image_path (str): Path to the cropped PNG relative to output_dir.
            - equation_number (str or None): Detected equation number.

    Raises:
        FileNotFoundError: If pdf_path does not exist.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    try:
        all_text_blocks = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_blocks = _get_text_blocks_from_page(page, page_num)
            all_text_blocks.extend(page_blocks)
    finally:
        doc.close()

    # Detect formula regions
    formula_regions = detect_formula_regions(all_text_blocks)

    results = []
    formula_counter = 0

    for region in formula_regions:
        formula_counter += 1
        page = region["page"]
        bbox = region["bbox"]
        eq_num = region.get("equation_number")

        # Generate filename
        if eq_num:
            image_filename = f"formula_p{page}_eq{eq_num}.png"
        else:
            image_filename = f"formula_p{page}_{formula_counter}.png"

        image_path = os.path.join(output_dir, image_filename)

        try:
            crop_formula_to_image(pdf_path, page, bbox, image_path)
        except Exception as e:
            print(
                f"Warning: Failed to crop formula {formula_counter} on page {page}: {e}",
                file=sys.stderr,
            )
            continue

        results.append({
            "page": page,
            "bbox": list(bbox),
            "image_path": image_filename,
            "equation_number": eq_num,
        })

    # Save results summary
    summary_path = os.path.join(output_dir, "formulas_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results


def main():
    """CLI interface for formula extraction.

    Detects and crops formula regions from all pages of a PDF.
    """
    parser = argparse.ArgumentParser(
        description="Formula region detection and cropping from PDF documents"
    )
    parser.add_argument(
        "--pdf", required=True, help="Path to the input PDF file"
    )
    parser.add_argument(
        "--output-dir",
        default="./formulas_output",
        help="Directory for extracted formulas (default: ./formulas_output)",
    )

    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf)
    output_dir = os.path.abspath(args.output_dir)

    try:
        results = process_all_formulas(pdf_path, output_dir)
        output = {
            "total_formulas": len(results),
            "formulas": results,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))

    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stdout)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stdout)
        sys.exit(1)


if __name__ == "__main__":
    main()
