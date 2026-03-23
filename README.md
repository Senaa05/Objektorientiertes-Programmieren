# Bibflow

Gruppenmitglieder: Sena Besir, Giulia Falone, Naomi Uwensuyi

Dozierende: Felix Härer, Grieder Hermann

## Hauptfunktionen

### Administrator
- Bücher erfassen, bearbeiten und löschen
- Verfügbarkeit von Exemplaren verwalten
- Überfällige Bücher manuell auf "verfügbar" setzen
- Benutzerkonten erstellen und verwalten
- Statistiken über Ausleihen einsehen

### Benutzer
- Alle Bücher durchsuchen und anzeigen
- Beliebteste Bücher einsehen
- Bis zu 5 Bücher gleichzeitig ausleihen
- Ausleihen um 14 Tage verlängern (1x pro Buch)
- Persönliche Merkliste verwalten
- "Meine Liste" mit aktuellen Ausleihen

### Ausleihe 
- 30 Tage Standard-Ausleihdauer
- Automatische Erinnerung bei < 7 Tagen Restlaufzeit
- Pop-up bei überfälligen Büchern
- Echtzeit-Status der Buchverfügbarkeit

## User Stories

**Als Administrator möchte ich:**
- Bücher erfassen, damit die Bibliothek aktuell bleibt
- Buch-Informationen bearbeiten, damit Daten korrekt sind
- Bücher löschen, damit veraltete Medien entfernt werden
- Überfällige Bücher zurücksetzen, damit sie wieder verfügbar sind
- Benutzer erstellen, damit neue Leute Zugang erhalten

**Als Benutzer möchte ich:**
- Alle Bücher durchsuchen, damit ich interessante Titel finde
- Beliebteste Bücher sehen, damit ich weiß was gut ist
- Bücher ausleihen, damit ich sie lesen kann
- Ausleihen verlängern, damit ich mehr Zeit habe
- Bücher merken, damit ich sie später leicht finde
- Meine Ausleihen sehen, damit ich den Überblick behalte

## Use Cases

### UC1: Buch ausleihen (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer sucht nach einem Buch
3. System zeigt verfügbare Exemplare
4. Benutzer wählt ein Exemplar aus
5. System prüft ob Benutzer < 5 Ausleihen hat
6. System erstellt Ausleih mit 30-Tage Frist
7. Exemplar-Status wird auf "ausgeliehen" gesetzt
8. Ausleih wird zu "Meine Liste" hinzugefügt

### UC2: Buch erfassen (Administrator)
1. Administrator loggt sich ein
2. Administrator wählt "Buch erfassen"
3. Administrator gibt ISBN, Titel, Autor, Jahr ein
4. Administrator gibt Anzahl Exemplare an
5. System prüft ob ISBN bereits existiert
6. System erstellt Buch mit Exemplaren
7. Exemplare erhalten Status "verfügbar"

### UC3: Ausleih verlängern (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer öffnet "Meine Liste"
3. Benutzer wählt auszuleihendes Buch
4. System prüft ob Verlängerung möglich (< 1x)
5. System fügt 14 Tage zur Frist hinzu
6. Ausleih-Verlängerungszähler wird erhöht

### UC4: Überfälliges Buch zurücksetzen (Administrator)
1. Administrator loggt sich ein
2. Administrator sieht überfällige Bücher
3. Administrator wählt überfälliges Exemplar
4. Administrator setzt Status auf "verfügbar"
5. System entfernt Ausleih-Eintrag
6. Exemplar ist wieder ausleihbar

### UC5: Buch zur Merkliste hinzufügen (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer findet interessantes Buch
3. Benutzer klickt "Zur Merkliste"
4. System fügt ISBN zur Merkliste hinzu
5. Buch erscheint in persönlicher Merkliste



