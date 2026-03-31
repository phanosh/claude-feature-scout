# Contributing to claude-feature-scout

Thanks for helping grow the feature database! Every contribution makes Claude Code more discoverable for everyone.

## Adding a Feature

1. **Fork** this repo and create a branch
2. **Add your entry** to `data/features.yaml` following the schema below
3. **Validate** locally: `python scripts/validate-features.py data/features.yaml`
4. **Submit a PR** -- CI will validate automatically

### Entry Schema

```yaml
- id: "kebab-case-unique-id"
  title: "Concise, descriptive title"
  description: |
    1-3 sentences explaining what this feature does and why it's useful.
  category: "workflow"  # see categories below
  tags: [lowercase, relevant, tags]
  relevance_signals:
    files: ["glob-patterns"]         # Project files that make this tip relevant
    frameworks: ["nextjs"]           # Specific frameworks
    indicators: ["has_tests"]        # Project characteristics
    workflow_patterns: ["tdd"]       # Workflow styles
  difficulty: "beginner"             # beginner | intermediate | advanced
  source:
    author: "twitter-handle"         # or "anthropic-docs" or "community"
    url: "https://..."
    date: "2026-01-15"
  example: |
    Concrete code or command showing usage
  added_date: "2026-03-31"
  last_verified: "2026-03-31"
```

### Categories

| Category | Use for |
|---|---|
| `workflow` | Session management, worktrees, parallel work, scheduling, planning |
| `configuration` | CLAUDE.md, settings, permissions, model selection |
| `automation` | Hooks, GitHub Actions, CI/CD, scheduled tasks |
| `skills` | Custom skills, slash commands, plugins |
| `integration` | MCP servers, Chrome, Slack, desktop app, VS Code, JetBrains |
| `coding` | Code generation, TDD, debugging, refactoring, review |
| `navigation` | Codebase exploration, search, context management |
| `remote` | SSH, headless, mobile, Dispatch, Remote Control |
| `memory` | CLAUDE.md hierarchy, memory system, project context |
| `performance` | Model settings, compaction, context management, fast mode |

### Relevance Signals Guide

The `relevance_signals` field is what makes recommendations personalized. Think about: **"What kind of project would benefit from this tip?"**

- **files**: Use actual file patterns. `["package.json"]` for Node.js projects, `["Cargo.toml"]` for Rust, etc.
- **frameworks**: Use lowercase identifiers: `nextjs`, `django`, `fastapi`, `rails`, `spring`, etc.
- **indicators**: Choose from: `large_codebase`, `monorepo`, `has_tests`, `has_ci`, `uses_docker`, `has_claude_md`, `has_custom_skills`, `has_hooks`, `team_project`, `many_branches`
- **workflow_patterns**: Choose from: `tdd`, `feature_branches`, `trunk_based`, `conventional_commits`, `parallel_development`, `documentation_heavy`, `ci_cd_heavy`

Leave arrays empty `[]` if a signal doesn't apply. Features with no relevance signals are still searchable but won't appear in project-specific recommendations.

### Source Attribution

Every feature needs a source:
- **Twitter tip**: `author: "handle"`, `url: "https://x.com/..."`, `date: "YYYY-MM-DD"`
- **Official docs**: `author: "anthropic-docs"`, `url: "https://docs.anthropic.com/..."`, `date: "YYYY-MM-DD"`
- **Your own discovery**: `author: "community"`, `url: "https://github.com/your-handle"`, `date: "YYYY-MM-DD"`

### Tips for Good Entries

- **Be specific**: "Use `--model sonnet` for faster iteration on small tasks" beats "You can change models"
- **Include a real example**: Copy-pasteable commands or code snippets
- **Think about relevance**: Who would benefit most? Tag accordingly
- **Verify it works**: Set `last_verified` to today's date after testing

## Updating Existing Entries

- Fix typos, improve descriptions, update examples -- all welcome
- Update `last_verified` date when you confirm a feature still works
- If a feature has been removed from Claude Code, open an issue to discuss removal

## Reporting Issues

- Feature doesn't work anymore? Open an issue with the feature ID
- Wrong category or missing tags? Submit a PR
- Duplicate entries? Open an issue -- we'll merge them

## Development

```bash
# Validate the database
python scripts/validate-features.py data/features.yaml

# Test the merge/dedup script
python scripts/merge-scraped.py data/features.yaml /path/to/scraped.yaml

# Install the plugin locally for testing
claude --plugin-dir /path/to/claude-feature-scout
```

## Full Schema Reference

See `data/schema.yaml` for the complete field-by-field schema documentation.
