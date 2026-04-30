#!/usr/bin/env python3
"""Specialized table extraction from PDF documents.

Detects table regions by both caption-driven search and alignment-based
analysis, crops them as images, and attempts structured text extraction
from table cells.

Usage:
    python pdf_extract_tables.py --pdf paper.pdf --output-dir ./tables
"""

import sys
import os
import json
import argparse
import subprocess
import re

sys.stdout.reconfigure(encoding='utf-8')


# ---------------------------------------------------------------------------
# Shared caption regex patterns — reusable across caption detection functions
# ---------------------------------------------------------------------------
_TABLE_CAPTION_PATTERNS = [
    # "Table 1", "Table 12" — English, numeric
    re.compile(r'\bTable\s+(\d+)\b', re.IGNORECASE),
    # "Table S1", "Table S12" — Supplementary, letter + numeric
    re.compile(r'\bTable\s+S(\d+)\b', re.IGNORECASE),
    # "Table S1.1" — Supplementary with sub-number
    re.compile(r'\bTable\s+S(\d+)[.:](\d+)\b', re.IGNORECASE),
    # "表 1", "表1" — Chinese
    re.compile(r'表\s*(\d+)', re.UNICODE),
    # "附表 1", "附表1" — Chinese supplementary
    re.compile(r'附表\s*(\d+)', re.UNICODE),
]


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


