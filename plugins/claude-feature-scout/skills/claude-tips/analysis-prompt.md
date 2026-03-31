# Project Analysis Reference

Reference tables for the claude-tips skill's project detection and analysis phases.

---

## Language & Runtime Detection Matrix

| Manifest File | Language Tag | Additional Check |
|---|---|---|
| `package.json` | `node` | If `tsconfig.json` exists or deps include `typescript` -> add `typescript` |
| `Cargo.toml` | `rust` | - |
| `pyproject.toml` | `python` | - |
| `requirements.txt` | `python` | - |
| `setup.py` | `python` | - |
| `go.mod` | `go` | - |
| `Gemfile` | `ruby` | - |
| `pom.xml` | `java` | - |
| `build.gradle` | `java` | - |
| `*.csproj` | `dotnet` | - |
| `*.sln` | `dotnet` | - |

---

## Framework Detection Matrix

### JavaScript / TypeScript Frameworks

| Dependency in package.json | Framework Tag | Notes |
|---|---|---|
| `next` | `nextjs` | Check both `dependencies` and `devDependencies` |
| `react` (without `next`) | `react` | Only tag as `react` if `next` is not present |
| `vue` | `vue` | Includes Vue 2 and Vue 3 |
| `@angular/core` | `angular` | Look for `@angular/` prefix |
| `svelte` | `svelte` | Also check for `@sveltejs/kit` |
| `express` | `express` | Server-side framework |

### Python Frameworks

| Dependency in pyproject.toml / requirements.txt | Framework Tag | Notes |
|---|---|---|
| `django` | `django` | Also check for `Django` (case-insensitive) |
| `fastapi` | `fastapi` | - |
| `flask` | `flask` | Also check for `Flask` (case-insensitive) |

### Ruby Frameworks

| Dependency in Gemfile | Framework Tag | Notes |
|---|---|---|
| `rails` | `rails` | Look for `gem 'rails'` or `gem "rails"` |

### Go Frameworks

| Dependency in go.mod | Framework Tag | Notes |
|---|---|---|
| `github.com/gin-gonic/gin` | `gin` | Match on path containing `gin` |
| `github.com/gofiber/fiber` | `fiber` | Match on path containing `fiber` |

---

## Project Structure Indicator Detection Commands

| Indicator | Detection Method | Command / Check |
|---|---|---|
| `monorepo` | Glob + Read | `Glob("**/package.json")` returns >1 result, OR root `package.json` contains `"workspaces"` |
| `large_codebase` | Bash | `find . -type f \| wc -l` returns value > 500 |
| `has_tests` | Glob | Any of: `Glob("test/**")`, `Glob("__tests__/**")`, `Glob("**/*_test.*")`, `Glob("**/*.spec.*")` return results |
| `has_ci` | Glob | `Glob(".github/workflows/*")` or `Glob(".gitlab-ci.yml")` return results |
| `uses_docker` | Glob | `Glob("Dockerfile")` or `Glob("docker-compose.yml")` or `Glob("docker-compose.yaml")` return results |
| `uses_claude_code` | Glob | `Glob(".claude/**")` returns results |
| `has_custom_skills` | Glob | `Glob(".claude/skills/**")` returns results |
| `has_hooks` | Read + Grep | Read `.claude/settings.json` and check if `"hooks"` key exists |
| `has_claude_md` | Glob | `Glob("CLAUDE.md")` returns results |
| `many_branches` | Bash | `git branch -a \| wc -l` returns value > 10 |

---

## Workflow Pattern Detection

All workflow detection requires an active git repository.

| Pattern | Detection Method | Command |
|---|---|---|
| `conventional_commits` | Bash + pattern match | `git log --oneline -20` then check if messages match `^(feat\|fix\|chore\|docs\|style\|refactor\|perf\|test\|build\|ci):` |
| `feature_branches` | Bash + pattern match | `git branch -a` then check for branches matching `feature/`, `fix/`, `release/` prefixes |
| `trunk_based` | Bash + count | `git branch -a \| wc -l` returns <= 3 AND most recent commits are on main/master |
| `colocated_tests` | Glob | Test files (`.test.*`, `.spec.*`) found in same directories as source files (not in separate `test/` directory) |
| `active_development` | Bash | `git log --oneline --since="1 day ago" \| wc -l` returns > 5 |

---

## Current Claude Code Usage Inventory

Check these paths to determine what the user already has configured:

| Path | What to Check | Purpose |
|---|---|---|
| `.claude/` | Directory exists and list contents | Determines if user is a Claude Code user at all |
| `.claude/settings.json` | Read and parse for `hooks` key | Determines if user has hooks configured |
| `.claude/settings.json` | Read and parse for `permissions` key | Determines permission configuration |
| `.claude/skills/` | List directory contents | Determines if user has custom skills |
| `CLAUDE.md` | Read contents | Determines project-level instructions |
| `.claude/CLAUDE.md` | Read contents | Determines Claude-specific instructions |

---

## Feature Scoring Algorithm

```
score = 0

# File pattern matches (+3 each)
for pattern in feature.relevance_signals.files:
    if Glob(pattern) returns results:
        score += 3

# Framework matches (+2 each)
for framework in feature.relevance_signals.frameworks:
    if framework in detected_frameworks:
        score += 2

# Indicator matches (+1 each)
for indicator in feature.relevance_signals.indicators:
    if indicator in detected_indicators:
        score += 1

# Workflow pattern matches (+1 each)
for pattern in feature.relevance_signals.workflow_patterns:
    if pattern in detected_workflow_patterns:
        score += 1

# Already-in-use penalty (-5)
if feature is already configured/in use:
    score -= 5

# New user bonus (+2)
if feature.difficulty == "beginner" AND ".claude/" does not exist:
    score += 2
```

---

## Tier Assignment

After scoring, assign features to tiers:

| Tier | Criteria | Count |
|---|---|---|
| **Quick Wins** | difficulty = "beginner" OR requires zero setup | 3-5 features |
| **Power-Ups** | difficulty = "intermediate" | 3-5 features |
| **Deep Cuts** | difficulty = "advanced" AND matches detected framework/language | 2-3 features |
