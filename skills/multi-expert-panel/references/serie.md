# Gesprächsreihe · mehrere Sitzungen zu einem Vorhaben

Eine Sitzung gibt einen ersten Überblick. Große Vorhaben brauchen mehr: Die erste Sitzung findet die kritischen Punkte, die nächsten gehen je einem Punkt auf den Grund, jedes Mal mit den passenden Fachleuten. Jede Sitzung baut auf den vorherigen auf und wiederholt nichts, was schon geklärt ist.

## Ablage

Ein Ordner pro Vorhaben, im Arbeitsordner des Nutzers:

```
panel_<kurzname>/
├── index.html                       Übersicht: alle Sitzungen, Verlauf des Urteils
├── dossier.md                       Gedächtnis der Reihe (siehe unten)
├── sitzung-01_<thema>.html / .json  Sitzung 1: Gesamtbild
├── sitzung-02_<thema>.html / .json  Sitzung 2: ein Punkt in der Tiefe
└── …
```

`<kurzname>`: kurz, Kleinbuchstaben, lateinisch (z. B. `panel_host-your-logo`). Gibt es den Ordner schon, gehört die neue Sitzung dazu.

Bauen: `python3 scripts/render.py sitzung.json --serie panel_<kurzname>/`. Das Skript legt HTML und JSON mit fester Nummer ab, verlinkt alle Sitzungen (zurück · Übersicht · weiter) und baut `index.html` neu. Dieselbe Nummer noch einmal ersetzt diese Sitzung.

## Wann

- **Neue Reihe:** Der Nutzer sagt „mehrere Sitzungen“, „Reihe“, „Schritt für Schritt vertiefen“, "series", „سلسلة جلسات“, oder die Sache ist groß (Gründung, Investition, Bauprojekt, Karrierewechsel) und Stil F ist gewählt. Dann ist Sitzung 1 der Überblick. Am Ende schlägt das Fazit 2–4 Themen für weitere Sitzungen vor (`fazit.naechste_sitzung`).
- **Weitere Sitzung:** Der Nutzer sagt „nächste Sitzung“, „neue Sitzung zu …“, „vertiefe …“, „Sitzung 3“, "next session on …", „جلسة جديدة عن …“, „تعمّق في …“, oder er wählt einen vorgeschlagenen Punkt. Auch in einem späteren Gespräch: Liegt ein passender `panel_*`-Ordner im Arbeitsordner, an ihn anknüpfen.
- **Ohne Dateizugriff** (z. B. reiner Chat): Die Reihe läuft im selben Gespräch weiter. Am Anfang jeder Sitzung steht dann der Rückblick als Text.

## Ablauf einer weiteren Sitzung

1. **Lesen, nicht raten:** zuerst `dossier.md` und das `fazit` der letzten Sitzung (`sitzung-NN_*.json`). Ganze frühere Gespräche nur lesen, wenn eine genaue Aussage gebraucht wird.
2. **Thema wählen:**
   - Hat der Nutzer ein Thema genannt, ist es gesetzt.
   - Sonst 2–4 Themen vorschlagen, aus `naechste_sitzung`, offenen Fragen und 🚨-Punkten im Dossier. Zu jedem Thema ein Halbsatz, warum es jetzt dran ist.
3. **Panel neu zusammenstellen.** Jede Sitzung hat ihr eigenes Panel:
   - **Fachleute für genau dieses Thema** aus der Bibliothek, z. B. eine Sitzung „Förderung“ mit Fördermittelberater, Steuerberaterin und Bankberater.
   - **1–2 Stimmen aus früheren Sitzungen**, die das Thema aufgebracht haben. Sie sorgen für den roten Faden.
   - Der **Moderator** bleibt in der ganzen Reihe dieselbe Person (gleicher `name`). Kritiker und Beobachter sind immer dabei.
   - Gefragt wird wie in Schritt 2 von SKILL.md. Sind Thema und Panel schon genannt, nicht fragen.
