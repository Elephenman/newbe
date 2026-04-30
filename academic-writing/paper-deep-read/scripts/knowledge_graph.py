#!/usr/bin/env python3
"""Mermaid concept graph generator for multi-paper knowledge bases.

Scans Obsidian notes for concepts (wikilinks, tags, YAML fields), builds
concept-sharing graphs between papers, traces method evolution timelines,
maps tool ecosystems, and generates Mermaid diagram code.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
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

# YAML fields that contain concept-like values
CONCEPT_FIELDS = ("keywords", "methods", "tools", "databases")

# Maximum number of nodes before splitting into subgraphs
MAX_NODES_PER_GRAPH = 15

# Mermaid arrow styles
ARROW_STYLES = {
    "solid": "-->",
    "dashed": "-.->",
    "thick": "==>",
    "dotted": "-.->",
    "bidirectional": "<-->",
    "undirected": "---",
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown text."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _extract_wikilinks(text: str) -> list[str]:
    """Extract wikilink targets from markdown text (excluding images)..

    Skips ``![[...]]`` image references. Returns deduplicated list of
    targets (without display text).
    """
    # Match [[...]] but NOT ![[...]]
    pattern = r"(?<!\!)\[\[([^\]]+)\]\]"
    targets = []
    for m in re.finditer(pattern, text):
        inner = m.group(1)
        # Strip heading/block references and display text
        target = inner.split("|")[0].split("#")[0].split("^")[0].strip()
        if target:
            targets.append(target)
    return list(dict.fromkeys(targets))  # deduplicate, preserve order


def _extract_tags(frontmatter: dict, text: str) -> list[str]:
    """Extract tags from both frontmatter and inline ``#tag`` syntax."""
    tags: list[str] = []

    # From frontmatter
    fm_tags = frontmatter.get("tags", [])
    if isinstance(fm_tags, str):
        fm_tags = [fm_tags]
    for t in fm_tags:
        t_clean = t.strip().lstrip("#")
        if t_clean:
            tags.append(t_clean)

    # From inline text (avoid matching headings or wikilinks)
    for m in re.finditer(r"(?<!\[\[)\B#([a-zA-Z\u4e00-\u9fff][\w/\-]*)", text):
        tag = m.group(1)
        if tag and tag not in tags:
            tags.append(tag)

    return tags


def _extract_concept_fields(frontmatter: dict) -> list[str]:
    """Extract concept values from YAML fields like methods, tools, etc."""
    concepts: list[str] = []
    for field in CONCEPT_FIELDS:
        val = frontmatter.get(field, [])
        if isinstance(val, str):
            concepts.append(val)
        elif isinstance(val, list):
            concepts.extend(str(v) for v in val)
    return concepts


