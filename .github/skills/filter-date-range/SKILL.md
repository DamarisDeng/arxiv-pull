---
name: filter-date-range
description: Filters a parsed arXiv JSON array to retain only papers submitted within the last 24 hours relative to the current UTC time. Use this skill after parse-arxiv-response to remove stale entries.
---

## Filtering Logic

1. Get the current UTC timestamp at the time of execution.
2. Compute the cutoff: `cutoff = now_utc - 73 hours` (3 days + 1-hour buffer).
3. Keep only entries where `published_date >= cutoff`.
4. Return the filtered array (may be empty).

## Handling the arXiv Submission Lag

arXiv batches submissions and publishes them once daily. Papers submitted on day D typically appear with a `published_date` of day D+1 at 00:00 UTC. The 73-hour window (3 days + 1 hour) provides a buffer for this lag.

## Merge with Existing Data

Before filtering, merge newly fetched papers with the existing `data/papers.json` (if the file exists):

1. Load the existing `data/papers.json` array.
2. Concatenate newly fetched papers after the existing entries.
3. Deduplicate by arXiv `id` — when duplicates exist, keep the entry from the new fetch (it may have updated metadata).
4. Apply the 73-hour cutoff filter to the merged array.
5. Return the filtered, deduplicated array.

## Deduplication

If the same arXiv `id` appears more than once in the input array (can happen across paginated requests), keep only the first occurrence.

## Output

The filtered, deduplicated JSON array using the same schema as the input. This array represents the rolling 3-day window of papers. Log the count of papers kept, count removed, and count merged from previous data.