4. **Rückblick zu Beginn** (`serie.rueckblick`, 3–6 Stichpunkte): bisheriges Urteil mit Note, was geklärt ist, was offen ist und wichtige Fakten mit Quelle. Der Moderator eröffnet damit.
5. **Gespräch in der Tiefe:**
   - Nur das Thema der Sitzung, dafür gründlicher als in Sitzung 1: Zahlen, Varianten, konkrete Schritte.
   - Geklärtes wird nicht neu verhandelt. Ausnahme: Es gibt neue Fakten, und dann sagt das Gespräch, was sich geändert hat.
   - Teilnehmer dürfen auf frühere Sitzungen verweisen („In Sitzung 1 hat der Red Team gesagt …“).
6. **Fazit:**
   - Wie immer mit Urteil bzw. Note.
   - Ändert sich das Gesamturteil, sagt die `begruendung`, was es verändert hat („von PILOT 5/10 auf GO MIT AUFLAGEN 6/10, weil …“).
   - Dazu `naechste_sitzung`, oder ein klarer Hinweis, dass die Reihe für eine Entscheidung reicht.
7. **Bauen und Dossier aktualisieren:**
   - `render.py … --serie` ausführen.
   - `dossier.md` aktualisieren, vor dem Bauen, damit `index.html` darauf verlinkt.
   - Dem Nutzer den Link zu `index.html` und zur neuen Sitzung geben.

Tiefenmodus (unabhängige Agenten) und Reihe lassen sich kombinieren. Die Agenten bekommen dann den Rückblick mit, aber nicht die früheren Gespräche.

## dossier.md

Das Gedächtnis der Reihe. Kurz halten (unter etwa 150 Zeilen), Neues ergänzen, Veraltetes ändern statt doppelt führen.

```markdown
# <Vorhaben> · Dossier
Stand: <JJJJ-MM-TT> · Sitzungen: <n> · Aktuelles Urteil: <Urteil Note>

## Ziel und Rahmen
- Ziel, Budget, Zeitrahmen, Phase (vom Nutzer)

## Verlauf
| Nr. | Datum | Thema | Urteil | Was sich geändert hat |
|---|---|---|---|---|

## Entschieden / geklärt
- … (Sitzung n)

## Offene Fragen
- [ ] … (aufgebracht von <Rolle>, Sitzung n)

## Fakten und Quellen
- … (Quelle, Stand JJJJ-MM-TT)

## Wer schon mitgeredet hat
- <Rolle> (<Name>): Sitzung 1, 3 · Haltung: dafür / dagegen
```

Allgemein nützliche, geprüfte Fakten (z. B. Förderbedingungen) zusätzlich in `library/knowledge/` eintragen, siehe SKILL.md.

## JSON-Felder (zusätzlich zu `references/html-gespraech.md`)

```json
"serie": {
  "name": "Host your Logo",                 // gleich in allen Sitzungen
  "nummer": 2,                              // 1, 2, 3 …
  "thema": "Ownership verification",        // Thema dieser Sitzung (für Dateiname und Übersicht)
  "rueckblick": ["Sitzung 1: PILOT 5/10 …", "Offen: …"]   // ab Sitzung 2
},
"fazit": {
  "naechste_sitzung": ["Preise und Abo-Modell", "…"]      // Vorschläge für weitere Sitzungen
}
```

`serie.links` setzt `render.py` selbst. Für Sprachen außer de/en/ar können die Beschriftungen der Übersicht unter `beschriftungen.serie` mitkommen (Schlüssel: `reihe`, `sitzungen`, `stimmen`, `beitraege`, `verlauf`, `alle`, `next`, `dossier`, `tiefe`, `footer`), die der Sitzungsseite direkt unter `beschriftungen` (`sitzung`, `reihe`, `uebersicht`, `rueckblick`, `vertiefen`).
