# claude-feature-scout

The Claude team is shipping features faster than anyone can keep track of. New slash commands, hooks, integrations, workflow tricks -- every week there's something new buried in a tweet or changelog that could save you hours.

This plugin fixes that. It watches the firehose so you don't have to, then tells you exactly which features matter for **your** project.

## What it does

1. You run `/claude-tips` inside any project
2. It reads your codebase -- language, framework, test setup, CI, git patterns, existing Claude config
3. It checks its database of 130+ features and tells you what you're missing
4. Recommendations are specific to your project, not generic "did you know" lists

If you're not in a project directory, it asks what you're working on and gives you relevant tips anyway.

## Setup

Add the marketplace and install the plugin:

```bash
claude plugin marketplace add phanosh/claude-feature-scout
claude plugin install claude-feature-scout
```

Restart Claude Code. The `/claude-tips` and `/scrape-features` commands are now available in any project.

To update later:

```bash
claude plugin update claude-feature-scout
```

## Commands

| Command | What it does |
|---|---|
| `/claude-tips` | Analyze your project, recommend features you should be using |
| `/claude-tips hooks` | Search the database for a specific topic |
| `/claude-tips all` | Browse every feature, grouped by category |
| `/claude-tips new` | See what was recently added |

## Keeping it fresh

The database updates automatically. Set up a daily scrape with Claude Code's built-in scheduling:

```
/schedule daily /scrape-features
```

This runs a Claude agent that searches Twitter/X ([@claudeai](https://x.com/claudeai), [@bcherny](https://x.com/bcherny), [@amorriscode](https://x.com/amorriscode)) and the official docs for new features, deduplicates them, and pushes updates to the repo. Runs on your Max subscription -- no API keys, no CI, no extra cost.

You can also run `/scrape-features` manually anytime.

## What's in the database

130+ features across 10 categories, sourced from official docs, power users, and the community:

- **workflow** -- worktrees, planning mode, parallel sessions, batch commands
- **configuration** -- CLAUDE.md, model selection, permissions, settings
- **automation** -- hooks, GitHub Actions, CI/CD, scheduled agents
- **skills** -- custom skills, slash commands, plugins
- **integration** -- MCP servers, Chrome, Slack, VS Code, JetBrains
- **coding** -- TDD, debugging, refactoring, code review patterns
- **remote** -- SSH, mobile, Dispatch, Remote Control
- **performance** -- fast mode, context compaction, effort settings
- **memory** -- memory system, CLAUDE.md hierarchy
- **navigation** -- codebase search, context management

Every entry includes relevance signals (which project types benefit), difficulty level, a concrete example, and a source link.

## Contributing

Found a tip that's not in the database? Add it:

1. Fork this repo
2. Add your entry to `data/features.yaml` (see [CONTRIBUTING.md](CONTRIBUTING.md) for the schema)
3. Run `python scripts/validate-features.py data/features.yaml`
4. Open a PR

## License

MIT
