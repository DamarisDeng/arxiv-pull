---
name: parse-arxiv-response
description: Converts the raw Atom/XML response from the arXiv API into a structured JSON array. Use this skill after fetch-arxiv-papers returns a raw API response.
---

## Input

Raw Atom/XML string from the arXiv API (as returned by the `/fetch-arxiv-papers` skill).

## Parsing Rules

For each `<entry>` element in the Atom feed, extract the following fields:

| JSON field | XML source | Notes |
|------------|-----------|-------|
| `id` | `<id>` | Strip the `http://arxiv.org/abs/` prefix; keep only the arXiv ID (e.g., `2401.12345`) |
| `title` | `<title>` | Collapse whitespace; remove newlines |
| `authors` | `<author><name>` | Collect all author names into an array |
| `published_date` | `<published>` | ISO 8601 format; keep as-is |
| `abstract` | `<summary>` | Collapse whitespace; remove leading/trailing whitespace |
| `pdf_link` | `<link rel="related" title="pdf">` href | Use the direct PDF link |
| `categories` | `<category>` term attributes | Collect all category terms into an array |
| `affiliations` | `<author><arxiv:affiliation>` | Collect unique affiliations across all authors into an array. If no `<arxiv:affiliation>` elements exist, set to `["Unknown"]` |

## Output

A JSON array of objects matching the schema above. Example single entry:

```json
{
  "id": "2401.12345",
  "title": "A Quantitative Model of Cell Signaling",
  "authors": ["Jane Smith", "John Doe"],
  "published_date": "2024-01-15T00:00:00Z",
  "abstract": "We present a novel quantitative model...",
  "pdf_link": "https://arxiv.org/pdf/2401.12345",
  "categories": ["q-bio.QM", "q-bio.CB"],
  "affiliations": ["MIT", "Stanford University"]
}
```

## Error Handling

- If an `<entry>` is missing a required field, include the entry with that field set to `null`.
- Do not silently drop entries; always include all entries from the feed.
