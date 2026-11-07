# Stil F · HTML-Gesprächsprotokoll

Das Panel führt ein echtes Gespräch und legt es als HTML-Seite ab. Oben steht, wer am Tisch sitzt (Rolle, Seite, Typ), darunter das vollständige Gespräch, am Ende das Fazit des Moderators. Die Seite lässt sich im Browser lesen, drucken und weitergeben.

## Das Gespräch

- **Keine Längengrenze.** Das Gespräch läuft so lange, wie es Substanz hat. Jeder Punkt wird ausdiskutiert, bis klar ist, ob das Panel sich einig ist oder nicht. Wiederholungen und Höflichkeitsfloskeln („Guter Punkt!“) gehören nicht dazu, denn sie machen das Protokoll länger, ohne etwas zu sagen.
- **Echte Reaktionen:** Teilnehmer sprechen sich an, widersprechen, fragen nach, geben nach oder bleiben bei ihrer Meinung. Mindestens ein Konflikt, der nicht sofort aufgelöst wird.
- **Konkrete Stellen zitieren:** Wenn jemand über eine bestimmte Formulierung, Codezeile oder Zahl spricht, diese im Feld `zitat` angeben.
- **In Runden gliedern:** Jeder gewählte Diskussionspunkt (siehe SKILL.md, Schritt 2) bekommt eine eigene Runde mit seinem Namen, z. B. „Runde 2 · Zahlungsbereitschaft“. Ohne gewählte Punkte z. B. „Runde 1 · Erster Eindruck“, „Runde 2 · Inhalt“, „Runde 3 · Was jetzt?“. Im Fazit kommt jeder gewählte Punkt mindestens einmal vor.
- **Jeder bleibt in seiner Rolle:** Der Personaler redet nicht über Codequalität, der Skeptiker lobt nicht ohne Grund.

## Der Moderator / Zuhörer

Er eröffnet das Gespräch mit einem Satz und hört danach zu. Er greift nur ein, wenn das Gespräch sich im Kreis dreht. Am Ende schreibt er das Fazit:

- **Kritikpunkte aller Teilnehmer**, zusammengeführt und gewichtet (kritisch / mittel / klein), jeweils mit den Personen, die sie genannt haben.
- **Konkrete, umsetzbare Verbesserungen.** Bei Texten jeweils mit Vorher/Nachher-Formulierung, bei Code mit der korrigierten Zeile, bei Ideen mit dem konkreten Schritt. „Präziser formulieren“ ist kein Vorschlag, „Satz X durch Satz Y ersetzen“ schon.
- **Note** (Analyse) bzw. **Urteil + Erfolgsaussicht** (Entscheidung), dazu was die Note misst.
- **Nächster Schritt.**

## Größe des Panels

In diesem Stil gibt es keine Obergrenze für die Zahl der gewählten Stimmen. Hat der Nutzer viele gewählt, alle aufnehmen und nicht zusammenlegen. Bei etwa 8 oder mehr Stimmen: mehr Runden, und in jeder Runde sprechen nur die Personen, die zu diesem Punkt etwas Eigenes beitragen.

## Seiten

Jeder Teilnehmer bekommt eine Seite. Sie bestimmt Farbe und Platz im Gespräch:

| `seite` | Bedeutung | Platz |
|---|---|---|
| `pro` | eher dafür, sieht Potenzial | rechts, grün |
| `contra` | eher dagegen, sucht Schwächen | links, rot |
| `neutral` | fachlich, ohne Richtung | links, grau |
| `moderator` | Moderator / Zuhörer (genau einer) | Mitte, blau |

Ein ausgewogenes Panel hat mindestens eine Stimme auf `pro` und eine auf `contra`.

## So entsteht die Seite

1. Gespräch und Fazit als JSON in eine temporäre Datei schreiben (Schema unten, Beispiel: `assets/beispiel-daten.json`).
2. Seite bauen:
   ```bash
   python3 <skill-pfad>/scripts/render.py daten.json <ausgabe>.html
   ```
   Das Skript prüft die Pflichtfelder und meldet, was fehlt. Für eine Sitzung einer Gesprächsreihe stattdessen `render.py daten.json --serie panel_<kurzname>/` (siehe `references/serie.md`).
3. Ablageort: neben der geprüften Datei, sonst im aktuellen Arbeitsordner. Dateiname: `panel_<thema-kurz>_<JJJJ-MM-TT>.html`.
4. Seite öffnen, wenn möglich (`xdg-open` / `open`). Im Chat nur kurz antworten: Pfad, Note bzw. Urteil, die 3 wichtigsten Punkte. Das ganze Gespräch steht auf der Seite und muss nicht im Chat wiederholt werden.

