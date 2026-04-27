#!/usr/bin/env python3
"""Core PDF extraction engine using pymupdf (fitz).

Provides text extraction, embedded image extraction, vector region cropping,
structure detection, and batch extraction for academic papers.

Usage:
    python pdf_extract.py --pdf paper.pdf --output-dir ./output --mode full
    python pdf_extract.py --pdf paper.pdf --output-dir ./output --mode text
    python pdf_extract.py --pdf paper.pdf --output-dir ./output --mode images
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


def extract_text(pdf_path, start_page=0, end_page=None):
    """Extract text from a page range of a PDF.

    Args:
        pdf_path: Path to the PDF file.
        start_page: Zero-based index of the first page to extract.
        end_page: Zero-based index of the last page (exclusive). None means all
            remaining pages after start_page.

    Returns:
        Dict mapping page number (int) to extracted text (str).

    Raises:
        FileNotFoundError: If pdf_path does not exist.
        RuntimeError: If the PDF cannot be opened.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    try:
        total = len(doc)
        if end_page is None:
            end_page = total
        end_page = min(end_page, total)
        start_page = max(start_page, 0)

        result = {}
        for page_num in range(start_page, end_page):
            page = doc[page_num]
            text = page.get_text("text")
            result[page_num] = text
        return result
    finally:
        doc.close()


def extract_embedded_images(pdf_path, output_dir):
    """Extract all embedded raster images from a PDF.

    Uses page.get_images() and fitz.Pixmap. Handles CMYK to RGB conversion.
    Saves images as PNG files.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save extracted images into.

    Returns:
        List of dicts with keys: page (int), image_index (int), filename (str).

    Raises:
        FileNotFoundError: If pdf_path does not exist.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    try:
        results = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)

            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]
                try:
                    base_image = doc.extract_image(xref)
                    if base_image is None:
                        continue

                    image_bytes = base_image["image"]
                    image_ext = base_image.get("ext", "png")

                    # Use Pixmap for proper color space handling
                    pix = fitz.Pixmap(doc, xref)

                    # Convert CMYK to RGB if needed
                    if pix.n >= 5:  # CMYK or more channels
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    filename = f"page{page_num}_img{img_index}.png"
                    filepath = os.path.join(output_dir, filename)
                    pix.save(filepath)
                    pix = None  # Free memory

                    results.append({
                        "page": page_num,
                        "image_index": img_index,
                        "filename": filename,
                    })
                except Exception as e:
                    print(
                        f"Warning: Failed to extract image {img_index} on page {page_num}: {e}",
                        file=sys.stderr,
                    )
                    continue
        return results
    finally:
        doc.close()


def extract_vector_region(pdf_path, page_num, bbox, output_path):
    """Crop a rectangular region of a PDF page as a PNG image.

    Useful for capturing vector graphics like figures and charts at their
    original resolution.

    Args:
        pdf_path: Path to the PDF file.
        page_num: Zero-based page number.
        bbox: Tuple (x0, y0, x1, y1) in PDF points defining the crop region.
        output_path: Path to save the output PNG file.

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

        # Use a matrix for high-quality rendering (2x zoom for crisp output)
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat, clip=clip_rect)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        pix.save(output_path)
        return True
    finally:
        doc.close()


# Common academic section heading patterns (case-insensitive)
_SECTION_PATTERNS = [
    re.compile(r"^(?:\d+\.?\s*)?abstract\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?introduction\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?(?:related\s+work|background|literature\s+review)\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?(?:methods?|methodology|materials?\s+and\s+methods?|experimental\s+(?:setup|design|section))\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?(?:results?|results?\s+and\s+discussion|findings?)\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?discussion\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?(?:conclusions?|concluding\s+remarks?|summary)\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?(?:acknowledg(?:ement|ment)s?|funding)\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?(?:references?|bibliography)\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\.?\s*)?(?:appendix|appendices|supplementary)\b", re.IGNORECASE),
]


