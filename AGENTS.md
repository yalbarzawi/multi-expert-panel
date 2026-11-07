# Working rules for this repository

These rules apply to every contributor, human or AI agent (Claude Code reads them through `CLAUDE.md`). Follow them for every commit, tag and release.

## 1. Repository layout

| Path | Content |
|---|---|
| `skills/multi-expert-panel/` | the skill itself: `SKILL.md`, `library/`, `references/`, `assets/`, `scripts/render.py`, `scripts/check_library.py` |
| `.claude-plugin/` | `plugin.json` and `marketplace.json` (Claude Code plugin) |
| `docs/` | GIFs and icons for the READMEs, not part of the skill |
| `demo/` | demo data for the GIFs |
| `scripts/` | tools for maintainers: GIFs, ZIP, version check, trigger test |
| `evals/` | eval cases |

Fixed decisions: the skill name is `multi-expert-panel` (English, never rename it). The HTML protocol design (`assets/gespraech.html`, colours included) is approved; do not redesign it without an issue. Skill instructions are German on purpose.

## 2. Commits

Format: [Conventional Commits 1.0](https://www.conventionalcommits.org/en/v1.0.0/), written in **English**.

```
<type>(<scope>): <summary>

<body: why, not what. Wrap at 72 characters.>

<footer: BREAKING CHANGE: …, Refs #12, Co-Authored-By: …>
```

- **Summary:** imperative mood ("add", not "added"), lower case, no period, at most 72 characters.
- **One logical change per commit.** The repository must work after every commit (checks pass, links resolve).
- **Types:**

| Type | Use for | Version effect |
|---|---|---|
| `feat` | new behaviour of the skill (mode, style, option) | minor |
| `fix` | wrong behaviour, broken output, wrong fact | patch |
| `library` | roles, topic packs, points, knowledge files | patch (minor for a new category or 5+ topic packs) |
| `docs` | READMEs, references for humans, comments | none |
| `refactor` | restructuring without behaviour change | none |
| `test` | evals, trigger queries | none |
| `build` | ZIP, plugin manifests, packaging | none |
| `ci` | GitHub workflows | none |
| `chore` | everything else, including `chore(release)` | none |

- **Scopes** (optional, one word): `skill`, `library`, `html`, `render`, `deep`, `series`, `plugin`, `demo`, `readme`.
- **Breaking change:** `!` after the type and a `BREAKING CHANGE:` footer. Breaking means: install path, skill name, trigger words, JSON schema of `render.py`, or file layout that users depend on.
- **AI commits** end with a `Co-Authored-By:` line naming the model.
- **Before every commit:**
  ```bash
  python3 skills/multi-expert-panel/scripts/check_library.py
  python3 scripts/check_version.py
  ```
  Library changes also get a line in `skills/multi-expert-panel/library/CHANGELOG.md`. Visible UI changes: regenerate GIFs (`scripts/make_demo_gifs.py`, `scripts/make_flow_gifs.py`).

Examples:
```
feat(series): continue a series from an existing panel_* folder
fix(render): reject source links without http(s)
library: add 14 dentistry and veterinary roles
docs(readme): show install options per platform
feat!: move skill into skills/ for plugin layout
```

## 3. Branches and history

- `main` is always releasable. No direct work on `main`.
- Work on short branches: `feat/<topic>`, `fix/<topic>`, `library/<topic>`, `docs/<topic>`, `release/vX.Y.Z`.
- Merge into `main` with a fast-forward or squash merge, so `main` stays linear.
- Rewrite history (rebase, squash, amend) **only on branches that were never pushed**. Never force-push `main`, never move or delete a pushed tag.

## 4. Versions

[Semantic Versioning 2.0](https://semver.org/): `MAJOR.MINOR.PATCH`.

- **MAJOR:** any breaking change from section 2.
- **MINOR:** new feature (`feat`), or a large library extension.
- **PATCH:** fixes and normal library additions.

The version lives in **four places that must always match** (checked by `scripts/check_version.py` and CI):
1. `skills/multi-expert-panel/SKILL.md` → `metadata.version`
2. `.claude-plugin/plugin.json` → `version`
3. `.claude-plugin/marketplace.json` → `plugins[0].version`
4. `CHANGELOG.md` → newest `## [X.Y.Z] - YYYY-MM-DD` heading

Claude Code users only receive an update when the version changes.

## 5. Changelog

`CHANGELOG.md` follows [Keep a Changelog 1.1](https://keepachangelog.com/en/1.1.0/). New entries go under `## [Unreleased]` with the groups `Added`, `Changed`, `Fixed`, `Removed`, `Security`. Write for users: what changes for them, not which file changed. The library has its own detailed log in `skills/multi-expert-panel/library/CHANGELOG.md`.

## 6. Tags and releases

Tags are **annotated**, named `vX.Y.Z`, and point to the release commit on `main`.

Release checklist:
1. Branch `release/vX.Y.Z` from `main`.
2. Move `## [Unreleased]` in `CHANGELOG.md` to `## [X.Y.Z] - YYYY-MM-DD`, add a new empty `## [Unreleased]`.
3. Set the version in the four places from section 4.
4. Run the checks from section 2 and `python3 scripts/build_zip.py`.
5. Commit: `chore(release): vX.Y.Z`
6. Merge into `main`, then:
   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin main vX.Y.Z
   ```
7. The `release` workflow checks that the tag matches the version, builds `multi-expert-panel.zip` and publishes the GitHub release with the changelog section as notes.

An agent never pushes, tags or publishes a release without an explicit request from the maintainer in the current conversation.
