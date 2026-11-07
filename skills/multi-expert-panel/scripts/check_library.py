#!/usr/bin/env python3
"""Prüft die Bibliothek unter library/.

Aufruf: python3 scripts/check_library.py [--max-alter-tage 180]

- Rollen: jede Datei in roles/ hat Titel, Kategorie und eine Tabelle; keine doppelten Rollennamen.
- Themenpakete: Modus, Erkennen, Rollen und Punkte vorhanden; Rollen existieren in roles/,
  Punkte existieren in points.md; 1–3 Rollen mit ⭐.
- Wissen: jeder Abschnitt hat ein Stand-Datum; zu alte Einträge werden gemeldet.
Fehler → Exit-Code 1, Hinweise → nur Ausgabe. Nur Standardbibliothek.
"""
import datetime
import re
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "library"
KATEGORIEN = {"Fachexperte", "Hierarchie", "Persönlichkeitstyp", "Betroffener", "Feste Rolle"}


def schluessel(name):
    """Vergleichsform: Klammern, Emojis und Leerraum entfernen, klein."""
    name = re.sub(r"\(.*?\)|„.*?“", "", name)
    name = re.sub(r"[^\w\s/&.-]", "", name)
    return re.sub(r"\s+", " ", name).strip().lower()


def tabellen_erste_spalte(text):
    zeilen = []
    for z in text.splitlines():
        if z.startswith("|") and not re.match(r"^\|\s*-", z):
            zeilen.append(z.split("|")[1].strip())
    return zeilen[1:] if zeilen else []  # Kopfzeile weg


def main():
    max_alter = 180
    if "--max-alter-tage" in sys.argv:
        max_alter = int(sys.argv[sys.argv.index("--max-alter-tage") + 1])
    fehler, hinweise = [], []

    # Rollen
    rollen = {}
    for f in sorted((LIB / "roles").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        if not t.startswith("# "):
            fehler.append(f"{f.name}: erste Zeile muss '# Titel' sein")
        m = re.search(r"^Kategorie: (.+)$", t, re.M)
        if not m or m.group(1).strip() not in KATEGORIEN:
            fehler.append(f"{f.name}: 'Kategorie:' fehlt oder ist keine von {sorted(KATEGORIEN)}")
        namen = tabellen_erste_spalte(t)
        if not namen:
            fehler.append(f"{f.name}: keine Rollentabelle gefunden")
        for n in namen:
            k = schluessel(n)
            if k in rollen:
                fehler.append(f"Rolle doppelt: '{n}' in {f.name} und {rollen[k][0]}")
            rollen[k] = (f.name, n)

    # Teilnamen ("Skeptiker / Realist" → auch "skeptiker", "realist")
    bekannt = set(rollen)
    for k in list(rollen):
        for teil in k.split(" / "):
            bekannt.add(teil.strip())

    # Punkte
    pt = (LIB / "points.md").read_text(encoding="utf-8")
    punkte = {schluessel(p) for p in tabellen_erste_spalte(pt)}

    # Themenpakete
    for f in sorted((LIB / "topics").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        for feld in ("Modus:", "Erkennen:", "## Rollen", "## Diskussionspunkte"):
            if feld not in t:
                fehler.append(f"topics/{f.name}: '{feld}' fehlt")
        teile = re.split(r"^## ", t, flags=re.M)
        abschnitte = {s.split("\n", 1)[0].strip(): s for s in teile[1:]}
        sterne = 0
        for z in abschnitte.get("Rollen", "").splitlines():
            m = re.match(r"^- (⭐ )?([^:]+):", z)
            if not m:
                continue
            sterne += bool(m.group(1))
            if schluessel(m.group(2)) not in bekannt:
                hinweise.append(f"topics/{f.name}: Rolle '{m.group(2)}' nicht in roles/ gefunden")
        if not 1 <= sterne <= 3:
            hinweise.append(f"topics/{f.name}: {sterne} Rollen mit ⭐ (empfohlen 1–3)")
        for z in abschnitte.get("Diskussionspunkte", "").splitlines():
            m = re.match(r"^- (⭐ )?(.+)$", z)
            if m and schluessel(m.group(2)) not in punkte:
                hinweise.append(f"topics/{f.name}: Punkt '{m.group(2)}' fehlt in points.md")
        for link in re.findall(r"\]\(\.\./(knowledge/[^)]+)\)", t):
            if not (LIB / link).exists():
                fehler.append(f"topics/{f.name}: Verweis auf {link} existiert nicht")

    # Wissen
    heute = datetime.date.today()
    for f in sorted((LIB / "knowledge").glob("*.md")):
        for abschnitt in re.split(r"^## ", f.read_text(encoding="utf-8"), flags=re.M)[1:]:
            titel = abschnitt.split("\n", 1)[0].strip()
            m = re.search(r"^Stand: (\d{4}-\d{2}-\d{2})", abschnitt, re.M)
            if not m:
                fehler.append(f"knowledge/{f.name} › {titel}: 'Stand: JJJJ-MM-TT' fehlt")
                continue
            alter = (heute - datetime.date.fromisoformat(m.group(1))).days
            if alter > max_alter:
                hinweise.append(f"knowledge/{f.name} › {titel}: {alter} Tage alt, neu prüfen")
            if "Quellen:" not in abschnitt:
                hinweise.append(f"knowledge/{f.name} › {titel}: keine Quellen")

    print(f"Rollen: {len(rollen)} · Punkte: {len(punkte)} · "
          f"Themenpakete: {len(list((LIB / 'topics').glob('*.md')))} · "
          f"Wissensdateien: {len(list((LIB / 'knowledge').glob('*.md')))}")
    for h in hinweise:
        print("Hinweis:", h)
    for e in fehler:
        print("FEHLER:", e)
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
