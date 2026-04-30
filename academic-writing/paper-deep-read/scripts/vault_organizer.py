#!/usr/bin/env python3
"""PaperVault directory manager for Obsidian paper-reading notes.

Classifies papers by domain, generates filenames, creates the vault directory
structure, places notes into the correct folder, and maintains MOC (Map of
Content) and Dataview index files.
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
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

DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "01-Bioinformatics": [
        "bioinformatics", "sequence alignment", "genome", "genomics",
        "transcriptomics", "proteomics", "metabolomics", "phylogenetics",
        "gene expression", "NGS", "next-generation sequencing", "ChIP-seq",
        "RNA-seq", "single-cell RNA", "scRNA-seq", "GWAS", "variant calling",
        "assembly", "annotation", "BLAST", "biopython", "bioconductor",
        "SRA", "GEO", "ENA", "UniProt", "Pfam", "GO term", "gene ontology",
        "pathway analysis", "enrichment analysis",
    ],
    "01-Biology": [
        "cell biology", "molecular biology", "developmental biology",
        "immunology", "neuroscience", "cancer biology", "stem cell",
        "CRISPR", "gene editing", "knockout", "knockdown", "overexpression",
        "in vivo", "in vitro", "animal model", "mouse model", "zebrafish",
        "drosophila", "C. elegans", "arabidopsis", "signaling pathway",
        "transcription factor", "epigenetics", "histone", "methylation",
        "acetylation", "apoptosis", "autophagy", "metabolism",
    ],
    "02-AI-ML": [
        "deep learning", "machine learning", "neural network", "transformer",
        "attention mechanism", "CNN", "RNN", "LSTM", "GAN", "diffusion",
        "reinforcement learning", "self-supervised", "contrastive learning",
        "NLP", "natural language processing", "computer vision",
        "large language model", "LLM", "foundation model", "fine-tuning",
        "transfer learning", "embedding", "representation learning",
        "graph neural network", "GNN", "autoencoder", "VAE",
        "protein structure prediction", "AlphaFold", "ESM", "RoseTTAFold",
        "drug discovery AI", "virtual screening", "QSAR", "molecular generation",
        "generative model", "BERT", "GPT",
    ],
    "03-Structural-Biology": [
        "X-ray crystallography", "cryo-EM", "cryo-electron microscopy",
        "NMR structure", "protein structure", "X-ray diffraction",
        "molecular dynamics", "MD simulation", "docking", "homology modeling",
        "SAXS", "small-angle X-ray", "FRET", "cross-linking mass spec",
        "EM map", "resolution", "R-factor", "Ramachandran",
        "secondary structure", "tertiary structure", "quaternary structure",
        "protein folding", "intrinsically disordered", "IDP",
    ],
}

JOURNAL_ABBREVIATIONS: dict[str, str] = {
    # Top journals kept as-is
    "Nature": "Nature",
    "Science": "Science",
    "Cell": "Cell",
    "Nature Genetics": "NatGenet",
    "Nature Methods": "NatMethods",
    "Nature Biotechnology": "NatBiotechnol",
    "Nature Communications": "NatCommun",
    "Nature Structural & Molecular Biology": "NatStructMolBiol",
    "Nature Machine Intelligence": "NatMachIntell",
    "Nature Chemical Biology": "NatChemBiol",
    "Nature Neuroscience": "NatNeurosci",
    "Nature Medicine": "NatMed",
    "Nature Physics": "NatPhys",
    "Nature Chemistry": "NatChem",
    # Bioinformatics / computational
    "Bioinformatics": "Bioinformatics",
    "BMC Bioinformatics": "BMCBioinformatics",
    "PLoS Computational Biology": "PLoSComputBiol",
    "Nucleic Acids Research": "NucleicAcidsRes",
    "Genome Research": "GenomeRes",
    "Genome Biology": "GenomeBiol",
    "PLOS ONE": "PLoSONE",
    "eLife": "eLife",
    # AI/ML
    "NeurIPS": "NeurIPS",
    "ICML": "ICML",
    "ICLR": "ICLR",
    "AAAI": "AAAI",
    "CVPR": "CVPR",
    "JMLR": "JMLR",
    "IEEE Transactions on Pattern Analysis and Machine Intelligence": "TPAMI",
    # Structural biology
    "Acta Crystallographica Section D": "ActaCrystD",
    "Journal of Molecular Biology": "JMolBiol",
    "Structure": "Structure",
    "Protein Science": "ProteinSci",
    "Proteins: Structure, Function, and Bioinformatics": "Proteins",
    # General
    "Proceedings of the National Academy of Sciences": "PNAS",
    "The EMBO Journal": "EMBOJ",
    "EMBO Reports": "EMBORep",
    "Journal of Biological Chemistry": "JBiolChem",
    "Molecular Cell": "MolCell",
    "Developmental Cell": "DevCell",
}

VAULT_SUBDOMAINS: dict[str, list[str]] = {
    "01-Bioinformatics": [
        "Genomics", "Transcriptomics", "Proteomics", "Metabolomics",
        "Sequence-Analysis", "Network-Analysis", "Single-Cell",
    ],
    "01-Biology": [
        "Cell-Biology", "Molecular-Biology", "Immunology", "Neuroscience",
        "Developmental-Biology", "Cancer-Biology", "Plant-Biology",
    ],
    "02-AI-ML": [
        "Deep-Learning", "NLP", "Computer-Vision", "Graph-Learning",
        "Reinforcement-Learning", "Generative-Models", "Protein-AI",
        "Drug-Discovery-AI",
    ],
    "03-Structural-Biology": [],
    "04-Other": [],
}

MOC_TEMPLATE = """# {domain} - Map of Content

