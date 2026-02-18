---
name: fetch-arxiv-papers
description: Queries the arXiv API for the latest q-bio.QM preprints sorted by submission date. Use this skill when retrieving new papers from arXiv.
---

## API Details

- **Base URL:** `http://export.arxiv.org/api/query`
- **Required parameters:**
  - `search_query=cat:q-bio.QM`
  - `sortBy=submittedDate`
  - `sortOrder=descending`
  - `start=0`
  - `max_results=100`

## Example Request

```bash
curl -s "http://export.arxiv.org/api/query?search_query=cat:q-bio.QM&sortBy=submittedDate&sortOrder=descending&start=0&max_results=100"
```

## Pagination

If the `<opensearch:totalResults>` value in the response exceeds `max_results`, repeat the request with `start` incremented by `max_results` until all results submitted in the last 24 hours have been retrieved.

## Response Format

The API returns Atom/XML. Pass the raw response to the `/parse-arxiv-response` skill for conversion to JSON.

## Rate Limiting

- arXiv requests a maximum of 3 requests per second.
- Add a 1-second delay between paginated requests.
- If a request fails with a 5xx error, retry once after 5 seconds before treating it as a failure.