def _safe_id(name: str) -> str:
    """Convert a concept or paper name to a valid Mermaid node ID."""
    # Replace non-alphanumeric chars (except CJK) with underscores
    safe = re.sub(r"[^\w\u4e00-\u9fff]", "_", name)
    # Ensure starts with letter or underscore
    if safe and safe[0].isdigit():
        safe = f"n_{safe}"
    if not safe:
        safe = "unknown"
    return safe


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def extract_concepts(notes_dir: str) -> list[dict]:
    """Scan all ``.md`` files and extract concepts.

    Concepts are drawn from wikilinks, tags, and YAML fields
    (keywords, methods, tools, databases).

    Parameters
    ----------
    notes_dir : str
        Directory containing Obsidian note files.

    Returns
    -------
    list[dict]
        Each dict: ``{concept, type, frequency, source_notes}``.
        *type* is one of ``wikilink``, ``tag``, ``keyword``, ``method``,
        ``tool``, ``database``.
    """
    notes_path = Path(notes_dir)
    if not notes_path.exists():
        return []

    # Aggregate concepts across all notes
    concept_data: dict[str, dict[str, Any]] = {}
    # concept -> {types: set, frequency: int, source_notes: list}

    md_files = list(notes_path.rglob("*.md"))
    # Also check subdirectories one level down
    for sub in notes_path.iterdir():
        if sub.is_dir():
            md_files.extend(sub.rglob("*.md"))

    # Deduplicate by resolved path
    seen_paths: set[str] = set()
    unique_files: list[Path] = []
    for f in md_files:
        try:
            resolved = str(f.resolve())
        except OSError:
            resolved = str(f)
        if resolved not in seen_paths:
            seen_paths.add(resolved)
            unique_files.append(f)

    for fpath in unique_files:
        try:
            text = fpath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        fm = _parse_frontmatter(text)
        note_name = fpath.stem

        # Wikilinks
        for wl in _extract_wikilinks(text):
            if wl not in concept_data:
                concept_data[wl] = {
                    "types": set(), "frequency": 0, "source_notes": []
                }
            concept_data[wl]["types"].add("wikilink")
            concept_data[wl]["frequency"] += 1
            if note_name not in concept_data[wl]["source_notes"]:
                concept_data[wl]["source_notes"].append(note_name)

        # Tags
        for tag in _extract_tags(fm, text):
            if tag not in concept_data:
                concept_data[tag] = {
                    "types": set(), "frequency": 0, "source_notes": []
                }
            concept_data[tag]["types"].add("tag")
            concept_data[tag]["frequency"] += 1
            if note_name not in concept_data[tag]["source_notes"]:
                concept_data[tag]["source_notes"].append(note_name)

        # YAML concept fields
        field_type_map = {
            "keywords": "keyword",
            "methods": "method",
            "tools": "tool",
            "databases": "database",
        }
        for field in CONCEPT_FIELDS:
            for val in _extract_concept_fields({field: fm.get(field, [])}):
                if val not in concept_data:
                    concept_data[val] = {
                        "types": set(), "frequency": 0, "source_notes": []
                    }
                concept_data[val]["types"].add(field_type_map.get(field, "keyword"))
                concept_data[val]["frequency"] += 1
                if note_name not in concept_data[val]["source_notes"]:
                    concept_data[val]["source_notes"].append(note_name)

    # Build result list
    results: list[dict] = []
    for concept, data in concept_data.items():
        # Pick the most specific type
        type_priority = ["method", "tool", "database", "keyword", "tag", "wikilink"]
        chosen_type = "wikilink"
        for t in type_priority:
            if t in data["types"]:
                chosen_type = t
                break

        results.append({
            "concept": concept,
            "type": chosen_type,
            "frequency": data["frequency"],
            "source_notes": data["source_notes"],
        })

    # Sort by frequency descending
    results.sort(key=lambda x: x["frequency"], reverse=True)
    return results


def build_concept_graph(concepts: list, notes: list) -> str:
    """Create a Mermaid graph connecting papers that share concepts.

    Papers are represented as nodes; shared concepts form edges with
    the concept name as the edge label.

    Parameters
    ----------
    concepts : list[dict]
        Output of :func:`extract_concepts`.
    notes : list[dict]
        Each dict must contain ``title`` and optionally ``year``.

    Returns
    -------
    str
        Mermaid graph code string (without `````mermaid````` fences).
    """
    # Build a mapping: concept -> list of papers that mention it
    concept_papers: dict[str, list[str]] = defaultdict(list)
    for c in concepts:
        for sn in c.get("source_notes", []):
            concept_papers[c["concept"]].append(sn)

    # Build edges between papers sharing concepts
    edges: list[dict] = []
    edge_labels: dict[tuple[str, str], list[str]] = defaultdict(list)

    for concept, paper_list in concept_papers.items():
        if len(paper_list) < 2:
            continue
        # Create edges between all pairs
        unique_papers = list(dict.fromkeys(paper_list))
        for i in range(len(unique_papers)):
            for j in range(i + 1, len(unique_papers)):
                pair = (unique_papers[i], unique_papers[j])
                edge_labels[pair].append(concept)

    # Build graph data
    paper_ids: dict[str, str] = {}
    nodes: list[dict] = []
    for n in notes:
        title = n.get("title", "Unknown")
        nid = _safe_id(title)
        paper_ids[title] = nid
        # Also map by note filename (stem)
        nodes.append({"id": nid, "label": title, "shape": "rounded"})

    # Also add nodes from edges that may not be in the notes list
    for pair in edge_labels:
        for paper_name in pair:
            if paper_name not in paper_ids:
                nid = _safe_id(paper_name)
                paper_ids[paper_name] = nid
                nodes.append({"id": nid, "label": paper_name, "shape": "rounded"})

    graph_edges: list[dict] = []
    for (p1, p2), labels in edge_labels.items():
        id1 = paper_ids.get(p1, _safe_id(p1))
        id2 = paper_ids.get(p2, _safe_id(p2))
        # Truncate label if too many shared concepts
        label_text = ", ".join(labels[:3])
        if len(labels) > 3:
            label_text += f" (+{len(labels) - 3})"
        graph_edges.append({
            "from": id1, "to": id2,
            "label": label_text, "style": "-->"
        })

    graph_data = {"nodes": nodes, "edges": graph_edges}
    return generate_mermaid(graph_data, layout="LR")


