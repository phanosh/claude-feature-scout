---
name: scrape-features
description: >
  Scrape Twitter/X and docs for new Claude Code features, deduplicate against
  the existing database, and commit updates. Use when you want to update the
  feature database with recent tips. MANUAL TRIGGER ONLY: /scrape-features
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# Feature Scraper

You are the feature scraper for claude-feature-scout. Your job is to find NEW Claude Code features and tips, deduplicate them, and update the database.

## Step 1: Read Current State

Read the current feature database and sources config:

```
Read ${SKILL_DIR}/../../data/features.yaml
Read ${SKILL_DIR}/../../data/sources.yaml
```

Note the total feature count and the `last_scraped` dates.

## Step 2: Search for New Features

Use WebSearch to check each tracked source for new Claude Code content. Run these searches:

1. `"claudeai" claude code new feature` (filter for recent results)
2. `"bcherny" claude code tip` (filter for recent results)
3. `"amorriscode" claude code` (filter for recent results)
4. `claude code changelog site:docs.anthropic.com` (recent updates)
5. `claude code new feature announcement` (general recent coverage)

For each search result that describes a Claude Code feature or tip:
- Check if it already exists in the database (match by title similarity or source URL)
- If it's genuinely new, note it down

## Step 3: Format New Features

For each new feature found, create an entry following the schema:

```yaml
- id: "kebab-case-unique-id"
  title: "Human-readable title"
  description: |
    1-3 sentence description.
  category: "workflow|configuration|automation|skills|integration|coding|navigation|remote|memory|performance"
  tags: [relevant, lowercase, tags]
  relevance_signals:
    files: ["glob-patterns-if-applicable"]
    frameworks: ["framework-names-if-applicable"]
    indicators: ["project-trait-if-applicable"]
    workflow_patterns: ["workflow-if-applicable"]
  difficulty: "beginner|intermediate|advanced"
  source:
    author: "twitter-handle-or-anthropic-docs"
    url: "source-url"
    date: "YYYY-MM-DD"
  example: |
    Concrete code or command example
  added_date: "YYYY-MM-DD"
  last_verified: "YYYY-MM-DD"
```

## Step 4: Update the Database

If new features were found:

1. Append the new entries to the features.yaml file (at `${SKILL_DIR}/../../data/features.yaml`) under the appropriate category sections
2. Update the feature count in the file header comment
3. Update `last_scraped` dates in the sources.yaml file (at `${SKILL_DIR}/../../data/sources.yaml`) to today

## Step 5: Validate

Run the validation script from the plugin root:
```bash
python3 ${SKILL_DIR}/../../scripts/validate-features.py ${SKILL_DIR}/../../data/features.yaml
```

If validation fails, fix the issues and re-run.

## Step 6: Commit and Push

If new features were added:
```bash
git add ${SKILL_DIR}/../../data/features.yaml ${SKILL_DIR}/../../data/sources.yaml
git commit -m "chore: update feature database (N new features from scrape)"
git push
```

## Step 7: Report

Summarize what was found:
- How many new features added
- Which sources they came from
- Any notable new capabilities discovered

If nothing new was found, say so -- that's fine, not every week has new features.

## Rules

- Only include genuinely NEW Claude Code features or tips
- Do NOT include general AI tips, Claude API-only features, or non-Claude-Code content
- Every entry must have a concrete, actionable example
- Deduplicate carefully -- check title similarity, not just exact matches
- When in doubt about whether something is new, skip it (false negatives are better than duplicates)
