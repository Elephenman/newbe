#!/usr/bin/env python3
"""Obsidian markdown assembler and validator for paper deep reading notes.

Builds YAML frontmatter, wikilinks, callouts, Mermaid diagrams, and assembles
complete Obsidian notes from templates. Validates output for correct syntax.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

import yaml

# ---------------------------------------------------------------------------
# Ensure UTF-8 on Windows
# ---------------------------------------------------------------------------
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REQUIRED_FRONTMATTER_FIELDS = [
    "title", "year", "journal", "paper_type", "domains", "read_date", "tags"
]

OPTIONAL_FRONTMATTER_FIELDS = [
    "authors", "corresponding_author", "doi", "pubmed_id", "arxiv_id",
    "keywords", "methods", "tools", "databases", "read_depth",
    "note_version", "aliases", "source_pdf"
]

CALLOUT_TYPES = {"abstract", "figure", "info", "tip", "warning", "example", "question"}

MERMAID_DIAGRAM_TYPES = {"flowchart", "sequence", "graph"}

NODE_SHAPES = {
    "rect": ("[", "]"),
    "rounded": ("(", ")"),
    "stadium": ("([", "])"),
    "diamond": ("{", "}"),
    "circle": ("((", "))"),
    "hexagon": ("{{", "}}"),
    "flag": ("/", "\\"),
    "cylinder": ("[(", ")]"),
    "database": ("[(", ")]"),
    "async": ("(((", ")))"),
}


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def build_frontmatter(metadata: dict) -> str:
    """Build valid YAML frontmatter from a metadata dict.

    Required fields: title, year, journal, paper_type, domains, read_date, tags.
    Lists use YAML array syntax. Tags use ``#category/sub`` format.

    Parameters
    ----------
    metadata : dict
        Key-value pairs. Required keys must be present.

    Returns
    -------
    str
        YAML frontmatter block enclosed in ``---`` delimiters.

    Raises
    ------
    ValueError
        If any required field is missing.
    """
    missing = [f for f in REQUIRED_FRONTMATTER_FIELDS if f not in metadata]
    if missing:
        raise ValueError(f"Missing required frontmatter fields: {missing}")

    ordered: dict[str, Any] = {}
    for field in REQUIRED_FRONTMATTER_FIELDS:
        ordered[field] = _normalize_field(field, metadata[field])
    for field in OPTIONAL_FRONTMATTER_FIELDS:
        if field in metadata:
            ordered[field] = _normalize_field(field, metadata[field])

    # yaml.dump handles list formatting; allow_unicode for Chinese chars
    yaml_str = yaml.dump(
        ordered, allow_unicode=True, default_flow_style=False, sort_keys=False
    ).rstrip()
    return f"---\n{yaml_str}\n---"


def _normalize_field(field: str, value: Any) -> Any:
    """Normalize a single frontmatter field value."""
    if field == "tags":
        if isinstance(value, str):
            value = [value]
        return [_ensure_hash(t) for t in value]
    if field in ("domains", "keywords", "methods", "tools", "databases",
                 "authors", "aliases"):
        if isinstance(value, str):
            return [value]
        return list(value)
    return value


def _ensure_hash(tag: str) -> str:
    """Ensure a tag starts with ``#``."""
    return tag if tag.startswith("#") else f"#{tag}"


def build_wikilinks(concepts: list, existing_notes: list) -> dict:
    """Create [[wikilinks]] for concepts, checking existence of target notes.

    Parameters
    ----------
    concepts : list
        Each entry is either a string (concept name) or a dict
        ``{concept, display}`` with alternative display text.
    existing_notes : list
        List of note titles (without ``.md``) that already exist in the vault.

    Returns
    -------
    dict
        ``{concept_name: wikilink_string}``. Uses ``[[target|display]]``
        format when the display text differs from the target.
    """
    existing_set = {n.replace(".md", "") for n in existing_notes}
    result: dict[str, str] = {}

    for entry in concepts:
        if isinstance(entry, str):
            concept = entry
            display = None
        elif isinstance(entry, dict):
            concept = entry.get("concept", "")
            display = entry.get("display")
        else:
            continue

        if not concept:
            continue

        # Resolve target: prefer existing note, else use concept as-is
        target = concept if concept in existing_set else concept

        if display and display != target:
            wikilink = f"[[{target}|{display}]]"
        else:
            wikilink = f"[[{target}]]"

        result[concept] = wikilink

    return result


