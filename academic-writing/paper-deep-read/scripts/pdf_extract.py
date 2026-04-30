#!/usr/bin/env python3
"""Caption-driven figure extraction from academic PDFs.

Extracts the paper's original embedded high-resolution images directly
from the PDF, matched to Figure/Table numbers via caption positioning.

Usage:
    python pdf_extract.py --pdf paper.pdf --output-dir ./output --mode figures
    python pdf_extract.py --pdf paper.pdf --output-dir ./output --mode text
    python pdf_extract.py --pdf paper.pdf --output-dir ./output --mode full
"""

import sys
import os
import io
import json
import argparse
import re

sys.stdout.reconfigure(encoding="utf-8")

# Lazy import — fitz is only loaded when actually needed
_fitz = None


def get_fitz():
    """Get the fitz module, installing pymupdf if necessary."""
    global _fitz
    if _fitz is not None:
        return _fitz
    try:
        import fitz
        _fitz = fitz
        return _fitz
    except ImportError:
        print("pymupdf not found, installing...", file=sys.stderr)
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pymupdf"],
            stdout=sys.stderr,
            stderr=subprocess.DEVNULL,
        )
        import fitz
        _fitz = fitz
        return _fitz


# Minimum image size to filter logos/icons/decorative elements
_MIN_W = 200
_MIN_H = 200

# Caption patterns — line-starting with Figure/Table number
_CAP_PATTERNS = [
    (re.compile(r"^Figure\s+(\d+)\s*[\.:\-|—]\s", re.I), "figure", False),
    (re.compile(r"^Fig\.\s*(\d+)\s*[\.:\-|—]\s", re.I), "figure", False),
    (re.compile(r"^Figure\s+S(\d+)\s*[\.:\-|—]\s", re.I), "figure", True),
    (re.compile(r"^Fig\.\s*S(\d+)\s*[\.:\-|—]\s", re.I), "figure", True),
    (re.compile(r"^Table\s+(\d+)\s*[\.:\-|—]\s", re.I), "table", False),
    (re.compile(r"^Table\s+S(\d+)\s*[\.:\-|—]\s", re.I), "table", True),
    # Standalone "Figure N." at line end
    (re.compile(r"^Figure\s+(\d+)\s*[\.]?\s*$", re.I), "figure", False),
    (re.compile(r"^Fig\.\s*(\d+)\s*[\.]?\s*$", re.I), "figure", False),
    (re.compile(r"^Table\s+(\d+)\s*[\.]?\s*$", re.I), "table", False),
    # Chinese
    (re.compile(r"^图\s*(\d+)\s*[\.：\-]\s", re.I), "figure", False),
    (re.compile(r"^表\s*(\d+)\s*[\.：\-]\s", re.I), "table", False),
]


def _gen_filename(fig_num, is_supp, fig_type):
    """Generate filename matching paper's Figure/Table numbering.

    Always outputs .png for Obsidian consistency.
    Examples: fig1.png, fig2.png, figS1.png, table1.png
    """
    prefix = "fig" if fig_type == "figure" else "table"
    num = f"S{fig_num}" if is_supp else fig_num
    return f"{prefix}{num}.png"


# ── Caption Detection ──────────────────────────────────────────────


