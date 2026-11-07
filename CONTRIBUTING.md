# Contributing

The library is the fuel of the panel. The easiest contribution is one line: a missing role.

## Add a role (2 minutes)

1. Open the matching file in [skills/multi-expert-panel/library/roles/](skills/multi-expert-panel/library/roles/), e.g. `health-psychology.md`.
2. Add a row: `| Zahnarzt | Behandlungsplan, Kosten, Alternativen |` (role names are German in the library; the panel translates them).
3. Run the check: `python3 skills/multi-expert-panel/scripts/check_library.py`
4. Add a line to [library/CHANGELOG.md](skills/multi-expert-panel/library/CHANGELOG.md) and open a pull request.

## Add a topic pack or a fact

See [library/README.md](skills/multi-expert-panel/library/README.md) for the format of topic packs (`topics/`) and dated facts with sources (`knowledge/`).

## Other changes

- Skill instructions: `skills/multi-expert-panel/SKILL.md` and `references/` (German on purpose, see the note at the top of SKILL.md).
- The HTML design (`assets/gespraech.html`) is final; please open an issue before changing it.
- After visible changes, regenerate the GIFs: `python3 scripts/make_demo_gifs.py` and `python3 scripts/make_flow_gifs.py`.

Commit messages, branches, versions and releases follow [AGENTS.md](AGENTS.md) (Conventional Commits, SemVer, Keep a Changelog).

Every pull request gets an answer within 7 days.