def build_callout(callout_type: str, title: str, content: str,
                  folded: bool = True) -> str:
    """Create an Obsidian callout block.

    Parameters
    ----------
    callout_type : str
        One of: abstract, info, tip, warning, example, question.
    title : str
        Callout header text.
    content : str
        Body text (may contain newlines).
    folded : bool
        If True the callout starts collapsed (``-`` modifier).

    Returns
    -------
    str
        Complete callout block string.

    Raises
    ------
    ValueError
        If *callout_type* is not recognised.
    """
    if callout_type not in CALLOUT_TYPES:
        raise ValueError(
            f"Invalid callout type '{callout_type}'. "
            f"Must be one of: {sorted(CALLOUT_TYPES)}"
        )

    modifier = "-" if folded else ""
    header = f"> [!{callout_type}]{modifier} {title}"

    content_lines = content.split("\n")
    body = "\n".join(f"> {line}" for line in content_lines)

    return f"{header}\n{body}"


def build_mermaid_diagram(diagram_type: str, nodes: list,
                          edges: list) -> str:
    """Generate a Mermaid code block.

    Parameters
    ----------
    diagram_type : str
        One of: flowchart, sequence, graph.
    nodes : list[dict]
        Each dict: ``{id, label, shape}``. *shape* is optional (default
        ``rect``).
    edges : list[dict]
        Each dict: ``{from, to, label?, style?}``. *style* can be
        ``-->``, ``---``, ``-.->``, ``==>`` etc.

    Returns
    -------
    str
        ````mermaid ... ```` code block.

    Raises
    ------
    ValueError
        If *diagram_type* is not recognised.
    """
    if diagram_type not in MERMAID_DIAGRAM_TYPES:
        raise ValueError(
            f"Invalid diagram type '{diagram_type}'. "
            f"Must be one of: {sorted(MERMAID_DIAGRAM_TYPES)}"
        )

    lines: list[str] = []

    if diagram_type == "flowchart":
        lines.append("flowchart TD")
    elif diagram_type == "graph":
        lines.append("graph TD")
    elif diagram_type == "sequence":
        lines.append("sequenceDiagram")

    # Nodes
    if diagram_type != "sequence":
        for node in nodes:
            nid = node.get("id", "")
            label = node.get("label", nid)
            shape = node.get("shape", "rect")
            left, right = NODE_SHAPES.get(shape, NODE_SHAPES["rect"])
            lines.append(f"    {nid}{left}{label}{right}")
    else:
        # sequence diagram participants
        for node in nodes:
            nid = node.get("id", "")
            label = node.get("label", nid)
            lines.append(f"    participant {nid} as {label}")

    # Edges
    for edge in edges:
        src = edge.get("from", "")
        tgt = edge.get("to", "")
        label = edge.get("label", "")
        style = edge.get("style", "-->")

        if diagram_type == "sequence":
            arrow_map = {
                "-->": "->>",
                "--": "-->>",
                "-.->": "-->>",
                "==>": "-)",
            }
            arrow = arrow_map.get(style, "->>")
            if label:
                lines.append(f"    {src}{arrow}{tgt}: {label}")
            else:
                lines.append(f"    {src}{arrow}{tgt}")
        else:
            if label:
                lines.append(f"    {src} {style}|{label}| {tgt}")
            else:
                lines.append(f"    {src} {style} {tgt}")

    body = "\n".join(lines)
    return f"```mermaid\n{body}\n```"


