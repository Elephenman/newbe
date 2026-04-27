#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Obsidian paper note templates from DOI or PDF"""
import os, sys, re

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

TEMPLATES = {}

TEMPLATES["minimal"] = """---
title: "{title}"
authors: "{authors}"
doi: "{doi}"
year: "{year}"
tags: [paper, {keywords}]
---

# {title}

**Authors**: {authors}
**DOI**: {doi}
**Year**: {year}

## One-sentence summary
{one_sentence}

## Key findings
{key_findings}

## Relevance to my research
- 
"""

TEMPLATES["detailed"] = """---
title: "{title}"
authors: "{authors}"
doi: "{doi}"
year: "{year}"
journal: "{journal}"
tags: [paper, {keywords}, detailed]
---

# {title}

## Basic info
- **Authors**: {authors}
- **DOI**: {doi}
- **Journal**: {journal}
- **Year**: {year}

## Abstract
{abstract}

## Research question
{research_question}

## Method
{method}

## Key results
{key_results}

## Limitations
{limitations}

## My thoughts
- How does this paper inspire my research?
- Methods I can borrow?
- Pitfalls to avoid?

## Next steps
- [ ] Read full text
- [ ] Try to reproduce key experiments
- [ ] Cite in my paper
"""

TEMPLATES["meeting"] = """---
title: "{title}"
authors: "{authors}"
doi: "{doi}"
tags: [paper, group-meeting, {keywords}]
type: group_meeting_report
---

# Group Meeting: {title}

## 1. Paper info
- **Title**: {title}
- **Authors**: {authors}
- **Journal**: {journal} ({year})
- **DOI**: {doi}

## 2. Background & motivation
{background}

## 3. Core method
{method}

## 4. Key results (3-5)
{key_results}

## 5. Innovation
{innovation}

## 6. Limitations & improvements
{limitations}

## 7. Implications for our lab
- 
"""

def generate_note(input_source, template_type="minimal", auto_fill=True, vault_path=None):
    meta = {}
    
    if input_source.startswith('10.'):
        # DOI input -> CrossRef API
        try:
            import requests
            r = requests.get(f"https://api.crossref.org/works/{input_source}", timeout=10)
            data = r.json()["message"]
            meta["title"] = data.get("title",[""])[0]
            meta["authors"] = "; ".join([f"{a.get('given','')} {a.get('family','')}" for a in data.get("author",[])])
            meta["doi"] = input_source
            meta["journal"] = data.get("container-title",[""])[0]
            meta["year"] = str(data.get("published-print",{}).get("date-parts",[[0]])[0][0])
            meta["abstract"] = data.get("abstract", "")
        except:
            meta["doi"] = input_source
    elif input_source.endswith('.pdf'):
        # PDF input -> pdfplumber
        try:
            import pdfplumber
            with pdfplumber.open(input_source) as pdf:
                first_page = pdf.pages[0].extract_text() or ""
                meta["title"] = pdf.metadata.get("Title", first_page.split('\n')[0])
                meta["authors"] = pdf.metadata.get("Author", "")
                doi_match = re.search(r'(10\.\d{4,}/[^\s]+)', first_page)
                meta["doi"] = doi_match.group(1).rstrip('.') if doi_match else ""
                meta["abstract"] = first_page[:500]
        except:
            pass
    else:
        meta["title"] = input_source
    
    # Fill defaults
    for key in ["title","authors","doi","year","journal","abstract","keywords",
                 "one_sentence","key_findings","research_question","method","key_results",
                 "limitations","background","innovation"]:
        if key not in meta:
            meta[key] = ""
    
    meta["keywords"] = meta.get("keywords", "bioinformatics")
    template = TEMPLATES.get(template_type, TEMPLATES["minimal"])
    
    # Fill template
    note = template
    for key, val in meta.items():
        note = note.replace(f"{{{key}}}", val)
    
    # Save
    filename = (meta.get("title","untitled")[:50]).replace(' ','_').replace('/','_')
    out_path = os.path.join(vault_path or ".", f"{filename}.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(note)
    
    print(f"Obsidian note generated")
    print(f"  Template: {template_type}")
    print(f"  Output: {out_path}")
    title_display = meta.get('title','')[:60]
    print(f"  Title: {title_display}")

def main():
    print("="*50); print("  Obsidian Paper Note Generator"); print("="*50)
    inp = get_input("PDF path or DOI", "10.1038/nature12373")
    tt = get_input("Template type (minimal/detailed/meeting)", "minimal")
    af = get_input("Auto-fill metadata (yes/no)", "yes")
    vp = get_input("Obsidian vault path", ".")
    generate_note(inp, tt, af.lower() in ('yes','y'), vp)

if __name__ == "__main__":
    main()