def detect_captions(pdf_path):
    """Scan all pages for figure/table captions with position info."""
    fitz = get_fitz()
    doc = fitz.open(pdf_path)
    captions = []

    for pn in range(len(doc)):
        page = doc[pn]
        td = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)

        for block in td.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                line_text = "".join(s.get("text", "") for s in spans)
                stripped = line_text.strip()

                for pat, ftype, supp in _CAP_PATTERNS:
                    m = pat.match(stripped)
                    if m:
                        # Collect bbox from all spans in this line
                        xs = [s["bbox"][0] for s in spans]
                        ys = [s["bbox"][1] for s in spans]
                        x1s = [s["bbox"][2] for s in spans]
                        y1s = [s["bbox"][3] for s in spans]

                        # Collect continuation lines in same block
                        cap_text = line_text.strip()
                        all_lines = block.get("lines", [])
                        found_idx = None
                        for li_idx, li in enumerate(all_lines):
                            li_txt = "".join(
                                s.get("text", "") for s in li.get("spans", [])
                            )
                            if m.group(0) in li_txt and found_idx is None:
                                found_idx = li_idx

                        if found_idx is not None:
                            for ci in range(found_idx + 1, len(all_lines)):
                                ct = "".join(
                                    s.get("text", "")
                                    for s in all_lines[ci].get("spans", [])
                                ).strip()
                                if any(p.match(ct) for p, _, _ in _CAP_PATTERNS):
                                    break
                                if ct:
                                    cap_text += " " + ct
                                    for s in all_lines[ci].get("spans", []):
                                        xs.append(s["bbox"][0])
                                        ys.append(s["bbox"][1])
                                        x1s.append(s["bbox"][2])
                                        y1s.append(s["bbox"][3])

                        captions.append({
                            "fig_num": m.group(1),
                            "fig_type": ftype,
                            "page": pn,
                            "caption": cap_text,
                            "bbox": {
                                "x0": min(xs) if xs else 0,
                                "y0": min(ys) if ys else 0,
                                "x1": max(x1s) if x1s else 0,
                                "y1": max(y1s) if y1s else 0,
                            },
                            "is_supp": supp,
                        })
                        break

    doc.close()
    return captions


# ── Embedded Image Discovery ───────────────────────────────────────


def discover_images(pdf_path):
    """Find all significant embedded images with their positions.

    Uses page.get_images() for real xrefs + pixel dimensions,
    page.get_image_info() for bbox positions.
    Links them via matching pixel dimensions (width × height).
    """
    fitz = get_fitz()
    doc = fitz.open(pdf_path)
    images = []

    for pn in range(len(doc)):
        page = doc[pn]

        # Real xrefs + pixel dims from get_images()
        img_list = page.get_images(full=True)
        xref_dims = {}
        for entry in img_list:
            xref = entry[0]
            w, h = entry[2], entry[3]
            xref_dims[xref] = (w, h)

        # Bbox positions from get_image_info()
        img_infos = page.get_image_info()
        info_by_size = {}
        for info in img_infos:
            iw, ih = info.get("width", 0), info.get("height", 0)
            if iw < _MIN_W or ih < _MIN_H:
                continue
            bbox = info.get("bbox", (0, 0, 0, 0))
            key = (iw, ih)
            if key not in info_by_size:
                info_by_size[key] = bbox

        # Match xrefs to bboxes via pixel dimensions
        for xref, (w, h) in xref_dims.items():
            if w < _MIN_W or h < _MIN_H:
                continue

            bbox = info_by_size.get((w, h), (0, 0, 0, 0))
            # Fallback: approximate match (±2px tolerance)
            if bbox == (0, 0, 0, 0):
                for sk, sb in info_by_size.items():
                    if abs(sk[0] - w) <= 2 and abs(sk[1] - h) <= 2:
                        bbox = sb
                        break

            # Fallback: extract image to verify it's real
            if bbox == (0, 0, 0, 0):
                try:
                    base = doc.extract_image(xref)
                    ew, eh = base["width"], base["height"]
                    if ew < _MIN_W or eh < _MIN_H:
                        continue
                    pr = page.rect
                    bbox = (pr.x0, pr.y0, pr.x1, pr.y1)
                except Exception:
                    continue

            images.append({
                "page": pn, "bbox": bbox,
                "width": w, "height": h, "xref": xref,
            })

    doc.close()

    # Deduplicate by xref (keep entry with largest bbox area)
    seen = {}
    for img in images:
        xref = img["xref"]
        area = (img["bbox"][2] - img["bbox"][0]) * (img["bbox"][3] - img["bbox"][1])
        if xref not in seen or area > (seen[xref][1]):
            seen[xref] = (img, area)

    return [v[0] for v in seen.values()]


# ── Caption-Image Matching ─────────────────────────────────────────


