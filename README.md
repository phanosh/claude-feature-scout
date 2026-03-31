# claude-feature-scout

Discover Claude Code features you didn't know you needed -- personalized for YOUR project.

## What it does

- **Analyzes your project** -- detects frameworks, patterns, tooling, and current Claude Code usage
- **Matches against 130+ features** -- curated database of tips, tricks, and features from official docs, power users, and the community
- **Recommends what matters** -- personalized to your workflow, not generic advice

## Install

```bash
# From GitHub (recommended)
/plugin install claude-feature-scout@nicodemosvarnava/claude-feature-scout
```

Or for local development:
```bash
claude --plugin-dir /path/to/claude-feature-scout
```

## Usage

```bash
/claude-tips              # Personalized recommendations for your project
/claude-tips hooks        # Search for hook-related features
/claude-tips all          # Browse the full catalog by category
/claude-tips new          # See recently added features
/claude-tips testing      # Tips for your testing workflow
```

## Example Output

When you run `/claude-tips` in a Next.js project with tests and CI:

```
## Quick Wins
Features you can start using right now with zero setup.

### Use `--model sonnet` for faster iteration
Why for your project: Your Next.js project has frequent component changes --
switching to Sonnet for quick edits saves time without sacrificing quality.
Example: claude --model sonnet
Difficulty: beginner

### Compact context with /compact
Why for your project: Large React component trees can fill context fast.
Use /compact to summarize and reclaim space mid-session.
Example: /compact
Difficulty: beginner

## Power-Ups
Features worth the setup investment for your workflow.

### Git worktrees for parallel Claude sessions
Why for your project: With 15+ branches detected, you're doing parallel work.
Worktrees let you run separate Claude sessions per branch simultaneously.
Example: git worktree add ../my-app-feature feature-branch && cd ../my-app-feature && claude
Difficulty: intermediate

### Pre-commit hooks with PreToolUse
Why for your project: Your CI pipeline runs ESLint -- catch issues before
commit by adding a PreToolUse hook that validates code changes.
Difficulty: intermediate

## Deep Cuts
Advanced features particularly suited to your Next.js workflow.

### MCP server for database access
Why for your project: Connect Claude directly to your dev database via MCP
so it can query schema and data while debugging.
Difficulty: advanced
```

## How It Works

```
/claude-tips
    |
    v
Phase 1: Detect project (package.json, go.mod, CLAUDE.md, .git, etc.)
    |
    v
Phase 2: Build profile (language, framework, structure, git patterns, Claude usage)
    |
    v
Phase 3: Score 130+ features against your profile
    |
    v
Phase 4: Present top recommendations in 3 tiers
         (Quick Wins / Power-Ups / Deep Cuts)
```

The feature database updates weekly via a Claude Code scheduled agent (`/schedule weekly /scrape-features`) that searches for new tips from [@claudeai](https://x.com/claudeai), [@bcherny](https://x.com/bcherny), [@amorriscode](https://x.com/amorriscode), and official docs. No CI or API keys needed -- runs on your Max subscription.

## Feature Database

The database lives in `data/features.yaml` with 130+ entries across 10 categories:

| Category | Count | Examples |
|---|---|---|
| workflow | 26 | Worktrees, planning mode, batch commands |
| configuration | 13 | CLAUDE.md levels, model selection, permissions |
| automation | 15 | Hooks, GitHub Actions, scheduling |
| skills | 11 | Custom skills, slash commands, plugins |
| integration | 14 | MCP, Chrome, Slack, VS Code, JetBrains |
| coding | 33 | TDD, debugging, refactoring, code review |
| navigation | 4 | Codebase search, context management |
| remote | 6 | SSH, mobile, Dispatch, Remote Control |
| memory | 4 | Memory system, CLAUDE.md hierarchy |
| performance | 6 | Fast mode, compaction, effort settings |

## Contributing

We welcome community contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add features to the database.

Quick version:
1. Fork this repo
2. Add your entry to `data/features.yaml`
3. Run `python scripts/validate-features.py data/features.yaml`
4. Submit a PR

## Automated Updates

The feature database stays fresh via Claude Code's built-in `/schedule` feature -- no CI, no API keys, no extra cost on Max.

### Setup (one-time)

Run this in the claude-feature-scout repo directory:

```
/schedule weekly /scrape-features
```

This creates a scheduled agent that runs every week, searches Twitter/X and docs for new Claude Code tips, deduplicates against the existing database, and pushes updates directly.

### Manual scrape

You can also run the scraper anytime:

```
/scrape-features
```

### How it works

1. Claude Code uses WebSearch to find new tips from tracked accounts (@claudeai, @bcherny, @amorriscode) and official docs
2. Deduplicates against existing entries (by ID, source URL, and title similarity)
3. Validates new entries against the schema
4. Commits and pushes to the repo

## License

MIT
