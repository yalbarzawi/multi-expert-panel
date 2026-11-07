#!/usr/bin/env python3
"""Prüft, ob die Version an allen vier Stellen gleich ist (siehe AGENTS.md, Abschnitt 4).

Aufruf:
  python3 scripts/check_version.py              Versionen vergleichen
  python3 scripts/check_version.py v1.0.0       zusätzlich: passt der Tag?
  python3 scripts/check_version.py --notes      Abschnitt der aktuellen Version aus CHANGELOG.md ausgeben
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def versionen():
    skill = (ROOT / "skills/multi-expert-panel/SKILL.md").read_text(encoding="utf-8")
    m = re.search(r'^\s+version:\s*"?([0-9][^"\s]*)"?\s*$', skill.split("\n---", 1)[0], re.M)
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    markt = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    log = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    c = re.search(r"^## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}", log, re.M)
    return {
        "SKILL.md": m.group(1) if m else None,
        "plugin.json": plugin.get("version"),
        "marketplace.json": (markt.get("plugins") or [{}])[0].get("version"),
        "CHANGELOG.md": c.group(1) if c else None,
    }, log


def main():
    v, log = versionen()
    if "--notes" in sys.argv:
        aktuell = v["CHANGELOG.md"]
        teil = re.search(rf"^## \[{re.escape(aktuell)}\].*?\n(.*?)(?=^## \[|\Z)", log, re.M | re.S)
        print(teil.group(1).strip() if teil else "")
        return
    fehler = [f"{k}: {w}" for k, w in v.items() if w is None]
    if len(set(v.values())) != 1:
        fehler.append("Versionen unterschiedlich: " + ", ".join(f"{k}={w}" for k, w in v.items()))
    tag = next((a for a in sys.argv[1:] if a.startswith("v")), None)
    if tag and tag[1:] != v["SKILL.md"]:
        fehler.append(f"Tag {tag} passt nicht zu Version {v['SKILL.md']}")
    if fehler:
        sys.exit("Versionsprüfung fehlgeschlagen:\n- " + "\n- ".join(fehler))
    print(f"Version {v['SKILL.md']} überall gleich" + (f", Tag {tag} passt" if tag else ""))


if __name__ == "__main__":
    main()