def match_captions_images(captions, images, pdf_path):
    """Match each caption to its nearest embedded image.

    Strategy: figures are above their captions on the same page.
    Match by finding the nearest image whose bbox bottom is closest
    to the caption's bbox top.
    """
    fitz = get_fitz()
    doc = fitz.open(pdf_path)

    imgs_by_page = {}
    for img in images:
        p = img["page"]
        imgs_by_page.setdefault(p, []).append(img)

    matched = []
    used_xrefs = set()

    for cap in captions:
        cp = cap["page"]
        cy_top = cap["bbox"]["y0"]
        page_imgs = imgs_by_page.get(cp, [])

        if not page_imgs:
            # Image might be on previous page
            page_imgs = imgs_by_page.get(cp - 1, [])

        if not page_imgs:
            matched.append({"caption": cap, "image": None, "method": "no_image"})
            continue

        best_img, best_dist = None, float("inf")
        for img in page_imgs:
            if img["xref"] in used_xrefs:
                continue
            dist = abs(img["bbox"][3] - cy_top)
            if dist < best_dist:
                best_dist = dist
                best_img = img

        if best_img:
            used_xrefs.add(best_img["xref"])
            matched.append({"caption": cap, "image": best_img, "method": "position"})
        else:
            matched.append({"caption": cap, "image": None, "method": "all_used"})

    doc.close()
    return matched


# ── Figure Extraction ──────────────────────────────────────────────


def extract_figures(pdf_path, output_dir):
    """Extract figures by directly pulling embedded images from the PDF.

    No region cropping — we get the exact original image the authors
    embedded. Caption positions determine Figure/Table numbering only.
    """
    fitz = get_fitz()
    os.makedirs(output_dir, exist_ok=True)

    captions = detect_captions(pdf_path)
    images = discover_images(pdf_path)

    if not captions and not images:
        print("WARNING: No captions or images found.", file=sys.stderr)
        return {"panels": [], "total": 0, "caption_failed": True}

    if captions:
        # Deduplicate captions: same fig number on same page → keep longest
        seen = {}
        for c in captions:
            key = (c["fig_num"], c["fig_type"], c["page"], c["is_supp"])
            if key not in seen or len(c["caption"]) > len(seen[key]["caption"]):
                seen[key] = c
        captions = sorted(seen.values(), key=lambda c: (c["page"], c["fig_num"]))
        matches = match_captions_images(captions, images, pdf_path)
    else:
        matches = []

    doc = fitz.open(pdf_path)
    panels = []

    for m in matches:
        cap, img = m["caption"], m["image"]

        if img is None:
            if cap:
                print(f"  Skip: '{cap['caption'][:40]}' has no matching image",
                      file=sys.stderr)
            continue

        # Extract embedded image directly
        try:
            base = doc.extract_image(img["xref"])
        except Exception as e:
            print(f"  Skip: xref {img['xref']} failed: {e}", file=sys.stderr)
            continue

        img_bytes = base["image"]
        img_ext = base["ext"]
        img_w, img_h = base["width"], base["height"]

        if cap is not None:
            filename = _gen_filename(cap["fig_num"], cap["is_supp"], cap["fig_type"])
            caption_text = cap["caption"]
            fig_num = cap["fig_num"]
            fig_type = cap["fig_type"]
            is_supp = cap["is_supp"]
        else:
            # No caption → skip (only extract caption-identified figures)
            continue

        filepath = os.path.join(output_dir, filename)

        # Save as PNG (convert JPEG if needed)
        if img_ext == "png":
            with open(filepath, "wb") as f:
                f.write(img_bytes)
        else:
            try:
                from PIL import Image as PILImage
                pil_img = PILImage.open(io.BytesIO(img_bytes))
                pil_img.save(filepath, "PNG")
            except ImportError:
                with open(filepath, "wb") as f:
                    f.write(img_bytes)

        panels.append({
            "fig_num": fig_num, "page": img["page"],
            "filename": filename, "fig_type": fig_type,
            "is_supp": is_supp, "caption": caption_text,
            "width": img_w, "height": img_h,
        })
        print(f"  Extracted: {filename} ({img_w}x{img_h})")

    doc.close()
    return {"panels": panels, "total": len(panels),
            "caption_failed": len(captions) == 0}


# ── Text Extraction & Structure ────────────────────────────────────


def extract_text(pdf_path, start=0, end=None):
    """Extract text from a page range."""
    fitz = get_fitz()
    doc = fitz.open(pdf_path)
    total = len(doc)
    if end is None:
        end = total
    end = min(end, total)

    result = {}
    for pn in range(max(start, 0), end):
        result[pn] = doc[pn].get_text("text")

    doc.close()
    return result


