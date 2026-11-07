#!/usr/bin/env python3
"""Baut dist/multi-expert-panel.zip für claude.ai (Einstellungen → Skills → hochladen).

Aufruf: python3 scripts/build_zip.py
Enthält nur den Skill-Ordner skills/multi-expert-panel/ (ohne GIFs, Caches),
mit dem Ordnernamen multi-expert-panel, wie claude.ai es erwartet.
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "multi-expert-panel"
ZIEL = ROOT / "dist" / "multi-expert-panel.zip"


def main():
    ZIEL.parent.mkdir(exist_ok=True)
    n = 0
    with zipfile.ZipFile(ZIEL, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SKILL.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc":
                z.write(f, Path("multi-expert-panel") / f.relative_to(SKILL))
                n += 1
    print(f"{ZIEL.relative_to(ROOT)}  {n} Dateien, {ZIEL.stat().st_size / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
