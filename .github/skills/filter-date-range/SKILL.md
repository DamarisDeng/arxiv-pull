---
name: filter-date-range
description: Filters a parsed arXiv JSON array to retain only papers submitted within the last 24 hours relative to the current UTC time. Use this skill after parse-arxiv-response to remove stale entries.
---

## Filtering Logic

1. Get the current UTC timestamp at the time of execution.
2. Compute the cutoff: `cutoff = now_utc - 24 hours`.
3. Keep only entries where `published_date >= cutoff`.
4. Return the filtered array (may be empty).

## Handling the arXiv Submission Lag

arXiv batches submissions and publishes them once daily. Papers submitted on day D typically appear with a `published_date` of day D+1 at 00:00 UTC. To avoid missing papers near the boundary:

- Use a **25-hour window** (`now_utc - 25 hours`) rather than exactly 24 hours.
- This provides a 1-hour buffer for submission lag without including papers more than a day old.

## Deduplication

If the same arXiv `id` appears more than once in the input array (can happen across paginated requests), keep only the first occurrence.

## Output

The filtered, deduplicated JSON array using the same schema as the input. Log the count of papers kept and count removed.
