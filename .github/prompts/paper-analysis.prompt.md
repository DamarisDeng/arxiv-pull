# Paper Analysis Instructions

These instructions guide the `paper-analyzer` agent when summarizing and ranking papers.

## TL;DR Summaries

- Every paper must have a `tldr` field — never leave it empty or null unless the abstract is genuinely missing.
- Maximum 30 words per TL;DR.
- Write for a computational biology audience: assume familiarity with standard methods (Bayesian inference, ODEs, ML) but not hyper-specific domain jargon.
- Vary sentence openers — do not start every TL;DR with "This paper" or "The authors."
- Follow the full guidelines in the `/summarize-abstract` skill.

## Keyword Extraction

- Extract 0–5 keywords per paper following the `/extract-keywords` skill priority order.
- Keywords must be **specific and named** — reject generic terms like "deep learning", "statistics", or "biology" as standalone keywords.
- Title-case all keywords.

## Relevance Scoring

Score each paper 0–10 using this rubric:

| Score | Meaning |
|-------|---------|
| 9–10 | Strong methodological contribution directly advancing computational/quantitative biology tools or theory |
| 7–8 | Clear computational method applied to a biological question with novel findings |
| 5–6 | Quantitative analysis with standard methods; incremental contribution |
| 3–4 | Primarily empirical/experimental; quantitative component is minor |
| 1–2 | Minimal quantitative content; descriptive or review-style |
| 0 | Misclassified or irrelevant |

- Be consistent: papers with similar abstracts should receive similar scores.
- Do not inflate scores; reserve 9–10 for genuinely novel methodological contributions.

## Sorting

- `data/analysis.json` must be sorted by `relevance_score` descending before writing.
- For ties, sort alphabetically by `title`.
