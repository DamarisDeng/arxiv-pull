# arXiv Ingest Instructions

These instructions guide the `arxiv-ingest` agent when fetching and normalizing paper data.

## Execution

Run the ingest script — it handles API calls, XML parsing, date filtering, merging, and deduplication:

```bash
python3 scripts/fetch_papers.py
```

The script uses only the official arXiv API (`http://export.arxiv.org/api/query`) with `search_query=cat:q-bio.QM`, includes pagination and rate limiting, and applies a 73-hour retention window (3 days + 1-hour buffer for arXiv submission lag).

## Output Quality

- Every paper in `data/papers.json` must have all 7 required fields: `id`, `title`, `authors`, `published_date`, `abstract`, `pdf_link`, `categories`.
- Fields with missing data should be `null`, not omitted or set to empty string.
- `authors` must always be an array, even for single-author papers.
- `pdf_link` must always point to `https://arxiv.org/pdf/<id>` (use HTTPS).

## Logging

The script prints a one-line summary:
```
[arxiv-ingest] Fetched N new papers, M total retained (3-day window) for YYYY-MM-DD UTC (range: <earliest_date> to <latest_date>)
```