def build_method_evolution(method_name: str, notes: list) -> str:
    """Trace a method's evolution across papers chronologically.

    Generates a timeline Mermaid diagram showing how the method
    was used or improved over time.

    Parameters
    ----------
    method_name : str
        Name of the method to trace.
    notes : list[dict]
        Each dict must contain ``title`` and ``year``, and optionally
        ``methods`` (list of method names).

    Returns
    -------
    str
        Mermaid timeline diagram code string.
    """
    # Filter notes that mention the method
    relevant: list[dict] = []
    for n in notes:
        methods = n.get("methods", [])
        if isinstance(methods, str):
            methods = [methods]
        keywords = n.get("keywords", [])
        if isinstance(keywords, str):
            keywords = [keywords]
        title = n.get("title", "")

        search_pool = [m.lower() for m in methods] + \
                      [k.lower() for k in keywords] + \
                      [title.lower()]
        if method_name.lower() in " ".join(search_pool):
            relevant.append(n)

    # Sort by year
    relevant.sort(key=lambda x: int(x.get("year", 0)))

    if not relevant:
        return f"graph TD\n    A[No papers found for: {method_name}]"

    # Build timeline as a linear flowchart
    nodes: list[dict] = []
    edges: list[dict] = []

    prev_id: Optional[str] = None
    for i, paper in enumerate(relevant):
        title = paper.get("title", "Unknown")
        year = paper.get("year", "?")
        nid = f"P{i}"
        label = f"{year}: {title}"
        if len(label) > 60:
            label = label[:57] + "..."
        nodes.append({"id": nid, "label": label, "shape": "stadium"})

        if prev_id is not None:
            edges.append({
                "from": prev_id, "to": nid,
                "label": "evolved", "style": "-->"
            })
        prev_id = nid

    # Add method header node
    header_id = "M0"
    header_label = method_name
    nodes.insert(0, {"id": header_id, "label": header_label, "shape": "hexagon"})
    edges.insert(0, {
        "from": header_id, "to": nodes[1]["id"],
        "label": "first appear", "style": "-.->"
    })

    graph_data = {"nodes": nodes, "edges": edges}
    return generate_mermaid(graph_data, layout="TD")


def build_tool_ecosystem(notes: list) -> str:
    """Map tools mentioned in papers and their relationships.

    Generates a Mermaid diagram showing which tools are used together
    (co-occurrence in the same paper). Tools are nodes; shared usage
    forms edges.

    Parameters
    ----------
    notes : list[dict]
        Each dict should contain ``tools`` (list of tool names) and
        optionally ``title`` and ``year``.

    Returns
    -------
    str
        Mermaid graph code string.
    """
    # Collect tools per paper
    tool_papers: dict[str, list[str]] = defaultdict(list)
    paper_tools: dict[str, list[str]] = defaultdict(list)

    for n in notes:
        title = n.get("title", "Unknown")
        tools = n.get("tools", [])
        if isinstance(tools, str):
            tools = [tools]
        for tool in tools:
            tool_papers[tool].append(title)
            paper_tools[title].append(tool)

    # Build co-occurrence edges
    co_occurrence: dict[tuple[str, str], int] = defaultdict(int)
    for paper, tools in paper_tools.items():
        unique_tools = list(dict.fromkeys(tools))
        for i in range(len(unique_tools)):
            for j in range(i + 1, len(unique_tools)):
                pair = tuple(sorted([unique_tools[i], unique_tools[j]]))
                co_occurrence[pair] += 1

    # Build nodes and edges
    all_tools = sorted(tool_papers.keys(),
                       key=lambda t: len(tool_papers[t]), reverse=True)
    nodes: list[dict] = []
    edges: list[dict] = []

    for tool in all_tools:
        nid = _safe_id(tool)
        count = len(tool_papers[tool])
        label = f"{tool} ({count})"
        nodes.append({"id": nid, "label": label, "shape": "rounded"})

    for (t1, t2), count in sorted(co_occurrence.items(),
                                   key=lambda x: x[1], reverse=True):
        id1 = _safe_id(t1)
        id2 = _safe_id(t2)
        style = "==>" if count >= 3 else "-->" if count >= 2 else "---"
        edges.append({
            "from": id1, "to": id2,
            "label": f"{count} papers", "style": style
        })

    graph_data = {"nodes": nodes, "edges": edges}
    return generate_mermaid(graph_data, layout="TD")


