---
name: summarize-abstract
description: Generates a concise one-sentence TL;DR summary from a technical arXiv abstract. Use this skill when processing each paper in the paper-analyzer step.
---

## Task

Given a scientific abstract, produce a single plain-English sentence (≤ 30 words) that captures:
1. **What** the paper does or proposes
2. **How** (the key method or approach, if space allows)
3. **Why it matters** (the key result or contribution, if space allows)

## Guidelines

- Write for a computational biology audience — assume familiarity with terms like "statistical model," "network analysis," "ODE," "ML," but not highly domain-specific jargon.
- Prefer active voice: "The authors propose…" or "This paper introduces…"
- Do not start with "This paper" or "We" — vary the opening.
- Do not include paper title or author names in the TL;DR.
- If the abstract is fewer than 3 sentences or clearly lacks methodological content, write: `"Presents [topic] with limited methodological detail."`

## Examples

**Input abstract excerpt:** "We develop a stochastic differential equation model for transcriptional bursting in single cells and derive analytical expressions for the noise in mRNA copy numbers..."
**TL;DR:** `"Derives analytical noise expressions for transcriptional bursting using a stochastic SDE model of single-cell gene expression."`

**Input abstract excerpt:** "In this study, we analyze 500 patient genomes to identify SNPs associated with drug resistance..."
**TL;DR:** `"Identifies drug-resistance-associated SNPs from 500 patient genomes using genome-wide association analysis."`
