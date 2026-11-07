#!/usr/bin/env python3
"""Erzeugt die animierten Demo-GIFs für die READMEs (docs/*.gif).

Aufruf: python3 scripts/make_demo_gifs.py [--chrome /pfad/zu/chrome]

Ablauf: Demo-Daten (demo/*.json, skills/multi-expert-panel/assets/beispiel-daten.json) mit render.py
zu HTML bauen, mit Chrome headless als hohe Bildschirmfotos aufnehmen, daraus
ein weiches Scrollen (pro Sprache) und eine Überblendung zwischen den Sprachen
als GIF erzeugen. Braucht: Chrome/Chromium, ffmpeg, Pillow.
"""
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "multi-expert-panel"
W, H, FPS, OUT_W, COLORS = 880, 620, 8, 600, 96
DEMOS = {  # Sprache → Datendatei
    "en": ROOT / "demo/demo-en.json",
    "de": ROOT / "demo/demo-de-firma.json",
    "de-bewerbung": SKILL / "assets/beispiel-daten.json",
    "ar": ROOT / "demo/demo-ar.json",
    "fr": ROOT / "demo/demo-fr.json",
}
SCROLL = ["en", "de", "de-bewerbung", "ar"]          # bekommen ein eigenes Scroll-GIF
LANG_SWITCH = ["en", "de", "ar", "fr"]  # Reihenfolge der Überblendung


def chrome_pfad():
    if "--chrome" in sys.argv:
        return sys.argv[sys.argv.index("--chrome") + 1]
    for c in ("google-chrome", "chromium", "chromium-browser", "/opt/google/chrome/chrome"):
        if shutil.which(c) or Path(c).exists():
            return shutil.which(c) or c
    sys.exit("Chrome/Chromium nicht gefunden, mit --chrome angeben")


def aufnehmen(chrome, html, png, tmp):
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-color-profile=srgb", f"--window-size={W},12000",
                    f"--user-data-dir={tmp}/profil", f"--screenshot={png}", html.as_uri()],
                   check=True, stderr=subprocess.DEVNULL, timeout=90)
    im = Image.open(png).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((2, im.height - 2)))
    unten = ImageChops.difference(im, bg).getbbox()[3] + 30
    return im.crop((0, 0, W, min(unten, im.height)))


def gif(ordner, ziel):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{ordner}/%04d.png",
                    "-vf", f"scale={OUT_W}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors={COLORS}"
                           ":stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    "-loop", "0", str(ziel)], check=True)


def bilder(ordner, liste):
    ordner.mkdir()
    for i, im in enumerate(liste):
        im.save(ordner / f"{i:04d}.png")


def reihe(chrome, tmp):
    """Gesprächsreihe: Übersicht (index.html) → Sitzung 2 mit Rückblick → docs/demo-series.gif."""
    s1 = json.loads((ROOT / "demo/demo-en.json").read_text(encoding="utf-8"))
    s1["serie"] = {"name": "Online shop for handmade ceramics", "nummer": 1, "thema": "First look"}
    s1["fazit"]["naechste_sitzung"] = ["Shipping and breakage", "Production time next to a day job"]
    (tmp / "s1.json").write_text(json.dumps(s1, ensure_ascii=False), encoding="utf-8")
    ordner = tmp / "panel_ceramics-shop"
    ordner.mkdir()
    (ordner / "dossier.md").write_text("# Dossier\n", encoding="utf-8")
    for daten in (tmp / "s1.json", ROOT / "demo/series-en-2.json"):
        subprocess.run([sys.executable, str(SKILL / "scripts/render.py"), str(daten), "--serie", str(ordner)],
                       check=True, stdout=subprocess.DEVNULL)
    index = aufnehmen(chrome, ordner / "index.html", tmp / "r-index.png", tmp)
    s2 = aufnehmen(chrome, next(ordner.glob("sitzung-02_*.html")), tmp / "r-s2.png", tmp)
    def ausschnitt(im, y=0):
        flaeche = Image.new("RGB", (W, H), im.getpixel((2, im.height - 2)))
        flaeche.paste(im.crop((0, y, W, min(im.height, y + H))), (0, 0))
        return flaeche
    a, b = ausschnitt(index), ausschnitt(s2)
    ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * x)
    maxy = max(0, min(s2.height - H, 1100))
    folge = [a] * int(2.8 * FPS) + [Image.blend(a, b, k / 6) for k in range(1, 6)] + [b] * int(2 * FPS)
    folge += [ausschnitt(s2, int(maxy * ease(i / (3 * FPS)))) for i in range(3 * FPS + 1)] + [ausschnitt(s2, maxy)] * int(2.5 * FPS)
    bilder(tmp / "f-reihe", folge)
    gif(tmp / "f-reihe", ROOT / "docs/demo-series.gif")


def main():
    chrome = chrome_pfad()
    (ROOT / "docs").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        seiten = {}
        for lang, daten in DEMOS.items():
            if not daten.exists():
                print(f"übersprungen: {daten} fehlt")
                continue
            html = tmp / f"{lang}.html"
            subprocess.run([sys.executable, str(SKILL / "scripts/render.py"), str(daten), str(html)],
                           check=True, stdout=subprocess.DEVNULL)
            seiten[lang] = aufnehmen(chrome, html, tmp / f"{lang}.png", tmp)

        ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * x)
        for lang in SCROLL:
            if lang not in seiten:
                continue
            im = seiten[lang]
            maxy = max(0, im.height - H)
            schritte = int(min(7, 2.5 + maxy / 1200) * FPS)
            ys = [0] * int(1.5 * FPS) + [int(maxy * ease(i / schritte)) for i in range(schritte + 1)] + [maxy] * int(2.5 * FPS)
            bilder(tmp / f"f-{lang}", [im.crop((0, y, W, y + H)) for y in ys])
            gif(tmp / f"f-{lang}", ROOT / f"docs/demo-{lang}.gif")

        tops = [seiten[l].crop((0, 0, W, H)) for l in LANG_SWITCH if l in seiten]
        folge = []
        for i, a in enumerate(tops):
            b = tops[(i + 1) % len(tops)]
            folge += [a] * int(1.8 * FPS) + [Image.blend(a, b, k / 5) for k in range(1, 5)]
        if folge:
            bilder(tmp / "f-lang", folge)
            gif(tmp / "f-lang", ROOT / "docs/demo-languages.gif")
        reihe(chrome, tmp)
    for f in sorted((ROOT / "docs").glob("*.gif")):
        print(f"{f.relative_to(ROOT)}  {f.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