def detect_tables_by_caption(pdf_path):
    """Detect tables by scanning all pages for caption patterns.

    Searches page text for patterns like "Table 1", "Table S1", "表 1",
    then retrieves the bounding box of the caption text span.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        List of dicts with keys:
            - table_number (str): The number part of the caption (e.g. "1", "S1").
            - page_num (int): Zero-based page number where the caption was found.
            - caption_text (str): The full caption text span.
            - caption_bbox (list): [x0, y0, x1, y1] of the caption span.
            - is_supplementary (bool): True if the caption indicates a
              supplementary table (e.g. "Table S1").

    Raises:
        FileNotFoundError: If pdf_path does not exist.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    try:
        results = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text(
                "dict", flags=fitz.TEXT_PRESERVE_WHITESPACE
            )["blocks"]

            for block in blocks:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue

                        # Check each caption pattern
                        for pattern in _TABLE_CAPTION_PATTERNS:
                            match = pattern.search(text)
                            if match is None:
                                continue

                            # Determine table number and supplementary flag
                            is_supplementary = False
                            table_number = ""

                            matched_text = match.group(0)

                            if '附表' in matched_text:
                                # Chinese supplementary
                                table_number = match.group(1)
                                is_supplementary = True
                            elif '表' in matched_text:
                                # Chinese standard
                                table_number = match.group(1)
                            elif 'S' in matched_text.upper():
                                # Supplementary English patterns (Table S1, Table S1.1)
                                groups = match.groups()
                                if len(groups) >= 2 and groups[1]:
                                    # "Table S1.1" style — combine groups
                                    table_number = f"S{groups[0]}.{groups[1]}"
                                else:
                                    table_number = f"S{match.group(1)}"
                                is_supplementary = True
                            else:
                                # Standard English "Table N"
                                table_number = match.group(1)

                            results.append({
                                "table_number": table_number,
                                "page_num": page_num,
                                "caption_text": text,
                                "caption_bbox": list(span["bbox"]),
                                "is_supplementary": is_supplementary,
                            })
                            # Only match the first pattern that hits
                            break

        return results

    finally:
        doc.close()


def _extract_description_from_caption(caption_text):
    """Extract a short filesystem-safe description from a table caption.

    Takes the first meaningful words after the table number, sanitizes them
    for use in filenames, and truncates to a reasonable length.

    Args:
        caption_text: The full caption text string.

    Returns:
        A sanitized description string (lowercase, hyphen-separated).
    """
    # Remove the table number prefix (e.g. "Table 1", "Table S1", "表 1")
    cleaned = caption_text
    for pattern in _TABLE_CAPTION_PATTERNS:
        cleaned = pattern.sub('', cleaned)
    cleaned = cleaned.strip()

    # Remove leading punctuation like ".", ":", "—", "-"
    cleaned = re.sub(r'^[.:;\-\—–,\s]+', '', cleaned)

    if not cleaned:
        return "untitled"

    # Take first meaningful words (up to ~5 words)
    words = cleaned.split()
    desc_words = words[:5]

    # Sanitize for filesystem: lowercase, replace non-alphanumeric with hyphen
    desc = '-'.join(desc_words).lower()
    desc = re.sub(r'[^\w\-]', '-', desc)
    desc = re.sub(r'-+', '-', desc)
    desc = desc.strip('-')

    if not desc:
        return "untitled"

    return desc


def _bbox_overlap_ratio(bbox_a, bbox_b):
    """Compute the overlap ratio between two bounding boxes.

    Returns the ratio of the intersection area to the smaller box area.
    A ratio >= 0.3 is generally considered "overlapping enough" for
    deduplication purposes.

    Args:
        bbox_a: (x0, y0, x1, y1) or [x0, y0, x1, y1].
        bbox_b: (x0, y0, x1, y1) or [x0, y0, x1, y1].

    Returns:
        Float overlap ratio (0.0 if no overlap).
    """
    a = list(bbox_a)
    b = list(bbox_b)

    ix0 = max(a[0], b[0])
    iy0 = max(a[1], b[1])
    ix1 = min(a[2], b[2])
    iy1 = min(a[3], b[3])

    if ix1 <= ix0 or iy1 <= iy0:
        return 0.0

    intersection = (ix1 - ix0) * (iy1 - iy0)
    area_a = max((a[2] - a[0]) * (a[3] - a[1]), 1)
    area_b = max((b[2] - b[0]) * (b[3] - b[1]), 1)
    smaller_area = min(area_a, area_b)

    return intersection / smaller_area


def crop_table_by_caption(
    pdf_path, page_num, caption_bbox, table_number, caption_text, output_dir
):
    """Crop a table region identified by its caption.

    Estimates the table region as being above or containing the caption.
    Uses alignment-based detection as a confirmatory check: if a matching
    alignment-detected table exists on the same page near the caption,
    that bbox is preferred over the estimated region.

    Args:
        pdf_path: Path to the PDF file.
        page_num: Zero-based page number.
        caption_bbox: [x0, y0, x1, y1] of the caption text span.
        table_number: The table number string (e.g. "1", "S1").
        caption_text: The full caption text.
        output_dir: Directory to save the cropped image.

    Returns:
        Dict with keys:
            - page (int): Page number.
            - bbox (list): Final bounding box used [x0, y0, x1, y1].
            - image_path (str): Filename of the cropped PNG.
            - text_or_none (list or null): Extracted table text, or None.

    Raises:
        FileNotFoundError: If pdf_path does not exist.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # --- Step 1: Try alignment-based detection on the same page ---
    try:
        alignment_bboxes = detect_table_regions(pdf_path, page_num)
    except Exception as e:
        print(
            f"Warning: alignment detection failed on page {page_num}: {e}",
            file=sys.stderr,
        )
        alignment_bboxes = []

    # Find the alignment bbox that is near the caption (overlapping or
    # directly above it within a reasonable vertical gap).
    best_alignment_bbox = None
    caption_y0 = caption_bbox[1]
    caption_y1 = caption_bbox[3]
    caption_cy = (caption_y0 + caption_y1) / 2
    # A table is "near" its caption if it overlaps or is within 50 points
    # vertically above the caption.
    proximity_threshold = 50

    for abbox in alignment_bboxes:
        abbox_y0 = abbox[1]
        abbox_y1 = abbox[3]

        # Check if the alignment bbox is on the same page region as caption
        # The table should be above or overlapping the caption
        vertical_gap = caption_y0 - abbox_y1  # gap between table bottom and caption top
        overlaps = _bbox_overlap_ratio(abbox, caption_bbox) > 0

        if overlaps or (vertical_gap >= -10 and vertical_gap <= proximity_threshold):
            # Also check horizontal alignment — table and caption should
            # share some horizontal range
            horizontal_overlap = min(abbox[2], caption_bbox[2]) - max(abbox[0], caption_bbox[0])
            if horizontal_overlap > 0:
                best_alignment_bbox = abbox
                break

    # --- Step 2: Determine final bbox ---
    if best_alignment_bbox is not None:
        # Use the alignment-detected bbox, but extend it to include the caption
        final_bbox = [
            min(best_alignment_bbox[0], caption_bbox[0]),
            min(best_alignment_bbox[1], caption_bbox[1]),
            max(best_alignment_bbox[2], caption_bbox[2]),
            max(best_alignment_bbox[3], caption_bbox[3]),
        ]
    else:
        # Estimate the table region above the caption
        doc = fitz.open(pdf_path)
        try:
            page = doc[page_num]
            page_height = page.rect.height
            page_width = page.rect.width
        finally:
            doc.close()

        # Estimate: table content is above the caption, typically occupying
        # the region from some point above to the caption position.
        # Heuristic: table height is roughly 3x the caption height, and
        # extends to the page margins horizontally.
        caption_height = caption_bbox[3] - caption_bbox[1]
        estimated_table_height = max(caption_height * 8, 100)
        margin = 30  # left/right margin from page edge

        final_bbox = [
            margin,
            max(0, caption_bbox[1] - estimated_table_height),
            page_width - margin,
            caption_bbox[3],
        ]

    # --- Step 3: Crop the table image ---
    description = _extract_description_from_caption(caption_text)
    image_filename = f"table{table_number}-{description}.png"
    image_path = os.path.join(output_dir, image_filename)

    try:
        crop_table_to_image(pdf_path, page_num, tuple(final_bbox), image_path)
    except Exception as e:
        print(
            f"Warning: Failed to crop caption-detected table {table_number} "
            f"on page {page_num}: {e}",
            file=sys.stderr,
        )
        return {
            "page": page_num,
            "bbox": list(final_bbox),
            "image_path": None,
            "text_or_none": None,
        }

    # --- Step 4: Attempt text extraction ---
    text_result = None
    try:
        text_result = extract_table_text(pdf_path, page_num, tuple(final_bbox))
    except Exception as e:
        print(
            f"Warning: Failed to extract text from caption-detected table "
            f"{table_number} on page {page_num}: {e}",
            file=sys.stderr,
        )

    return {
        "page": page_num,
        "bbox": list(final_bbox),
        "image_path": image_filename,
        "text_or_none": text_result,
    }