Ohne Python (z. B. Claude.ai): `assets/gespraech.html` kopieren und `__PANEL_DATEN__` durch das JSON ersetzen.

## JSON-Schema

Die Schlüssel und festen Werte (`seite`, `gewicht`: kritisch | mittel | klein) bleiben immer gleich. Nur die Texte werden in der Sprache des Nutzers geschrieben. Für Deutsch, Englisch und Arabisch sind die Beschriftungen der Seite eingebaut; für jede andere Sprache `beschriftungen` mitliefern (Beispiel unten: Französisch).

```json
{
  "titel": "Anschreiben Frontend-Entwickler",
  "modus": "Analyse",                 // oder "Entscheidung"
  "ziel": "Einladung zum Gespräch",
  "stil": "Gesprächsprotokoll",
  "datum": "2026-11-06",
  "sprache": "de",                  // Sprachcode des Nutzers: de, en, ar, fr, tr, fa, es, zh … (ar, fa, ur, he u. a. = rechts-nach-links)
  "beschriftungen": {               // nur für Sprachen außer de/en/ar: Beschriftungen der Seite übersetzen (fehlende Schlüssel → Englisch)
    "panel": "Panel d'experts", "ziel": "Objectif", "stil": "Style", "was": "Ce qui est évalué", "wer": "Autour de la table",
    "personen": "personnes", "gespraech": "La discussion", "beitraege": "interventions", "fazit": "Synthèse",
    "urteil": "Verdict du panel", "note": "Note globale", "krit": "Critiques du panel", "verb": "Améliorations concrètes",
    "vorher": "Avant", "nachher": "Après", "bed": "Condition clé", "next": "Prochaine étape", "q": ["« ", " »"],
    "seite": {"pro": "pour", "contra": "contre", "neutral": "neutre", "moderator": "modération"},
    "modi": {"Analyse": "Analyse", "Entscheidung": "Décision"},
    "kat": {"Fachexperte": "Expert", "Hierarchie": "Hiérarchie", "Persönlichkeitstyp": "Personnalité", "Betroffener": "Concerné", "Feste Rolle": "Rôle fixe"},
    "gew": {"kritisch": "critique", "mittel": "moyen", "klein": "mineur"},
    "unabh": "🔎 avis indépendant", "tiefe": "Mode approfondi", "quellen": "Sources",
    "footer": "Créé avec le skill multi-expert-panel. Toutes les voix sont simulées et ne remplacent pas un conseil professionnel."
  },
  "tiefenmodus": true,              // optional, siehe references/subagent-modus.md
  "serie": {"name": "…", "nummer": 2, "thema": "…", "rueckblick": ["…"]},  // optional, Gesprächsreihe: references/serie.md
  "gegenstand": "Geprüfter Text oder kurze Beschreibung (optional)",
  "teilnehmer": [
    {
      "id": "hr",                     // Pflicht, kurz, eindeutig
      "rolle": "HR-Personalerin",     // Pflicht
      "name": "Sabine",               // optional, macht das Gespräch lebendiger
      "seite": "contra",              // pro | contra | neutral | moderator
      "kategorie": "Fachexperte",     // Fachexperte | Hierarchie | Persönlichkeitstyp | Betroffener | Feste Rolle
      "typ": "Erbsenzähler",          // optional: Persönlichkeitstyp
      "hierarchie": "Senior",         // optional
      "fokus": "Pflichtangaben und erster Eindruck",
      "unabhaengig": true,            // optional, Tiefenmodus: erste Einschätzung kam von einem eigenen Agenten
      "quellen": [{"titel": "…", "url": "https://…"}]   // optional: recherchierte Quellen dieser Person
    }
  ],
  "gespraech": [
    {"runde": "Runde 1 · Erster Eindruck"},
    {"von": "moderator", "text": "…"},
    {"von": "hr", "text": "…", "zitat": "Ich bin ein leidenschaftlicher und motivierter Entwickler"}
  ],
  "fazit": {
    "note": "3/10",                    // Analyse
    "note_fuer": "Chance auf Einladung",
    "urteil": "PILOT",                 // Entscheidung: GO | GO MIT AUFLAGEN | PILOT | NO-GO
    "begruendung": "1–2 Sätze",
    "kritikpunkte": [
      {"gewicht": "kritisch", "text": "…", "von": ["hr", "hm"]}
    ],
    "verbesserungen": [
      {"was": "Pflichtangaben ergänzen", "warum": "…", "vorher": "…", "nachher": "…"}
    ],
    "wichtigste_bedingung": "nur Entscheidung",
    "naechster_schritt": "…",
    "hinweis": "Bei Recht/Finanzen/Medizin: ersetzt keine Fachberatung",
    "naechste_sitzung": ["optional: Themen für eine weitere Sitzung"]
  }
}
```
