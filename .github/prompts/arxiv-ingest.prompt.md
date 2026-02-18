# arXiv Ingest Instructions

These instructions guide the `arxiv-ingest` agent when fetching and normalizing paper data.

## Data Source

- Use only the official arXiv API (`http://export.arxiv.org/api/query`).
- Do not scrape the arXiv website HTML.
- Do not use any third-party arXiv wrapper libraries or APIs.

## Category Targeting

- Always use `search_query=cat:q-bio.QM` — do not broaden to other q-bio subcategories unless explicitly instructed.
- Cross-listed papers (those with `q-bio.QM` plus other categories) are valid and should be included.

## Date Filtering & Retention

- Retain papers with `published_date` within the last **3 days (73 hours)** from the time of execution (per the `/filter-date-range` skill, which includes a 1-hour buffer for arXiv submission lag).
- On each run, merge newly fetched papers with the existing `data/papers.json` (if present), deduplicate by arXiv `id`, and drop papers older than 3 days.
- This accumulation ensures the dashboard shows a rolling 3-day window of papers across runs.

## Output Quality

- Every paper in `data/papers.json` must have all 8 required fields: `id`, `title`, `authors`, `published_date`, `abstract`, `pdf_link`, `categories`, `affiliations`.
- Fields with missing data should be `null`, not omitted or set to empty string.
- `authors` must always be an array, even for single-author papers.
- `pdf_link` must always point to `https://arxiv.org/pdf/<id>` (use HTTPS).
- `affiliations` must always be an array. If the arXiv API provides no affiliation data, set to `["Unknown"]`.

## Logging

At the end of the ingest step, print a one-line summary:
```
[arxiv-ingest] Fetched N new papers, M total retained (3-day window) for YYYY-MM-DD UTC (range: <earliest_date> to <latest_date>)
```
