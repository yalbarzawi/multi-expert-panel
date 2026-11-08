#!/usr/bin/env python3
"""Baut die HTML-Gesprächsseite aus einer JSON-Datei.

Aufruf:
  python3 render.py daten.json ausgabe.html          einzelne Sitzung
  python3 render.py daten.json --serie ORDNER        Sitzung einer Gesprächsreihe

Prüft die Pflichtfelder, setzt die Daten in assets/gespraech.html ein und
gibt den Pfad der fertigen Seite aus. Mit --serie wird die Sitzung als
sitzung-NN_<thema>.json/.html in ORDNER abgelegt, alle Sitzungen der Reihe
bekommen Vor/Zurück-Links und ORDNER/index.html wird neu gebaut
(Übersicht mit Verlauf des Urteils). Nur Standardbibliothek.
"""
import json
import re
import unicodedata
import sys
from pathlib import Path

VORLAGE = Path(__file__).resolve().parent.parent / "assets" / "gespraech.html"
INDEX_VORLAGE = VORLAGE.with_name("serie-index.html")
SEITEN = {"pro", "contra", "neutral", "moderator"}
GEWICHTE = {"kritisch", "mittel", "klein"}


def pruefen(d):
    fehler = []
    for feld in ("titel", "teilnehmer", "gespraech", "fazit"):
        if not d.get(feld):
            fehler.append(f"Feld '{feld}' fehlt oder ist leer")
    ids = set()
    for i, p in enumerate(d.get("teilnehmer", [])):
        if not p.get("id") or not p.get("rolle"):
            fehler.append(f"teilnehmer[{i}]: 'id' und 'rolle' sind Pflicht")
        if p.get("seite", "neutral") not in SEITEN:
            fehler.append(f"teilnehmer[{i}]: seite muss eine von {sorted(SEITEN)} sein")
        for k, q in enumerate(p.get("quellen") or []):
            if not isinstance(q, dict) or not re.match(r"https?://", str(q.get("url", ""))):
                fehler.append(f"teilnehmer[{i}].quellen[{k}]: braucht 'url' mit http(s)://")
        ids.add(p.get("id"))
    if not any(p.get("seite") == "moderator" for p in d.get("teilnehmer", [])):
        fehler.append("Es fehlt ein Teilnehmer mit seite 'moderator'")
    for i, m in enumerate(d.get("gespraech", [])):
        if "runde" in m:
            continue
        if m.get("von") not in ids:
            fehler.append(f"gespraech[{i}]: 'von' = {m.get('von')!r} ist keine Teilnehmer-id")
        if not m.get("text"):
            fehler.append(f"gespraech[{i}]: 'text' fehlt")
    sprache = str(d.get("sprache", "de"))
    if not re.fullmatch(r"[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})?", sprache):
        fehler.append("sprache muss ein Sprachcode sein, z. B. de, en, ar, fr, tr, fa, es, zh")
    b = d.get("beschriftungen")
    if b is not None and not isinstance(b, dict):
        fehler.append("beschriftungen muss ein Objekt sein")
    f = d.get("fazit", {})
    if not (f.get("note") or f.get("urteil")):
        fehler.append("fazit: 'note' oder 'urteil' ist Pflicht")
    for i, k in enumerate(f.get("kritikpunkte", [])):
        if k.get("gewicht", "mittel") not in GEWICHTE:
            fehler.append(f"fazit.kritikpunkte[{i}]: gewicht muss eine von {sorted(GEWICHTE)} sein")
    if not f.get("verbesserungen"):
        fehler.append("fazit: 'verbesserungen' fehlt (konkrete Vorschläge sind Pflicht)")
    serie = d.get("serie")
    if serie is not None:
        if not isinstance(serie, dict) or not serie.get("name") or not serie.get("thema"):
            fehler.append("serie: braucht 'name' und 'thema'")
        elif not isinstance(serie.get("nummer"), int) or serie["nummer"] < 1:
            fehler.append("serie.nummer muss eine ganze Zahl ab 1 sein")
        elif not isinstance(serie.get("rueckblick", []), list):
            fehler.append("serie.rueckblick muss eine Liste sein")
    return fehler


