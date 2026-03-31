# claude-feature-scout

Claude Code plugin marketplace. Two skills: `/claude-tips` (project analysis + recommendations) and `/scrape-features` (web search for new features).

## Structure
- `plugins/claude-feature-scout/data/features.yaml` — feature database (141 entries)
- `plugins/claude-feature-scout/data/schema.yaml` — YAML schema
- `plugins/claude-feature-scout/data/sources.yaml` — tracked scraping sources
- `plugins/claude-feature-scout/skills/*/SKILL.md` — skill definitions
- `plugins/claude-feature-scout/scripts/validate-features.py` — schema validator

## Validation
```
python3 plugins/claude-feature-scout/scripts/validate-features.py plugins/claude-feature-scout/data/features.yaml
```
Always run validation before committing changes to features.yaml.

## Conventions
- Feature IDs: kebab-case, unique
- Commit messages: conventional commits (feat:, fix:, chore:, docs:)
- Every feature entry needs: id, title, description, category, tags, relevance_signals, difficulty, source, example, added_date, last_verified
- Push to main after validation passes
