#!/usr/bin/env python3
"""Merge scraped features into the main database with deduplication."""

import sys
import re
import yaml
from pathlib import Path


def normalize(text: str) -> set[str]:
    """Normalize text to a set of lowercase words for Jaccard comparison."""
    return set(re.sub(r"[^a-z0-9\s]", "", text.lower()).split())


def jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two word sets."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def merge(existing_path: str, scraped_path: str) -> None:
    existing_data = yaml.safe_load(Path(existing_path).read_text())
    scraped_data = yaml.safe_load(Path(scraped_path).read_text())

    existing_features = existing_data.get("features", [])
    scraped_features = scraped_data.get("features", [])

    # Build lookup indexes
    existing_ids = {f["id"] for f in existing_features}
    existing_urls = set()
    for f in existing_features:
        src = f.get("source", {})
        if isinstance(src, dict) and src.get("url"):
            existing_urls.add(src["url"])
    existing_titles = {f["id"]: normalize(f.get("title", "")) for f in existing_features}

    added = 0
    skipped_id = 0
    skipped_url = 0
    flagged = []

    for sf in scraped_features:
        sid = sf.get("id", "")

        # Layer 1: Exact ID match
        if sid in existing_ids:
            skipped_id += 1
            continue

        # Layer 2: Source URL match
        src = sf.get("source", {})
        if isinstance(src, dict) and src.get("url") in existing_urls:
            skipped_url += 1
            continue

        # Layer 3: Title similarity
        new_title_words = normalize(sf.get("title", ""))
        is_similar = False
        for eid, etitle_words in existing_titles.items():
            sim = jaccard(new_title_words, etitle_words)
            if sim > 0.7:
                flagged.append(
                    f"  SIMILAR ({sim:.2f}): '{sf.get('title')}' ~ existing '{eid}'"
                )
                is_similar = True
                break

        if is_similar:
            continue

        # Not a duplicate -- add it
        existing_features.append(sf)
        existing_ids.add(sid)
        if isinstance(src, dict) and src.get("url"):
            existing_urls.add(src["url"])
        existing_titles[sid] = new_title_words
        added += 1

    # Write updated database
    existing_data["features"] = existing_features
    Path(existing_path).write_text(
        yaml.dump(existing_data, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    )

    # Report
    print(f"Merge complete:")
    print(f"  Added: {added}")
    print(f"  Skipped (exact ID): {skipped_id}")
    print(f"  Skipped (URL match): {skipped_url}")
    print(f"  Flagged (title similarity): {len(flagged)}")
    if flagged:
        print("Flagged entries:")
        for f in flagged:
            print(f)

    total = len(existing_features)
    print(f"Total features in database: {total}")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: merge-scraped.py <existing-features.yaml> <scraped-features.yaml>", file=sys.stderr)
        sys.exit(1)

    existing_path = sys.argv[1]
    scraped_path = sys.argv[2]

    for p in (existing_path, scraped_path):
        if not Path(p).exists():
            print(f"ERROR: File not found: {p}", file=sys.stderr)
            sys.exit(1)

    merge(existing_path, scraped_path)


if __name__ == "__main__":
    main()