def einbetten(vorlage, platzhalter, daten):
    # </script> im Text würde den JSON-Block beenden
    roh = json.dumps(daten, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return vorlage.read_text(encoding="utf-8").replace(platzhalter, roh)


def kurzname(text):
    t = str(text).lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:40].strip("-") or "thema"


def serie_bauen(daten, ordner):
    """Legt die Sitzung in ORDNER ab, verlinkt alle Sitzungen und baut index.html neu."""
    ordner.mkdir(parents=True, exist_ok=True)
    nr = daten["serie"]["nummer"]
    for alt in ordner.glob(f"sitzung-{nr:02d}_*.json"):  # gleiche Nummer = neue Fassung dieser Sitzung
        alt.unlink()
        alt.with_suffix(".html").unlink(missing_ok=True)
    stamm = f"sitzung-{nr:02d}_{kurzname(daten['serie']['thema'])}"
    daten = {k: v for k, v in daten.items()}
    daten["serie"] = {k: v for k, v in daten["serie"].items() if k != "links"}
    (ordner / f"{stamm}.json").write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")

    sitzungen = []
    for f in sorted(ordner.glob("sitzung-*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if isinstance(d.get("serie"), dict) and isinstance(d["serie"].get("nummer"), int):
            sitzungen.append((d["serie"]["nummer"], f, d))
    sitzungen.sort(key=lambda x: x[0])
    for i, (_, f, d) in enumerate(sitzungen):
        d["serie"]["links"] = {
            "index": "index.html",
            "zurueck": sitzungen[i - 1][1].with_suffix(".html").name if i > 0 else None,
            "weiter": sitzungen[i + 1][1].with_suffix(".html").name if i + 1 < len(sitzungen) else None,
        }
        f.with_suffix(".html").write_text(einbetten(VORLAGE, "__PANEL_DATEN__", d), encoding="utf-8")

    letzte = sitzungen[-1][2] if sitzungen else daten
    index = {
        "name": letzte["serie"]["name"],
        "sprache": letzte.get("sprache", "de"),
        "beschriftungen": (letzte.get("beschriftungen") or {}).get("serie", {}),
        "dossier": "dossier.md" if (ordner / "dossier.md").exists() else None,
        "sitzungen": [{
            "nummer": n, "thema": d["serie"]["thema"], "datum": d.get("datum"),
            "datei": f.with_suffix(".html").name,
            "teilnehmer": len(d.get("teilnehmer", [])),
            "beitraege": len([m for m in d.get("gespraech", []) if m.get("von")]),
            "tiefenmodus": bool(d.get("tiefenmodus") or any(p.get("unabhaengig") for p in d.get("teilnehmer", []))),
            "urteil": d["fazit"].get("urteil"), "note": d["fazit"].get("note"),
            "begruendung": d["fazit"].get("begruendung"), "naechster_schritt": d["fazit"].get("naechster_schritt"),
        } for n, f, d in sitzungen],
    }
    (ordner / "index.html").write_text(einbetten(INDEX_VORLAGE, "__SERIE_DATEN__", index), encoding="utf-8")
    return ordner / f"{stamm}.html"


def main():
    args = sys.argv[1:]
    serie_modus = len(args) == 3 and args[1] == "--serie"
    if len(args) != 2 and not serie_modus:
        sys.exit("Aufruf: render.py daten.json ausgabe.html | render.py daten.json --serie ORDNER")
    daten = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    fehler = pruefen(daten)
    if serie_modus and not daten.get("serie"):
        fehler.append("Für --serie braucht die Datei ein Feld 'serie' mit name, nummer, thema")
    if fehler:
        sys.exit("Daten unvollständig:\n- " + "\n- ".join(fehler))
    if serie_modus:
        ziel = serie_bauen(daten, Path(args[2]))
        print(ziel.resolve())
        print((ziel.parent / "index.html").resolve())
        return
    ziel = Path(args[1])
    ziel.write_text(einbetten(VORLAGE, "__PANEL_DATEN__", daten), encoding="utf-8")
    print(ziel.resolve())


if __name__ == "__main__":
    main()
