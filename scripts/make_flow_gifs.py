#!/usr/bin/env python3
"""Erzeugt die animierten Ablauf-GIFs des Werkzeugs (docs/flow-<sprache>.gif).

Aufruf: python3 scripts/make_flow_gifs.py [--chrome /pfad/zu/chrome] [en de ar]

Zeigt den Ablauf im Terminal: Befehl tippen → Panel, Perspektiven, Punkte und Stil
wählen → unabhängige Agenten arbeiten → kurzer Schlagabtausch → Urteil.
Inhalte: demo/flow.json, Aussehen: demo/flow.html.
Braucht: Chrome/Chromium, ffmpeg, Pillow.
"""
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_demo_gifs import ROOT, chrome_pfad, gif  # noqa: E402

W, H = 880, 560


def ereignisse(f):
    """Liste von (Ereignis, Anzahl Bilder), die das Bild nach dem Ereignis zeigen."""
    ev = []
    cmd = f["cmd"]
    for k in range(0, len(cmd) + 1, 3):
        ev.append(({"t": "type", "n": k}, 1))
    ev.append(({"t": "type", "n": len(cmd)}, 4))
    ev.append(({"t": "enter"}, 3))
    for i in range(len(f["think"])):
        ev.append(({"t": "think", "i": i}, 7))
    for i, q in enumerate(f["questions"]):
        ev.append(({"t": "q", "i": i}, 6))
        pos = 0
        for j in q["ticks"]:
            while pos < j:
                pos += 1
                ev.append(({"t": "cur", "i": i, "o": pos}, 2))
            ev.append(({"t": "tick", "i": i, "o": j}, 4))
        ev.append(({"t": "submit", "i": i}, 3))
    for p in range(0, 11):
        ev.append(({"t": "agents", "p": p / 10}, 2))
    ev.append(({"t": "agents", "p": 1}, 8))
    for i in range(len(f["debate"])):
        ev.append(({"t": "debate", "i": i}, 11))
    ev.append(({"t": "verdict"}, 12))
    ev.append(({"t": "saved"}, 32))
    return ev


def main():
    chrome = chrome_pfad()
    langs = [a for a in sys.argv[1:] if not a.startswith("--") and a != chrome] or ["en", "de", "ar"]
    flows = json.loads((ROOT / "demo/flow.json").read_text(encoding="utf-8"))
    vorlage = (ROOT / "demo/flow.html").read_text(encoding="utf-8")
    (ROOT / "docs").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for lang in langs:
            f = flows[lang]
            ev = ereignisse(f)
            html = tmp / f"flow-{lang}.html"
            html.write_text(vorlage.replace("__FLOW__", json.dumps(f, ensure_ascii=False))
                            .replace("__EVENTS__", json.dumps([e for e, _ in ev])), encoding="utf-8")

            def shot(n):
                png = tmp / f"{lang}-{n:04d}.png"
                for versuch in range(3):  # Chrome bricht headless gelegentlich ab, dann neu versuchen
                    r = subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                                        "--force-color-profile=srgb", f"--window-size={W},{H}",
                                        f"--user-data-dir={tmp}/profil-{lang}-{n % 6}-{versuch}", f"--screenshot={png}",
                                        f"{html.as_uri()}#{n}"], stderr=subprocess.DEVNULL, timeout=60)
                    if r.returncode == 0 and png.exists():
                        return png
                sys.exit(f"Chrome konnte Zustand {n} ({lang}) nicht aufnehmen")

            # Profile werden nach n % 6 geteilt, also je Profil nur ein Chrome gleichzeitig.
            schritte = list(range(1, len(ev) + 1))
            gruppen = [schritte[r::6] for r in range(6)]
            with ThreadPoolExecutor(6) as pool:
                ergebnisse = list(pool.map(lambda g: [shot(n) for n in g], gruppen))
            pngs = {int(p.stem.split("-")[1]): p for g in ergebnisse for p in g}

            ordner = tmp / f"frames-{lang}"
            ordner.mkdir()
            i = 0
            for n, (_, halten) in enumerate(ev, start=1):
                im = Image.open(pngs[n]).convert("RGB").crop((0, 0, W, H))
                for _ in range(halten):
                    im.save(ordner / f"{i:04d}.png")
                    i += 1
            gif(ordner, ROOT / f"docs/flow-{lang}.gif")
            ziel = ROOT / f"docs/flow-{lang}.gif"
            print(f"{ziel.relative_to(ROOT)}  {len(ev)} Zustände, {i} Bilder, {ziel.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