def detect_table_regions(pdf_path, page_num):
    """Detect table bounding boxes by analyzing text block alignment patterns.

    Scans text blocks on the page and identifies clusters that form columnar
    and row-aligned structures, which are characteristic of tables.

    Args:
        pdf_path: Path to the PDF file.
        page_num: Zero-based page number to analyze.

    Returns:
        List of bbox tuples (x0, y0, x1, y1) for detected table regions.

    Raises:
        FileNotFoundError: If pdf_path does not exist.
        ValueError: If page_num is out of range.
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
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

        # Collect all text spans with their positions
        spans = []
        for block in blocks:
            if block["type"] != 0:  # Skip image blocks
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip():
                        bbox = span["bbox"]
                        spans.append({
                            "text": span["text"].strip(),
                            "x0": bbox[0],
                            "y0": bbox[1],
                            "x1": bbox[2],
                            "y1": bbox[3],
                            "cx": (bbox[0] + bbox[2]) / 2,  # center x
                            "cy": (bbox[1] + bbox[3]) / 2,  # center y
                            "height": bbox[3] - bbox[1],
                        })

        if len(spans) < 4:
            return []

        # Group spans into rows by y-coordinate proximity
        row_tolerance = 3  # pixels
        sorted_by_y = sorted(spans, key=lambda s: s["cy"])
        rows = []
        current_row = [sorted_by_y[0]]

        for span in sorted_by_y[1:]:
            if abs(span["cy"] - current_row[0]["cy"]) < row_tolerance:
                current_row.append(span)
            else:
                rows.append(current_row)
                current_row = [span]
        rows.append(current_row)

        # A table needs at least 2 rows with multiple columns
        # Filter rows with 2+ items and look for column alignment
        multi_col_rows = [r for r in rows if len(r) >= 2]

        if len(multi_col_rows) < 2:
            return []

        # Detect column positions: find x-coordinates where many spans align
        all_cx = []
        for row in multi_col_rows:
            for span in row:
                all_cx.append(span["cx"])

        # Cluster x-centers to find column positions
        col_tolerance = 15  # pixels
        all_cx_sorted = sorted(all_cx)
        col_clusters = []
        current_cluster = [all_cx_sorted[0]]

        for cx in all_cx_sorted[1:]:
            if cx - current_cluster[-1] < col_tolerance:
                current_cluster.append(cx)
            else:
                col_clusters.append(current_cluster)
                current_cluster = [cx]
        col_clusters.append(current_cluster)

        # A table should have at least 2 distinct column positions
        col_positions = [sum(c) / len(c) for c in col_clusters if len(c) >= 2]

        if len(col_positions) < 2:
            return []

        # Now identify contiguous groups of multi-column rows as tables
        # Group multi_col_rows by y-proximity (allowing small gaps)
        row_y_positions = []
        for row in multi_col_rows:
            avg_y = sum(s["cy"] for s in row) / len(row)
            row_y_positions.append(avg_y)

        # Cluster rows into table regions
        table_regions = []
        current_table_rows = [0]

        for i in range(1, len(row_y_positions)):
            gap = row_y_positions[i] - row_y_positions[i - 1]
            avg_row_height = sum(s["height"] for s in multi_col_rows[i - 1]) / len(
                multi_col_rows[i - 1]
            )
            # Allow gap up to 2x row height (for table headers, etc.)
            if gap < max(avg_row_height * 2.5, 30):
                current_table_rows.append(i)
            else:
                if len(current_table_rows) >= 2:
                    table_regions.append(current_table_rows[:])
                current_table_rows = [i]

        if len(current_table_rows) >= 2:
            table_regions.append(current_table_rows[:])

        # Convert row groups to bounding boxes
        bboxes = []
        for row_indices in table_regions:
            region_spans = []
            for idx in row_indices:
                region_spans.extend(multi_col_rows[idx])

            if not region_spans:
                continue

            x0 = min(s["x0"] for s in region_spans) - 5
            y0 = min(s["y0"] for s in region_spans) - 5
            x1 = max(s["x1"] for s in region_spans) + 5
            y1 = max(s["y1"] for s in region_spans) + 5

            # Minimum size check: table should be at least 100x50 points
            if (x1 - x0) > 100 and (y1 - y0) > 50:
                bboxes.append((x0, y0, x1, y1))

        # Merge overlapping bboxes
        merged = _merge_overlapping_bboxes(bboxes)
        return merged

    finally:
        doc.close()


def _merge_overlapping_bboxes(bboxes):
    """Merge overlapping or adjacent bounding boxes.

    Args:
        bboxes: List of (x0, y0, x1, y1) tuples.

    Returns:
        List of merged bbox tuples.
    """
    if not bboxes:
        return []

    # Sort by y0 then x0
    sorted_boxes = sorted(bboxes, key=lambda b: (b[1], b[0]))
    merged = [list(sorted_boxes[0])]

    for box in sorted_boxes[1:]:
        last = merged[-1]
        # Check for overlap or close proximity (within 10 points)
        if (
            box[0] <= last[2] + 10
            and box[1] <= last[3] + 10
            and box[2] >= last[0] - 10
            and box[3] >= last[1] - 10
        ):
            last[0] = min(last[0], box[0])
            last[1] = min(last[1], box[1])
            last[2] = max(last[2], box[2])
            last[3] = max(last[3], box[3])
        else:
            merged.append(list(box))

    return [tuple(b) for b in merged]


def crop_table_to_image(pdf_path, page_num, bbox, output_path):
    """Crop a detected table region from a PDF page as a PNG image.

    Args:
        pdf_path: Path to the PDF file.
        page_num: Zero-based page number.
        bbox: Tuple (x0, y0, x1, y1) defining the table region.
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

        # High-resolution rendering for table clarity (3x zoom)
        mat = fitz.Matrix(3, 3)
        pix = page.get_pixmap(matrix=mat, clip=clip_rect)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        pix.save(output_path)
        return True
    finally:
        doc.close()