_SEC_PATTERNS = [
    re.compile(r"^(?:\d+\.?\s*)?abstract\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?introduction\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?(?:related\s+work|background|literature\s+review)\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?(?:methods?|methodology|materials?\s+and\s+methods?|experimental)\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?(?:results?|results?\s+and\s+discussion|findings?)\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?discussion\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?(?:conclusions?|concluding\s+remarks?|summary)\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?(?:acknowledg(?:ement|ment)s?|funding)\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?(?:references?|bibliography)\b", re.I),
    re.compile(r"^(?:\d+\.?\s*)?(?:appendix|appendices|supplementary)\b", re.I),
]


def detect_structure(pdf_path):
    """Identify section boundaries from heading patterns."""
    fitz = get_fitz()
    doc = fitz.open(pdf_path)
    sections = []

    for pn in range(len(doc)):
        for line in doc[pn].get_text("text").split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            for pat in _SEC_PATTERNS:
                if pat.match(stripped):
                    sections.append((stripped, pn))
                    break

    doc.close()

    if not sections:
        return {}

    seen = set()
    unique = []
    for name, page in sections:
        key = (name.lower().strip(), page)
        if key not in seen:
            seen.add(key)
            unique.append((name.strip(), page))

    total = len(doc)
    result = {}
    for i, (name, start) in enumerate(unique):
        end = unique[i + 1][1] - 1 if i + 1 < len(unique) else total - 1
        result[name] = (start, max(end, start))

    doc.close()
    return result


# ── Batch Extract ───────────────────────────────────────────────────


def batch_extract(pdf_path, output_dir, batch_size=8):
    """Full extraction: text + figures + structure."""
    fitz = get_fitz()
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    total = len(doc)
    doc.close()

    # Text batches
    for bs in range(0, total, batch_size):
        be = min(bs + batch_size, total)
        batch = extract_text(pdf_path, start=bs, end=be)
        fname = f"text_batch_{bs}_{be}.txt"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            for pn in range(bs, be):
                f.write(f"\n{'=' * 60}\nPAGE {pn + 1}\n{'=' * 60}\n\n")
                f.write(batch.get(pn, ""))

    # Figures
    fig_dir = os.path.join(output_dir, "images")
    fig_result = extract_figures(pdf_path, fig_dir)

    # Structure
    structure = detect_structure(pdf_path)
    with open(os.path.join(output_dir, "structure.json"), "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    summary = {
        "total_pages": total,
        "figures": fig_result["panels"],
        "total_figures": fig_result["total"],
        "caption_failed": fig_result["caption_failed"],
        "structure": structure,
    }

    with open(os.path.join(output_dir, "extraction_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return summary


# ── CLI ────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Caption-driven PDF figure extraction for academic papers")
    parser.add_argument("--pdf", required=True, help="Path to PDF")
    parser.add_argument("--output-dir", default="./pdf_output", help="Output directory")
    parser.add_argument("--mode", choices=["text", "figures", "full"], default="full")
    parser.add_argument("--batch-size", type=int, default=8)

    args = parser.parse_args()
    pdf_path = os.path.abspath(args.pdf)
    output_dir = os.path.abspath(args.output_dir)

    try:
        if args.mode == "text":
            os.makedirs(output_dir, exist_ok=True)
            result = extract_text(pdf_path)
            fpath = os.path.join(output_dir, "full_text.txt")
            with open(fpath, "w", encoding="utf-8") as f:
                for pn in sorted(result.keys()):
                    f.write(f"\n{'=' * 60}\nPAGE {pn + 1}\n{'=' * 60}\n\n")
                    f.write(result[pn])
            output = {"mode": "text", "total_pages": len(result)}

        elif args.mode == "figures":
            result = extract_figures(pdf_path, output_dir)
            output = {"mode": "figures", "total": result["total"],
                      "panels": result["panels"]}

        elif args.mode == "full":
            output = batch_extract(pdf_path, output_dir, args.batch_size)

        print(json.dumps(output, indent=2, ensure_ascii=False))

    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()