> [!abstract] Overview
> Papers and notes related to {domain}.

## Papers

{{papers}}

## Methods

{{methods}}

## Tools

{{tools}}
"""

DATAVIEW_INDEX_TEMPLATE = """```dataview
TABLE title, year, journal, paper_type
FROM "{domain}"
SORT year DESC
```
"""


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def classify_domain(metadata: dict) -> str:
    """Determine the domain folder from keywords, journal, and methods.

    Uses keyword matching with priority rules. The domain with the highest
    match score wins. Ties are broken by the order defined in
    ``DOMAIN_KEYWORDS``.

    Parameters
    ----------
    metadata : dict
        Must contain at least ``keywords`` or ``journal``. May also
        include ``methods`` and ``domains``.

    Returns
    -------
    str
        Domain folder name, e.g. ``"01-Bioinformatics"``.
        Defaults to ``"04-Other"`` if no match is found.
    """
    # Collect searchable text fields
    search_fields: list[str] = []

    for field in ("keywords", "methods", "tools", "databases"):
        val = metadata.get(field, [])
        if isinstance(val, str):
            search_fields.append(val.lower())
        elif isinstance(val, list):
            search_fields.extend(v.lower() for v in val)

    journal = metadata.get("journal", "")
    if journal:
        search_fields.append(journal.lower())

    title = metadata.get("title", "")
    if title:
        search_fields.append(title.lower())

    search_text = " ".join(search_fields)

    # Score each domain
    scores: dict[str, int] = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in search_text)
        scores[domain] = score

    # Explicit domain override
    domains = metadata.get("domains", [])
    if isinstance(domains, str):
        domains = [domains]
    for d in domains:
        d_stripped = d.strip().lstrip("#")
        for domain_key in DOMAIN_KEYWORDS:
            if d_stripped.lower() in domain_key.lower():
                scores[domain_key] = scores.get(domain_key, 0) + 10

    best_domain = max(scores, key=scores.get)  # type: ignore[arg-type]
    if scores[best_domain] == 0:
        return "04-Other"

    return best_domain


def generate_note_filename(metadata: dict) -> str:
    """Create a note filename as ``{year}-{journal_abbrev}-{core_keyword}.md``.

    Parameters
    ----------
    metadata : dict
        Must contain ``year``, ``journal``, and ``title``.

    Returns
    -------
    str
        Sanitized filename with ``.md`` extension. The core keyword is
        extracted from the title and capped at 20 Chinese characters (or
        equivalent width).
    """
    year = str(metadata.get("year", "0000"))
    journal = metadata.get("journal", "Unknown")

    # Journal abbreviation
    abbrev = JOURNAL_ABBREVIATIONS.get(journal)
    if abbrev is None:
        # Generate a simple abbreviation: take first letters of major words
        words = re.split(r"[\s&]+", journal)
        abbrev = "".join(w[0].upper() for w in words if w and w[0].isupper())
        if len(abbrev) > 12:
            abbrev = abbrev[:12]
        if not abbrev:
            abbrev = "J"

    # Core keyword extraction from title
    title = metadata.get("title", "Untitled")
    core_keyword = _extract_core_keyword(title)

    # Compose filename
    filename = f"{year}-{abbrev}-{core_keyword}.md"
    filename = _sanitize_filename(filename)

    return filename


def _extract_core_keyword(title: str, max_chars: int = 20) -> str:
    """Extract a core keyword phrase from *title*, limited to *max_chars*.

    For titles with a colon, prefer the part before the colon. Stop words
    are removed. Chinese and English characters are both handled.
    """
    # Prefer text before colon if present
    if ":" in title or "：" in title:
        parts = re.split(r"[:：]", title, maxsplit=1)
        segment = parts[0].strip()
    else:
        segment = title.strip()

    # Remove common stop words (English)
    stop_words = {
        "a", "an", "the", "of", "in", "for", "and", "or", "to", "with",
        "on", "by", "from", "at", "via", "using", "based", "through",
        "towards", "toward", "novel", "new", "efficient",
    }
    tokens = segment.split()
    filtered = [t for t in tokens if t.lower() not in stop_words]
    result = " ".join(filtered)

    # Trim to max_chars (counting CJK chars as 1 each)
    if len(result) > max_chars:
        result = result[:max_chars]

    return result.strip()


def _sanitize_filename(name: str) -> str:
    """Remove or replace characters illegal in filenames on Windows."""
    # Remove characters not allowed in Windows filenames
    illegal = r'[<>:"/\\|?*]'
    name = re.sub(illegal, "", name)
    # Replace multiple spaces/dashes
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"-{2,}", "-", name)
    # Strip leading/trailing spaces and dots
    name = name.strip(" .")
    return name


def create_vault_structure(vault_root: str) -> None:
    """Create the full PaperVault directory tree.

    Structure::

        <vault_root>/
        00-Inbox/
        01-Bioinformatics/{subdomains}
        01-Biology/{subdomains}
        02-AI-ML/{subdomains}
        03-Structural-Biology/
        04-Other/
        Templates/
        MOC/
        Resources/

    Also creates MOC index files for each domain.

    Parameters
    ----------
    vault_root : str
        Root path of the vault.
    """
    root = Path(vault_root)

    # Top-level directories
    top_dirs = [
        "00-Inbox", "01-Bioinformatics", "01-Biology", "02-AI-ML",
        "03-Structural-Biology", "04-Other", "Templates", "MOC", "Resources",
    ]

    for d in top_dirs:
        (root / d).mkdir(parents=True, exist_ok=True)

    # Subdomains
    for domain, subdomains in VAULT_SUBDOMAINS.items():
        for sub in subdomains:
            (root / domain / sub).mkdir(parents=True, exist_ok=True)

    # MOC index files
    for domain in list(VAULT_SUBDOMAINS.keys()) + ["00-Inbox", "04-Other"]:
        moc_path = root / "MOC" / f"{domain}-MOC.md"
        if not moc_path.exists():
            content = MOC_TEMPLATE.format(domain=domain)
            moc_path.write_text(content, encoding="utf-8")

    # Dataview index
    create_dataview_index(vault_root)


def place_note(note_path: str, vault_root: str, domain: str,
               source_pdf: str = "") -> str:
    """Move a note to the correct domain folder within the vault.

    Creates an ``images/`` subfolder alongside the placed note, copies the
    original PDF to the same directory, and updates relative image paths in
    the note content from ``images/`` to the new location.

    Parameters
    ----------
    note_path : str
        Current path of the note file.
    vault_root : str
        Root path of the vault.
    domain : str
        Domain folder name (e.g. ``"01-Bioinformatics"``).
    source_pdf : str
        Path to the original PDF file. If provided, the PDF is copied
        alongside the placed note so that the ``[[filename.pdf]]`` wikilink
        in the note can be resolved by Obsidian.

    Returns
    -------
    str
        Final path of the placed note.
    """
    src = Path(note_path)
    vault = Path(vault_root)
    dest_dir = vault / domain
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest = dest_dir / src.name

    # If source and dest are the same, nothing to do
    if src.resolve() == dest.resolve():
        return str(dest)

    # Copy file (do not move to avoid data loss across drives on Windows)
    shutil.copy2(str(src), str(dest))

    # Create images/ subfolder alongside note
    images_dir = dest_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Copy associated images if source has an images/ dir
    src_images = src.parent / "images"
    if src_images.exists() and src_images.is_dir():
        for img in src_images.iterdir():
            if img.is_file():
                shutil.copy2(str(img), str(images_dir / img.name))

    # Copy original PDF to the note's directory so the wikilink resolves
    if source_pdf:
        pdf_src = Path(source_pdf)
        if pdf_src.exists() and pdf_src.is_file():
            pdf_dest = dest_dir / pdf_src.name
            if not pdf_dest.exists():
                shutil.copy2(str(pdf_src), str(pdf_dest))

    # Update relative image paths in the note content
    content = dest.read_text(encoding="utf-8")
    updated = _update_image_paths(content)
    if updated != content:
        dest.write_text(updated, encoding="utf-8")

    return str(dest)


def _update_image_paths(content: str) -> str:
    """Update image references in note content to Obsidian wikilink syntax."""
    # Convert markdown image syntax to Obsidian ![[]] if needed
    # ![alt](images/filename.png) -> ![[filename.png]]
    pattern = r"!\[([^\]]*)\]\(images/([^)]+)\)"
    replacement = r"![[\2]]"
    return re.sub(pattern, replacement, content)


def update_moc(vault_root: str, domain: str,
               new_note_title: str) -> None:
    """Update a domain's Map of Content file with a new note link.

    Parameters
    ----------
    vault_root : str
        Root path of the vault.
    domain : str
        Domain folder name.
    new_note_title : str
        Title of the new note (used as the wikilink target).
    """
    vault = Path(vault_root)
    moc_path = vault / "MOC" / f"{domain}-MOC.md"

    if not moc_path.exists():
        # Create MOC file if missing
        moc_path.parent.mkdir(parents=True, exist_ok=True)
        content = MOC_TEMPLATE.format(domain=domain)
        moc_path.write_text(content, encoding="utf-8")

    content = moc_path.read_text(encoding="utf-8")
    link = f"- [[{new_note_title}]]"

    # Avoid duplicates
    if f"[[{new_note_title}]]" in content:
        return

    # Insert under ## Papers section
    papers_marker = "## Papers"
    if papers_marker in content:
        lines = content.split("\n")
        new_lines: list[str] = []
        inserted = False
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip() == papers_marker and not inserted:
                # Insert after the heading (and any blank line after it)
                new_lines.append(link)
                inserted = True
        content = "\n".join(new_lines)
    else:
        # Append at the end
        content += f"\n{link}\n"

    moc_path.write_text(content, encoding="utf-8")


def create_dataview_index(vault_root: str) -> None:
    """Create or update Dataview index files for the vault.

    Generates one Dataview query file per domain under the ``MOC/`` folder.

    Parameters
    ----------
    vault_root : str
        Root path of the vault.
    """
    vault = Path(vault_root)
    moc_dir = vault / "MOC"
    moc_dir.mkdir(parents=True, exist_ok=True)

    domains = list(VAULT_SUBDOMAINS.keys()) + ["00-Inbox", "04-Other"]

    for domain in domains:
        index_path = moc_dir / f"{domain}-Index.md"
        content = DATAVIEW_INDEX_TEMPLATE.format(domain=domain)
        index_path.write_text(content, encoding="utf-8")

    # Vault-wide index
    vault_index = moc_dir / "Vault-Index.md"
    vault_content = """```dataview
TABLE title, year, journal, paper_type, domains
FROM "01-Bioinformatics" OR "01-Biology" OR "02-AI-ML" OR "03-Structural-Biology" OR "04-Other"
SORT year DESC
```
"""
    vault_index.write_text(vault_content, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for vault_organizer."""
    parser = argparse.ArgumentParser(
        description="PaperVault directory manager"
    )
    parser.add_argument("--vault-root", type=str, required=True,
                        help="Root path of the PaperVault")
    parser.add_argument("--note", type=str,
                        help="Path to note file to place")
    parser.add_argument("--metadata", type=str,
                        help="Path to JSON file with paper metadata")
    parser.add_argument("--init-vault", action="store_true",
                        help="Initialize vault directory structure")
    parser.add_argument("--update-moc", action="store_true",
                        help="Update MOC after placing a note")
    parser.add_argument("--source-pdf", type=str, default="",
                        help="Path to original PDF to copy alongside note")

    args = parser.parse_args()

    output_data: dict[str, Any] = {"success": False}

    try:
        if args.init_vault:
            create_vault_structure(args.vault_root)
            output_data["success"] = True
            output_data["message"] = f"Vault structure created at {args.vault_root}"

        elif args.note and args.metadata:
            metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
            domain = classify_domain(metadata)
            final_path = place_note(
                args.note, args.vault_root, domain,
                source_pdf=args.source_pdf
            )
            filename = Path(final_path).stem
            title = metadata.get("title", filename)

            if args.update_moc:
                update_moc(args.vault_root, domain, title)

            output_data["success"] = True
            output_data["domain"] = domain
            output_data["final_path"] = final_path
            output_data["filename"] = generate_note_filename(metadata)

        else:
            parser.print_help()
            sys.exit(0)

    except Exception as exc:
        output_data["success"] = False
        output_data["error"] = str(exc)

    print(json.dumps(output_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
