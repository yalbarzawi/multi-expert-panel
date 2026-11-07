# Bibliothek des Expert-Panels

Die Bibliothek hilft dem Modell, passende **Rollen** und **Diskussionspunkte** vorzuschlagen und mit **aktuellem Wissen** zu arbeiten. Sie wird laufend erweitert. Neue Einträge brauchen keine Änderung an `SKILL.md`, solange sie dem Format unten folgen.

## Aufbau

```
library/
├── README.md          ← dieser Index + Regeln zum Erweitern
├── CHANGELOG.md       ← was wann dazukam
├── roles/             ← alle Rollen, eine Datei pro Kategorie
├── topics/            ← Themenpakete: Rollen + Punkte + Leitfragen + Fallen pro Thema
├── points.md          ← alle Diskussionspunkte + welche Rollen zu welchem Punkt passen
├── fields.md          ← vom Fachgebiet zur Rolle (wenn kein Themenpaket passt)
├── levels.md          ← Expertise-Leiter: jedes Fach vom Professor bis zum Laien
└── knowledge/         ← Fakten mit Datum und Quelle (Förderung, Marktpreise, Konkurrenz)
```

## So nutzt das Modell die Bibliothek

1. **Thema erkennen:** Die Zeile `Erkennen:` in den Dateien unter `topics/` mit der Anfrage vergleichen. Passt ein Paket, ist es der Ausgangspunkt für Rollen und Punkte.
2. **Kein Paket passt:** Fachgebiet über `fields.md` bestimmen und Rollen aus `roles/` mischen, Punkte aus `points.md` wählen. Fehlt das Fach ganz, mit `levels.md` Rollen bilden (Professor für …, Praktiker, Betroffener, Laie).
3. **Rollen anbieten:** ⭐ aus dem Paket zuerst, dazu Rollen aus anderen Kategorien (Hierarchie, Persönlichkeitstyp, Betroffener, Alltagsmensch, Recherche & Analyse) und aus mehreren Stufen der Expertise-Leiter, damit Forschung, Praxis und Alltag am Tisch sitzen.
4. **Punkte anbieten:** ⭐ aus dem Paket zuerst. Fehlt für einen gewählten Punkt eine passende Stimme: Tabelle „Welche Rollen zu welchem Punkt passen“ in `points.md`.
5. **Wissen nutzen:** Die Abschnitte `## Wissen` in den Paketen zeigen auf Dateien in `knowledge/`. Fakten dort haben ein `Stand`-Datum. Älter als 6 Monate und Websuche vorhanden → neu prüfen und die Datei aktualisieren. Ohne Websuche den Stand im Panel nennen.

Nur die Dateien lesen, die zum Thema gehören. Die ganze Bibliothek auf einmal zu laden, kostet Kontext ohne Nutzen.

## Kategorien der Rollen (`roles/`)

| Datei | Inhalt |
|---|---|
| software-it.md | Developer, Security, Architektur, DevOps, Datenschutz … |
| design-media.md | UI/UX, Art Director, Typograf, Markenstratege … |
| marketing-sales.md | SEO, Performance, Texter, Vertrieb, Marktforschung |
| law.md | Fachanwälte, Vertragsrecht, IT-/Medienrecht |
| finance-tax.md | Steuerberater, Finanzberater, Controller, Bank, Investor |
| hr-career.md | HR, Hiring Manager, Recruiter, Mentor |
| business-founding.md | Gründungsberater, Branchenveteran, Seriengründer, PM |
| research-analysis.md | Researcher, Wettbewerbsanalyst, Volkswirt, Finanzanalyst, Logiker, Statistiker … |
| real-estate-construction.md | Gutachter, Architekt, Makler, Handwerk, Energie |
| food-retail.md | Gastronom, Einzelhandel, Lebensmittelkontrolle, E-Commerce |
| health-psychology.md | Hausarzt, über 20 Fachärzte, Pflege, Apotheke, Therapie, Psychologie, Tierarzt |
| education-science.md | Lektor, Lehrer, Wissenschaftler, Übersetzer, Journalist |
| everyday-family.md | Familie, Budget, Verbraucherschutz |
| academia.md | Professor, Postdoc, Doktorand, Peer-Reviewer, Forschungsförderung |
| natural-sciences.md | Physik, Chemie, Biologie, Geo, Klima, Mathematik, Toxikologie … |
| engineering.md | Maschinenbau, Elektro, Bau/Statik, Produktion, Robotik, TÜV, Patente … |
| humanities-social.md | Soziologie, Geschichte, Ethik, Politik, Islamwissenschaft, Verhaltensökonomie … |
| trades-crafts.md | Elektriker, Installateur, Schreiner, Kfz, Bäcker, Landwirt, Fahrer … |
| public-sector-politics.md | Behörden, Politik, Justiz, Polizei, Feuerwehr, Zoll … |
| arts-culture-sport.md | Autor, Film, Musik, Museum, Influencer, Events, Sport, Games |
| everyday-people.md | Alltagsmenschen: Rentner, Student, Alleinerziehende, Pendler, Neu in Deutschland … |
| hierarchy.md | vom Azubi bis Aufsichtsrat |
| personality-types.md | Optimist, Skeptiker, Red Team, Zahlenmensch, Laie … |
| stakeholders.md | Zielkunde, Endnutzer, Konkurrent, Behörde, Zukunfts-Ich … |
| fixed-roles.md | Kritiker, Beobachter, Moderator (immer dabei) |

## Erweitern

### Neue Rolle
In die passende Datei unter `roles/` eine Tabellenzeile einfügen:
```
| Rollenname | Fokus in wenigen Wörtern |
```
- Der Fokus sagt, **worauf** die Rolle schaut, nicht wer sie ist.
- Keine Dubletten: erst mit `grep -ri "name" library/roles` prüfen.
- Neue Kategorie = neue Datei mit `# Titel` und `Kategorie: Fachexperte` (oder Hierarchie / Persönlichkeitstyp / Betroffener), dann oben in der Tabelle eintragen.

### Neues Themenpaket
Datei `topics/<thema-auf-englisch>.md` nach diesem Muster:
```
# Titel des Themas

Modus: Entscheidung            (oder Analyse)
Erkennen: Stichwörter Deutsch; English keywords; كلمات عربية

## Rollen

- ⭐ Rollenname: was sie in diesem Thema prüft
- Rollenname: …

## Diskussionspunkte

- ⭐ Punkt aus points.md
- Punkt …

## Leitfragen          (optional)
## Typische Fallen     (optional)
## Wissen              (optional, Links auf knowledge/…)
```
- 3 Rollen und 3–5 Punkte mit ⭐, Rollennamen genau wie in `roles/`.
- Ein neuer Punkt kommt zuerst mit Leitfrage in `points.md`.

### Neues Wissen
Datei in `knowledge/` oder neuer Abschnitt:
```
## Thema des Eintrags
Stand: JJJJ-MM-TT
- Fakt
Quellen: URL, URL
```
Kein Fakt ohne `Stand`. Unsichere Angaben als solche markieren („laut Drittquelle“, „nicht geprüft“).

### Danach
```bash
python3 scripts/check_library.py
```
Das Skript prüft Format, Rollennamen in Themenpaketen, Punkte gegen `points.md` und meldet Wissen, das älter als 6 Monate ist. Dann einen Eintrag in `CHANGELOG.md` schreiben.