def detect_structure(pdf_path):
    """Identify section boundaries by scanning for heading patterns.

    Looks for common academic paper section names (Introduction, Methods,
    Results, Discussion, etc.) and returns their page ranges.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Dict mapping section_name (str) to a tuple (start_page, end_page)
        where pages are zero-based. end_page is the page before the next
        section starts.

    Raises:
        FileNotFoundError: If pdf_path does not exist.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    try:
        # Collect section headings with their page numbers
        sections = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            lines = text.split("\n")

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                for pattern in _SECTION_PATTERNS:
                    if pattern.match(stripped):
                        sections.append((stripped, page_num))
                        break

        if not sections:
            return {}

        # Deduplicate: keep first occurrence of a section on a given page
        seen = set()
        unique_sections = []
        for name, page in sections:
            key = (name.lower().strip(), page)
            if key not in seen:
                seen.add(key)
                unique_sections.append((name.strip(), page))

        # Build page range dict
        total_pages = len(doc)
        result = {}
        for i, (name, start) in enumerate(unique_sections):
            if i + 1 < len(unique_sections):
                end = unique_sections[i + 1][1] - 1
            else:
                end = total_pages - 1
            end = max(end, start)  # Ensure end >= start
            result[name] = (start, end)

        return result
    finally:
        doc.close()


def batch_extract(pdf_path, output_dir, batch_size=8):
    """Full extraction pipeline for long academic papers.

    Extracts text in configurable batch sizes, all embedded images, and
    detects document structure.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save all extracted data.
        batch_size: Number of pages per text batch file.

    Returns:
        Summary dict with keys:
            - total_pages (int)
            - text_batches (list of {batch_index, start_page, end_page, filepath})
            - images (list from extract_embedded_images)
            - structure (dict from detect_structure)

    Raises:
        FileNotFoundError: If pdf_path does not exist.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    # Extract text in batches
    text_batches = []
    for batch_start in range(0, total_pages, batch_size):
        batch_end = min(batch_start + batch_size, total_pages)
        batch_text = extract_text(pdf_path, start_page=batch_start, end_page=batch_end)

        batch_filename = f"text_batch_{batch_start}_{batch_end}.txt"
        batch_filepath = os.path.join(output_dir, batch_filename)

        with open(batch_filepath, "w", encoding="utf-8") as f:
            for page_num in range(batch_start, batch_end):
                f.write(f"\n{'=' * 60}\n")
                f.write(f"PAGE {page_num + 1}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(batch_text.get(page_num, ""))

        text_batches.append({
            "batch_index": len(text_batches),
            "start_page": batch_start,
            "end_page": batch_end,
            "filepath": batch_filename,
        })

    # Extract images
    images_dir = os.path.join(output_dir, "images")
    images = extract_embedded_images(pdf_path, images_dir)

    # Detect structure
    structure = detect_structure(pdf_path)

    # Save structure to JSON
    structure_path = os.path.join(output_dir, "structure.json")
    with open(structure_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    summary = {
        "total_pages": total_pages,
        "text_batches": text_batches,
        "images": images,
        "structure": structure,
    }

    # Save summary
    summary_path = os.path.join(output_dir, "extraction_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return summary


def main():
    """CLI interface for PDF extraction.

    Modes:
        text   - Extract text only
        images - Extract embedded images only
        full   - Complete extraction (text batches, images, structure)
    """
    parser = argparse.ArgumentParser(
        description="Core PDF extraction engine for academic papers"
    )
    parser.add_argument(
        "--pdf", required=True, help="Path to the input PDF file"
    )
    parser.add_argument(
        "--output-dir",
        default="./pdf_output",
        help="Directory for extracted output (default: ./pdf_output)",
    )
    parser.add_argument(
        "--mode",
        choices=["text", "images", "full"],
        default="full",
        help="Extraction mode: text, images, or full (default: full)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=8,
        help="Pages per text batch in full mode (default: 8)",
    )

    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf)
    output_dir = os.path.abspath(args.output_dir)

    try:
        if args.mode == "text":
            os.makedirs(output_dir, exist_ok=True)
            result = extract_text(pdf_path)
            # Save to single text file
            text_path = os.path.join(output_dir, "full_text.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                for page_num in sorted(result.keys()):
                    f.write(f"\n{'=' * 60}\n")
                    f.write(f"PAGE {page_num + 1}\n")
                    f.write(f"{'=' * 60}\n\n")
                    f.write(result[page_num])
            output = {
                "mode": "text",
                "total_pages": len(result),
                "output_file": "full_text.txt",
            }

        elif args.mode == "images":
            result = extract_embedded_images(pdf_path, output_dir)
            output = {
                "mode": "images",
                "total_images": len(result),
                "images": result,
            }

        elif args.mode == "full":
            summary = batch_extract(pdf_path, output_dir, args.batch_size)
            output = summary

        print(json.dumps(output, indent=2, ensure_ascii=False))

    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stdout)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stdout)
        sys.exit(1)


if __name__ == "__main__":
    main()