def extract_table_text(pdf_path, page_num, bbox):
    """Extract structured text from a table region using text positioning.

    Attempts to reconstruct a tabular structure from text span positions.
    Falls back to returning raw text if structured extraction fails.

    Args:
        pdf_path: Path to the PDF file.
        page_num: Zero-based page number.
        bbox: Tuple (x0, y0, x1, y1) defining the table region.

    Returns:
        List of lists (rows of cell strings), or None if extraction fails
        (e.g., the text is insufficient for table reconstruction).

    Raises:
        FileNotFoundError: If pdf_path does not exist.
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

        # Get text blocks within the bbox
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

        spans = []
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                line_text = ""
                line_bbox = None
                for span in line["spans"]:
                    sbbox = span["bbox"]
                    # Check if span overlaps with the table region
                    if (
                        sbbox[0] < clip_rect.x1
                        and sbbox[2] > clip_rect.x0
                        and sbbox[1] < clip_rect.y1
                        and sbbox[3] > clip_rect.y0
                    ):
                        line_text += span["text"]
                        if line_bbox is None:
                            line_bbox = list(sbbox)
                        else:
                            line_bbox[0] = min(line_bbox[0], sbbox[0])
                            line_bbox[1] = min(line_bbox[1], sbbox[1])
                            line_bbox[2] = max(line_bbox[2], sbbox[2])
                            line_bbox[3] = max(line_bbox[3], sbbox[3])

                if line_text.strip() and line_bbox is not None:
                    spans.append({
                        "text": line_text.strip(),
                        "x0": line_bbox[0],
                        "y0": line_bbox[1],
                        "x1": line_bbox[2],
                        "y1": line_bbox[3],
                        "cx": (line_bbox[0] + line_bbox[2]) / 2,
                        "cy": (line_bbox[1] + line_bbox[3]) / 2,
                    })

        if len(spans) < 2:
            return None

        # Group into rows by y-coordinate
        row_tolerance = 3
        sorted_by_y = sorted(spans, key=lambda s: s["cy"])
        rows = []
        current_row = [sorted_by_y[0]]

        for span in sorted_by_y[1:]:
            if abs(span["cy"] - current_row[0]["cy"]) < row_tolerance:
                current_row.append(span)
            else:
                rows.append(sorted(current_row, key=lambda s: s["x0"]))
                current_row = [span]
        rows.append(sorted(current_row, key=lambda s: s["x0"]))

        # Detect column boundaries
        all_x_centers = []
        for row in rows:
            for span in row:
                all_x_centers.append(span["cx"])

        if not all_x_centers:
            return None

        # Cluster x-centers into columns
        col_tolerance = 20
        sorted_x = sorted(all_x_centers)
        col_clusters = [[sorted_x[0]]]

        for cx in sorted_x[1:]:
            if cx - col_clusters[-1][-1] < col_tolerance:
                col_clusters[-1].append(cx)
            else:
                col_clusters.append([cx])

        col_positions = [sum(c) / len(c) for c in col_clusters]
        num_cols = len(col_positions)

        # If we only detect 1 column, it's likely not a real table
        if num_cols < 2:
            return None

        # Assign each span to the nearest column
        table_data = []
        for row in rows:
            row_data = [""] * num_cols
            for span in row:
                # Find nearest column
                min_dist = float("inf")
                best_col = 0
                for col_idx, col_x in enumerate(col_positions):
                    dist = abs(span["cx"] - col_x)
                    if dist < min_dist:
                        min_dist = dist
                        best_col = col_idx

                if row_data[best_col]:
                    row_data[best_col] += " " + span["text"]
                else:
                    row_data[best_col] = span["text"]

            table_data.append(row_data)

        # Validate: check if table has meaningful content
        total_cells = sum(1 for row in table_data for cell in row if cell.strip())
        if total_cells < 4:
            return None

        return table_data

    finally:
        doc.close()


def process_all_tables(pdf_path, output_dir):
    """Find and extract all tables across all pages of a PDF.

    Strategy:
        1. First try caption-driven detection via detect_tables_by_caption().
        2. For each caption-detected table, call crop_table_by_caption().
        3. Then fall back to alignment-based detection for tables not found
           by caption search.
        4. Deduplicate: skip alignment-based tables whose bbox overlaps with
           a caption-based table.

    For each detected table, crops an image and attempts text extraction.
    The output format is backward-compatible with the original version.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save extracted tables.

    Returns:
        List of dicts with keys:
            - page (int): Page number where the table was found.
            - bbox (list): Bounding box [x0, y0, x1, y1].
            - image_path (str): Path to the cropped PNG image.
            - text_or_none (list or null): Extracted table text as list of
              rows, or None if text extraction failed.

    Raises:
        FileNotFoundError: If pdf_path does not exist.
    """
    fitz = _ensure_pymupdf()

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)

    results = []
    caption_bbox_set = []  # Collect bboxes from caption-based detection for dedup

    # ------------------------------------------------------------------
    # Phase 1: Caption-driven detection
    # ------------------------------------------------------------------
    try:
        caption_tables = detect_tables_by_caption(pdf_path)
    except Exception as e:
        print(
            f"Warning: caption-based table detection failed: {e}",
            file=sys.stderr,
        )
        caption_tables = []

    for cap_info in caption_tables:
        try:
            result = crop_table_by_caption(
                pdf_path,
                cap_info["page_num"],
                cap_info["caption_bbox"],
                cap_info["table_number"],
                cap_info["caption_text"],
                output_dir,
            )
            if result["image_path"] is not None:
                results.append(result)
                caption_bbox_set.append(result["bbox"])
        except Exception as e:
            print(
                f"Warning: Failed to process caption-detected table "
                f"{cap_info['table_number']} on page {cap_info['page_num']}: {e}",
                file=sys.stderr,
            )

    # ------------------------------------------------------------------
    # Phase 2: Alignment-based fallback for tables not found by captions
    # ------------------------------------------------------------------
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    table_counter = len(results)  # Continue numbering from caption-based results

    for page_num in range(total_pages):
        try:
            bboxes = detect_table_regions(pdf_path, page_num)
        except Exception as e:
            print(
                f"Warning: Failed to detect tables on page {page_num}: {e}",
                file=sys.stderr,
            )
            continue

        for bbox in bboxes:
            # Deduplication: skip if this bbox overlaps with any caption-based bbox
            is_duplicate = False
            for cap_bbox in caption_bbox_set:
                if _bbox_overlap_ratio(bbox, cap_bbox) >= 0.3:
                    is_duplicate = True
                    break

            if is_duplicate:
                continue

            table_counter += 1
            image_filename = f"table_p{page_num}_{table_counter}.png"
            image_path = os.path.join(output_dir, image_filename)

            try:
                crop_table_to_image(pdf_path, page_num, bbox, image_path)
            except Exception as e:
                print(
                    f"Warning: Failed to crop table {table_counter} on page {page_num}: {e}",
                    file=sys.stderr,
                )
                continue

            # Attempt text extraction
            text_result = None
            try:
                text_result = extract_table_text(pdf_path, page_num, bbox)
            except Exception as e:
                print(
                    f"Warning: Failed to extract text from table {table_counter} on page {page_num}: {e}",
                    file=sys.stderr,
                )

            results.append({
                "page": page_num,
                "bbox": list(bbox),
                "image_path": image_filename,
                "text_or_none": text_result,
            })

    # Save results summary
    summary_path = os.path.join(output_dir, "tables_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results


def main():
    """CLI interface for table extraction.

    Detects, crops, and extracts text from all tables in a PDF.
    """
    parser = argparse.ArgumentParser(
        description="Specialized table extraction from PDF documents"
    )
    parser.add_argument(
        "--pdf", required=True, help="Path to the input PDF file"
    )
    parser.add_argument(
        "--output-dir",
        default="./tables_output",
        help="Directory for extracted tables (default: ./tables_output)",
    )

    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf)
    output_dir = os.path.abspath(args.output_dir)

    try:
        results = process_all_tables(pdf_path, output_dir)
        output = {
            "total_tables": len(results),
            "tables": results,
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