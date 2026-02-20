#!/usr/bin/env python3
"""Fetch, parse, filter, and merge arXiv q-bio.QM papers into data/papers.json.

Replaces the fetch-arxiv-papers, parse-arxiv-response, and filter-date-range
Copilot skills with a single deterministic script (stdlib only).
"""

import json
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

API_URL = "http://export.arxiv.org/api/query"
CATEGORY = "q-bio.QM"
MAX_PER_PAGE = 100
RETENTION_HOURS = 73  # 3 days + 1-hour buffer for arXiv submission lag
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "papers.json")

ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"

# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_page(start: int) -> str:
    params = (
        f"search_query=cat:{CATEGORY}"
        f"&sortBy=submittedDate&sortOrder=descending"
        f"&start={start}&max_results={MAX_PER_PAGE}"
    )
    url = f"{API_URL}?{params}"
    for attempt in range(2):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as exc:
            if attempt == 0:
                print(f"[fetch] Retry after error: {exc}", file=sys.stderr)
                time.sleep(5)
            else:
                raise
    return ""


def fetch_all_recent() -> str:
    """Fetch pages until we've covered all results or gone past retention window."""
    first_page = fetch_page(0)
    root = ET.fromstring(first_page)
    total = int(root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults") or "0")
    pages = [first_page]

    fetched = MAX_PER_PAGE
    while fetched < total:
        time.sleep(1)  # rate-limit
        pages.append(fetch_page(fetched))
        fetched += MAX_PER_PAGE

    return "\n".join(pages)

# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------

def parse_entries(xml_text: str) -> list[dict]:
    papers = []
    for page_xml in xml_text.split("\n"):
        if not page_xml.strip():
            continue
        try:
            root = ET.fromstring(page_xml)
        except ET.ParseError:
            continue
        for entry in root.findall(f"{{{ATOM_NS}}}entry"):
            paper = parse_entry(entry)
            if paper:
                papers.append(paper)
    return papers


def parse_entry(entry: ET.Element) -> dict | None:
    raw_id = entry.findtext(f"{{{ATOM_NS}}}id") or ""
    arxiv_id = raw_id.replace("http://arxiv.org/abs/", "").strip()
    if not arxiv_id:
        return None

    title = " ".join((entry.findtext(f"{{{ATOM_NS}}}title") or "").split())

    authors = []
    for author_el in entry.findall(f"{{{ATOM_NS}}}author"):
        name = author_el.findtext(f"{{{ATOM_NS}}}name")
        if name:
            authors.append(name.strip())

    published = entry.findtext(f"{{{ATOM_NS}}}published")

    abstract = " ".join((entry.findtext(f"{{{ATOM_NS}}}summary") or "").split())

    pdf_link = None
    for link_el in entry.findall(f"{{{ATOM_NS}}}link"):
        if link_el.get("title") == "pdf":
            pdf_link = link_el.get("href")
            break
    if not pdf_link:
        pdf_link = f"https://arxiv.org/pdf/{arxiv_id}"

    categories = []
    for cat_el in entry.findall(f"{{{ATOM_NS}}}category"):
        term = cat_el.get("term")
        if term:
            categories.append(term)

    return {
        "id": arxiv_id,
        "title": title or None,
        "authors": authors,
        "published_date": published,
        "abstract": abstract or None,
        "pdf_link": pdf_link,
        "categories": categories,
    }

# ---------------------------------------------------------------------------
# Filter & Merge
# ---------------------------------------------------------------------------

def load_existing(path: str) -> list[dict]:
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def merge_and_filter(existing: list[dict], new: list[dict]) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=RETENTION_HOURS)

    # New papers take precedence on duplicate IDs
    by_id: dict[str, dict] = {}
    for paper in existing:
        pid = paper.get("id")
        if pid:
            by_id[pid] = paper
    for paper in new:
        pid = paper.get("id")
        if pid:
            by_id[pid] = paper

    # Apply date filter
    result = []
    for paper in by_id.values():
        pub = paper.get("published_date")
        if not pub:
            continue
        try:
            dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
        except ValueError:
            continue
        if dt >= cutoff:
            result.append(paper)

    # Sort by published_date descending
    result.sort(key=lambda p: p.get("published_date", ""), reverse=True)
    return result

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    output_path = os.path.abspath(OUTPUT_PATH)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("[fetch_papers] Querying arXiv API...")
    raw_xml = fetch_all_recent()

    new_papers = parse_entries(raw_xml)
    print(f"[fetch_papers] Parsed {len(new_papers)} papers from API")

    existing = load_existing(output_path)
    print(f"[fetch_papers] Loaded {len(existing)} existing papers from {output_path}")

    merged = merge_and_filter(existing, new_papers)
    print(f"[fetch_papers] {len(merged)} papers retained after merge + 73h filter")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Compute date range for summary
    dates = [p["published_date"][:10] for p in merged if p.get("published_date")]
    earliest = min(dates) if dates else "N/A"
    latest = max(dates) if dates else "N/A"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(
        f"[arxiv-ingest] Fetched {len(new_papers)} new papers, "
        f"{len(merged)} total retained (3-day window) for {today} UTC "
        f"(range: {earliest} to {latest})"
    )


if __name__ == "__main__":
    main()
