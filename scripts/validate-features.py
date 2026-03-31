#!/usr/bin/env python3
"""Validate the features.yaml database against the schema."""

import sys
import re
import yaml
from pathlib import Path

ALLOWED_CATEGORIES = {
    "workflow", "configuration", "automation", "skills", "integration",
    "coding", "navigation", "remote", "memory", "performance",
}

ALLOWED_DIFFICULTIES = {"beginner", "intermediate", "advanced"}

ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(path: str) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(Path(path).read_text())

    if not isinstance(data, dict) or "features" not in data:
        return ["Root must be a mapping with a 'features' key"]

    features = data["features"]
    if not isinstance(features, list):
        return ["'features' must be a list"]

    seen_ids: set[str] = set()

    for i, f in enumerate(features):
        prefix = f"features[{i}]"

        if not isinstance(f, dict):
            errors.append(f"{prefix}: must be a mapping")
            continue

        # Required string fields
        for field in ("id", "title", "description", "category", "difficulty"):
            if field not in f:
                errors.append(f"{prefix}: missing required field '{field}'")
            elif not isinstance(f[field], str):
                errors.append(f"{prefix}.{field}: must be a string")

        fid = f.get("id", "")

        # ID format
        if fid and not ID_PATTERN.match(fid):
            errors.append(f"{prefix}.id: '{fid}' is not valid kebab-case")

        # Unique ID
        if fid in seen_ids:
            errors.append(f"{prefix}.id: duplicate id '{fid}'")
        seen_ids.add(fid)

        # Category
        cat = f.get("category", "")
        if cat and cat not in ALLOWED_CATEGORIES:
            errors.append(f"{prefix}.category: '{cat}' not in {ALLOWED_CATEGORIES}")

        # Difficulty
        diff = f.get("difficulty", "")
        if diff and diff not in ALLOWED_DIFFICULTIES:
            errors.append(f"{prefix}.difficulty: '{diff}' not in {ALLOWED_DIFFICULTIES}")

        # Tags
        tags = f.get("tags", [])
        if not isinstance(tags, list):
            errors.append(f"{prefix}.tags: must be a list")
        elif any(not isinstance(t, str) for t in tags):
            errors.append(f"{prefix}.tags: all items must be strings")

        # Relevance signals
        rs = f.get("relevance_signals")
        if rs is not None:
            if not isinstance(rs, dict):
                errors.append(f"{prefix}.relevance_signals: must be a mapping")
            else:
                for key in ("files", "frameworks", "indicators", "workflow_patterns"):
                    val = rs.get(key)
                    if val is not None and not isinstance(val, list):
                        errors.append(f"{prefix}.relevance_signals.{key}: must be a list")

        # Source
        src = f.get("source")
        if src is not None:
            if not isinstance(src, dict):
                errors.append(f"{prefix}.source: must be a mapping")

        # Date fields
        for date_field in ("added_date", "last_verified"):
            val = f.get(date_field, "")
            if val and isinstance(val, str) and not DATE_PATTERN.match(val):
                errors.append(f"{prefix}.{date_field}: '{val}' is not YYYY-MM-DD format")

        # Example
        if "example" not in f:
            errors.append(f"{prefix}: missing 'example' field")

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        path = str(Path(__file__).resolve().parent.parent / "data" / "features.yaml")
    else:
        path = sys.argv[1]

    if not Path(path).exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    errors = validate(path)

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} errors):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    else:
        data = yaml.safe_load(Path(path).read_text())
        count = len(data.get("features", []))
        print(f"OK: {count} features validated successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
