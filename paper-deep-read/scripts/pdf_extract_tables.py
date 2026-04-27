#!/usr/bin/env python3
"""Specialized table extraction from PDF documents.

Detects table regions by analyzing text block alignment, crops them as images,
and attempts structured text extraction from table cells.

Usage:
    python pdf_extract_tables.py --pdf paper.pdf --output-dir ./tables
"""

import sys
import os
import json
import argparse
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

    For each detected table, crops an image and attempts text extraction.

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

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    results = []
    table_counter = 0

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
