---
name: validate-artifacts
description: Verifies that pipeline artifacts (data/papers.json, data/analysis.json, docs/index.html) are complete and well-formed before proceeding to the next step or deploying. Use this skill before any deployment step.
---

## Validation

Run the validation script — it performs all artifact checks deterministically:

```bash
python3 scripts/validate_artifacts.py
```

Exit code `0` = all checks pass. Exit code `1` = one or more failures (details printed to stderr).

### Checks performed

**`data/papers.json`**: file exists, valid JSON array, required fields (`id`, `title`, `authors`, `published_date`, `abstract`, `pdf_link`, `categories`), date range within 4 days.

**`data/analysis.json`**: file exists, valid JSON array, same length as papers.json, all paper fields plus `tldr`/`keywords`/`relevance_score`, score is integer 0–10, keywords array ≤ 5, sorted by score descending.

**`docs/index.html`**: file exists, `<!DOCTYPE html>`, `<title>` element, today's UTC date, paper count matches analysis.json, footer text present.

## Failure Action

If the script exits with code 1, review the failure messages and halt. Do not deploy until exit code is 0.