def generate_mermaid(graph_data: dict, layout: str = "TD") -> str:
    """Convert structured graph data to Mermaid syntax.

    Handles large graphs by splitting into subgraphs if the number of
    nodes exceeds :data:`MAX_NODES_PER_GRAPH`.

    Parameters
    ----------
    graph_data : dict
        ``{nodes: list[dict], edges: list[dict]}``.  Each node:
        ``{id, label, shape?}``.  Each edge: ``{from, to, label?, style?}``.
    layout : str
        Direction: ``TD``, ``LR``, or ``RL``.

    Returns
    -------
    str
        Mermaid graph code string (without `````mermaid````` fences).
    """
    if layout not in ("TD", "LR", "RL"):
        layout = "TD"

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    lines: list[str] = [f"graph {layout}"]

    shape_map = {
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

    need_subgraphs = len(nodes) > MAX_NODES_PER_GRAPH

    if need_subgraphs:
        # Split nodes into groups
        chunk_size = MAX_NODES_PER_GRAPH
        chunks = [nodes[i:i + chunk_size]
                  for i in range(0, len(nodes), chunk_size)]

        for idx, chunk in enumerate(chunks):
            group_label = f"Group {idx + 1}"
            lines.append(f"    subgraph {group_label}")
            for node in chunk:
                nid = node.get("id", "")
                label = node.get("label", nid)
                shape = node.get("shape", "rect")
                left, right = shape_map.get(shape, ("[", "]"))
                lines.append(f"        {nid}{left}{label}{right}")
            lines.append("    end")
    else:
        for node in nodes:
            nid = node.get("id", "")
            label = node.get("label", nid)
            shape = node.get("shape", "rect")
            left, right = shape_map.get(shape, ("[", "]"))
            lines.append(f"    {nid}{left}{label}{right}")

    for edge in edges:
        src = edge.get("from", "")
        tgt = edge.get("to", "")
        label = edge.get("label", "")
        style = edge.get("style", "-->")

        # Validate style
        valid_styles = {"-->", "---", "-.->", "==>", "-.->", "<-->", "---"}
        if style not in valid_styles:
            style = "-->"

        if label:
            lines.append(f"    {src} {style}|{label}| {tgt}")
        else:
            lines.append(f"    {src} {style} {tgt}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for knowledge_graph."""
    parser = argparse.ArgumentParser(
        description="Mermaid concept graph generator for paper knowledge bases"
    )
    parser.add_argument("--notes-dir", type=str, required=True,
                        help="Directory containing Obsidian note files")
    parser.add_argument("--mode", type=str,
                        choices=["concepts", "evolution", "ecosystem", "custom"],
                        default="concepts",
                        help="Graph generation mode")
    parser.add_argument("--method-name", type=str, default="",
                        help="Method name (for evolution mode)")
    parser.add_argument("--output", type=str, default="",
                        help="Output file path (prints to stdout if omitted)")

    args = parser.parse_args()

    output_data: dict[str, Any] = {"success": False}

    try:
        concepts = extract_concepts(args.notes_dir)

        # Also build a minimal notes list from file metadata
        notes: list[dict] = []
        notes_path = Path(args.notes_dir)
        for f in notes_path.rglob("*.md"):
            try:
                text = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            fm = _parse_frontmatter(text)
            notes.append({
                "title": fm.get("title", f.stem),
                "year": fm.get("year", 0),
                "methods": fm.get("methods", []),
                "tools": fm.get("tools", []),
                "keywords": fm.get("keywords", []),
            })

        if args.mode == "concepts":
            graph_code = build_concept_graph(concepts, notes)
            output_data["mermaid"] = graph_code
            output_data["concepts_count"] = len(concepts)

        elif args.mode == "evolution":
            if not args.method_name:
                output_data["error"] = "--method-name is required for evolution mode"
                print(json.dumps(output_data, ensure_ascii=False, indent=2))
                sys.exit(1)
            graph_code = build_method_evolution(args.method_name, notes)
            output_data["mermaid"] = graph_code

        elif args.mode == "ecosystem":
            graph_code = build_tool_ecosystem(notes)
            output_data["mermaid"] = graph_code

        elif args.mode == "custom":
            # Output extracted concepts for external graph building
            output_data["concepts"] = concepts
            output_data["notes"] = [
                {"title": n.get("title", ""), "year": n.get("year", 0)}
                for n in notes
            ]

        output_data["success"] = True

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            # Write mermaid code if present, otherwise full JSON
            if "mermaid" in output_data:
                mermaid_block = f"```mermaid\n{output_data['mermaid']}\n```"
                out_path.write_text(mermaid_block, encoding="utf-8")
            else:
                out_path.write_text(
                    json.dumps(output_data, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
            output_data["output_path"] = str(out_path)

    except Exception as exc:
        output_data["success"] = False
        output_data["error"] = str(exc)

    print(json.dumps(output_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
