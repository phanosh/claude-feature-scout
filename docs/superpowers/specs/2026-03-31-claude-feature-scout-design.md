# claude-feature-scout Design Spec

**Date**: 2026-03-31
**Status**: Approved

## Problem

Claude Code has 100+ features, tips, and tricks spread across official docs, Twitter posts, and community knowledge. Users don't know what they're missing -- especially features that would be perfect for their specific project/workflow but that they've never heard of.

## Solution

An open-source Claude Code plugin (`claude-feature-scout`) that ships a `/claude-tips` skill. It analyzes the user's current project, matches against a curated feature database, and recommends the most relevant tips personalized to their workflow.

## Architecture

### Components

1. **Skill** (`skills/claude-tips/SKILL.md`) -- Main entry point, handles UX flow
2. **Feature Database** (`data/features.yaml`) -- Curated, schema-validated knowledge base
3. **Scraping Pipeline** (`.github/workflows/scrape-features.yml`) -- Weekly automated updates
4. **Validation Scripts** (`scripts/`) -- Schema validation and deduplication

### Repository Structure

```
claude-feature-scout/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── claude-tips/
│       ├── SKILL.md
│       └── analysis-prompt.md
├── data/
│   ├── features.yaml
│   ├── schema.yaml
│   └── sources.yaml
├── scripts/
│   ├── validate-features.py
│   └── merge-scraped.py
├── .github/workflows/
│   ├── scrape-features.yml
│   └── validate-pr.yml
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

## Feature Database Schema

```yaml
- id: "kebab-case-unique-id"
  title: "Human-readable title"
  description: |
    Multi-line description of the feature/tip.
  category: "workflow"  # workflow | configuration | automation | skills | integration | coding | navigation | remote | memory | performance
  tags: [lowercase, hyphenated, free-form]
  relevance_signals:
    files: ["glob-patterns"]        # If matched in project, tip is relevant
    frameworks: ["nextjs"]          # Detected from dependency files
    indicators: ["large_codebase"]  # Abstract project traits
    workflow_patterns: ["tdd"]      # Inferred from git/structure
  difficulty: "intermediate"        # beginner | intermediate | advanced
  source:
    author: "bcherny"
    url: "https://x.com/..."
    date: "2025-06-15"
  example: |
    Code or command example
  added_date: "2025-07-01"
  last_verified: "2025-12-01"
```

## UX Flow

### Phase 1: Project Detection
- Check for project signals: package.json, Cargo.toml, pyproject.toml, go.mod, .git, src/, CLAUDE.md, etc.
- If no project: ask user -- generic tips, full catalog, or specific project type?

### Phase 2: Project Analysis (when project detected)
Build a profile:
- **Language/Runtime**: From dependency files
- **Framework**: Detection matrix (next.config.* -> nextjs, manage.py+django -> django, etc.)
- **Structure**: Monorepo? Large codebase? Has tests? CI? Docker?
- **Workflow**: Git history patterns (conventional commits, branch strategy, commit frequency)
- **Current Claude Code Usage**: .claude/ dir, hooks, skills, CLAUDE.md presence

### Phase 3: Feature Matching
Score each feature:
- +3 for file pattern match
- +2 for framework match
- +1 for indicator match
- +1 for workflow pattern match
- -5 if feature already in use (detected in Phase 2)

Take top 10-15 by score.

### Phase 4: Presentation
Three tiers:
1. **Quick Wins** (3-5): Zero setup, use right now
2. **Power-Ups** (3-5): Needs config, high payoff
3. **Deep Cuts** (2-3): Advanced, stack-specific

Each item shows: title, personalized "why it matters for YOUR project", quick example, difficulty badge.

### Arguments Support
- `/claude-tips` -- personalized recommendations
- `/claude-tips hooks` -- search by topic
- `/claude-tips all` -- full catalog by category
- `/claude-tips new` -- recently added features
- `/claude-tips update` -- info about last database update

## Scraping Pipeline

### Schedule
Weekly (Monday 6am UTC) via GitHub Actions, plus manual trigger.

### How It Works
1. `claude -p` with WebSearch tool scrapes tracked Twitter accounts (@claudeai, @bcherny, @amorriscode) and docs changelog
2. Output: new features in YAML format
3. `validate-features.py` validates schema
4. `merge-scraped.py` deduplicates (3 layers: exact ID, title similarity Jaccard > 0.7, source URL)
5. Creates PR for human review

### Tracked Sources (`data/sources.yaml`)
```yaml
sources:
  - account: "claudeai"
    platform: "twitter"
    search_query: "from:claudeai claude code"
    last_scraped: "2026-03-31"
  - account: "bcherny"
    platform: "twitter"
    search_query: "from:bcherny claude code"
    last_scraped: "2026-03-31"
  - account: "amorriscode"
    platform: "twitter"
    search_query: "from:amorriscode claude"
    last_scraped: "2026-03-31"
  - name: "claude-code-docs"
    platform: "web"
    url: "https://docs.anthropic.com/en/docs/claude-code"
    last_scraped: "2026-03-31"
```

## Community Contributions

- Fork, add to features.yaml, run validate script, submit PR
- CI validates every PR touching features.yaml
- CONTRIBUTING.md with schema reference and examples
- GitHub Discussions for proposing features
- "Good first issue" labels for verification tasks

## Success Criteria

1. Plugin installs cleanly via marketplace
2. `/claude-tips` produces personalized, non-generic recommendations for at least 5 different project types
3. Features database has 100+ entries across all categories
4. Scraping pipeline runs weekly without manual intervention
5. At least 3 community PRs adding features within first month