def assemble_note(template_path: str, sections: dict,
                  images_dir: str) -> str:
    """Fill a template with section content and resolve image placeholders.

    Parameters
    ----------
    template_path : str
        Path to the template file. Placeholders use ``{{section_name}}``
        syntax. Image placeholders use ``{{img:filename}}``.
    sections : dict
        Mapping of section names to content strings.
    images_dir : str
        Directory containing image files. Images are referenced using
        Obsidian ``![[image_filename]]`` syntax.

    Returns
    -------
    str
        Fully assembled note content.

    Raises
    ------
    FileNotFoundError
        If the template file does not exist.
    ValueError
        If a required section is missing from *sections*.
    """
    tpl = Path(template_path)
    if not tpl.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    content = tpl.read_text(encoding="utf-8")

    # Discover all placeholders
    placeholder_re = re.compile(r"\{\{(\w[\w\-]*)\}\}")
    placeholders = placeholder_re.findall(content)

    # Separate image placeholders from section placeholders
    section_placeholders = [p for p in placeholders if not p.startswith("img_")]
    img_placeholders = [p for p in placeholders if p.startswith("img_")]

    # Validate section placeholders
    missing_sections = [p for p in section_placeholders if p not in sections]
    if missing_sections:
        raise ValueError(f"Missing sections for placeholders: {missing_sections}")

    # Replace section placeholders
    for name in section_placeholders:
        content = content.replace(f"{{{{{name}}}}}", sections[name])

    # Replace image placeholders
    images_path = Path(images_dir)
    for img_ph in img_placeholders:
        # img_placeholder -> filename pattern: img_<name> -> <name>.png etc.
        base_name = img_ph[4:]  # strip 'img_'
        resolved = _resolve_image(base_name, images_path)
        if resolved:
            content = content.replace(f"{{{{{img_ph}}}}}", f"![[{resolved}]]")
        else:
            # leave as-is with a warning
            content = content.replace(
                f"{{{{{img_ph}}}}}",
                f"<!-- MISSING IMAGE: {base_name} -->"
            )

    return content


def _resolve_image(base_name: str, images_dir: Path) -> Optional[str]:
    """Find an image file matching *base_name* in *images_dir*."""
    if not images_dir.exists():
        return None
    for f in images_dir.iterdir():
        stem = f.stem
        if stem == base_name:
            return f.name
    # Fallback: prefix match
    for f in images_dir.iterdir():
        if f.stem.startswith(base_name) or base_name.startswith(f.stem):
            return f.name
    return None


