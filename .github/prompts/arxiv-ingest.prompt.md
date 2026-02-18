# arXiv Ingest Instructions

These instructions guide the `arxiv-ingest` agent when fetching and normalizing paper data.

## Data Source

- Use only the official arXiv API (`http://export.arxiv.org/api/query`).
- Do not scrape the arXiv website HTML.
- Do not use any third-party arXiv wrapper libraries or APIs.

## Category Targeting

- Always use `search_query=cat:q-bio.QM` — do not broaden to other q-bio subcategories unless explicitly instructed.
- Cross-listed papers (those with `q-bio.QM` plus other categories) are valid and should be included.

## Date Filtering

- Only include papers with `published_date` within the last **25 hours** from the time of execution (per the `/filter-date-range` skill, which uses a 25-hour window to account for arXiv submission lag).
- Never include papers from previous runs; check the published date, not the arXiv submission date.

## Output Quality

- Every paper in `data/papers.json` must have all 7 required fields: `id`, `title`, `authors`, `published_date`, `abstract`, `pdf_link`, `categories`.
- Fields with missing data should be `null`, not omitted or set to empty string.
- `authors` must always be an array, even for single-author papers.
- `pdf_link` must always point to `https://arxiv.org/pdf/<id>` (use HTTPS).

## Logging

At the end of the ingest step, print a one-line summary:
```
[arxiv-ingest] Fetched N papers for YYYY-MM-DD UTC (range: <earliest_date> to <latest_date>)
```