def validate_obsidian_markdown(file_path: str) -> dict:
    """Validate an Obsidian markdown file for common syntax issues.

    Checks:
    1. YAML frontmatter is parseable.
    2. All wikilinks have valid syntax (``[[target]]`` or ``[[target|display]]``).
    3. Callout blocks have correct format.
    4. Mermaid blocks have valid syntax (basic structural check).
    5. Image references point to existing files (same directory or ``images/``).

    Parameters
    ----------
    file_path : str
        Path to the ``.md`` file to validate.

    Returns
    -------
    dict
        ``{valid: bool, errors: list[str], warnings: list[str]}``
    """
    result: dict[str, Any] = {"valid": True, "errors": [], "warnings": []}

    p = Path(file_path)
    if not p.exists():
        result["valid"] = False
        result["errors"].append(f"File not found: {file_path}")
        return result

    text = p.read_text(encoding="utf-8")
    note_dir = p.parent

    # 1. YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        result["valid"] = False
        result["errors"].append("No YAML frontmatter found (missing --- delimiters)")
    else:
        try:
            yaml.safe_load(fm_match.group(1))
        except yaml.YAMLError as exc:
            result["valid"] = False
            result["errors"].append(f"YAML parse error: {exc}")

    # 2. Wikilinks
    wikilink_re = re.compile(r"\[\[(.*?)\]\]")
    for m in wikilink_re.finditer(text):
        inner = m.group(1)
        # valid: target or target|display
        if "|" in inner:
            parts = inner.split("|", 1)
            if not parts[0].strip():
                result["errors"].append(
                    f"Empty wikilink target at position {m.start()}: {m.group(0)}"
                )
                result["valid"] = False
        else:
            if not inner.strip():
                result["errors"].append(
                    f"Empty wikilink at position {m.start()}: {m.group(0)}"
                )
                result["valid"] = False
        # Warn about heading/block references (# or ^) without pipe
        if "#" in inner and "|" not in inner:
            result["warnings"].append(
                f"Wikilink with heading/block ref but no display text: {m.group(0)}"
            )

    # 3. Callout blocks
    callout_re = re.compile(r"^>\s*\[!(\w+)\]([+-]?)\s*(.*)$", re.MULTILINE)
    for m in callout_re.finditer(text):
        ctype = m.group(1).lower()
        modifier = m.group(2)
        if ctype not in CALLOUT_TYPES:
            result["warnings"].append(
                f"Unrecognised callout type '{ctype}' at position {m.start()}"
            )
        if modifier not in ("", "+", "-"):
            result["errors"].append(
                f"Invalid callout modifier '{modifier}' at position {m.start()}"
            )
            result["valid"] = False

    # 4. Mermaid blocks
    mermaid_re = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
    for m in mermaid_re.finditer(text):
        body = m.group(1).strip()
        if not body:
            result["errors"].append("Empty mermaid block found")
            result["valid"] = False
            continue
        first_line = body.split("\n")[0].strip()
        valid_starts = ("flowchart", "graph", "sequenceDiagram", "classDiagram",
                        "stateDiagram", "erDiagram", "gantt", "pie", "journey",
                        "mindmap", "timeline", "quadrantChart", "xychart")
        if not any(first_line.startswith(kw) for kw in valid_starts):
            result["errors"].append(
                f"Mermaid block does not start with a valid diagram type: "
                f"'{first_line}'"
            )
            result["valid"] = False

    # 5. Image references
    img_re = re.compile(r"!\[\[(.*?)\]\]")
    for m in img_re.finditer(text):
        img_name = m.group(1).strip()
        # Strip display text if present
        img_file = img_name.split("|")[0].strip()
        # Check that image reference includes file extension
        if not re.search(r"\.\w+$", img_file):
            result["warnings"].append(
                f"Image reference '{img_file}' is missing file extension "
                f"(e.g. .png). Use ![[{img_file}.png|w800]] instead of "
                f"![[{img_file}|w800]]"
            )
        img_path_direct = note_dir / img_file
        img_path_subdir = note_dir / "images" / img_file
        if not img_path_direct.exists() and not img_path_subdir.exists():
            result["warnings"].append(
                f"Image reference '{img_file}' not found in "
                f"{note_dir} or {note_dir / 'images'}"
            )

    # 6. source_pdf field and PDF wikilink
    if fm_match:
        fm_data = yaml.safe_load(fm_match.group(1))
        source_pdf = fm_data.get("source_pdf", "")
        if not source_pdf:
            result["warnings"].append(
                "YAML frontmatter is missing 'source_pdf' field. "
                "Add the original PDF path so readers can open it from Obsidian."
            )

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for obsidian_note_builder."""
    parser = argparse.ArgumentParser(
        description="Obsidian note assembler and validator"
    )
    parser.add_argument("--template", type=str, help="Path to template file")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--metadata", type=str,
                        help="Path to JSON file with metadata")
    parser.add_argument("--sections", type=str,
                        help="Path to JSON file with section content")
    parser.add_argument("--images-dir", type=str, default="",
                        help="Directory containing images")
    parser.add_argument("--validate", type=str,
                        help="Path to .md file to validate")

    args = parser.parse_args()

    output_data: dict[str, Any] = {"success": False}

    try:
        if args.validate:
            result = validate_obsidian_markdown(args.validate)
            output_data["success"] = True
            output_data["result"] = result

        elif args.template and args.metadata and args.sections:
            metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
            sections = json.loads(Path(args.sections).read_text(encoding="utf-8"))

            frontmatter = build_frontmatter(metadata)

            # Add frontmatter as a section if not provided
            if "frontmatter" not in sections:
                sections["frontmatter"] = frontmatter

            note_content = assemble_note(
                args.template, sections, args.images_dir or "."
            )

            if args.output:
                out_path = Path(args.output)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(note_content, encoding="utf-8")
                output_data["success"] = True
                output_data["output_path"] = str(out_path)
            else:
                output_data["success"] = True
                output_data["content"] = note_content
        else:
            parser.print_help()
            sys.exit(0)

    except Exception as exc:
        output_data["success"] = False
        output_data["error"] = str(exc)

    print(json.dumps(output_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
