# Bibflow :books:

Gruppenmitglieder: Sena Besir, Giulia Falone, Naomi Uwensuyi 
Dozierende: Felix Härer, Grieder Hermann

Dieses Projekt ist ein webbasiertes Bibliothekssystem, das die Verwaltung und Ausleihe von Büchern übersichtlich und effizient gestaltet. Unterschiedliche Funktionen für Administratoren und Benutzer sorgen für eine klare und strukturierte Nutzung.

## Problem
In der Bibliothek «Bibflow» ist die Verwaltung der Bücher und Ausleihen unübersichtlich, weil keine zentrale Lösung vorhanden ist. Benutzer wissen oft nicht, ob ein Buch verfügbar ist, und haben keinen Überblick über ihre Ausleihen. Zudem ist den Benutzern nicht bewusst, welche die beliebtesten Bücher in der Bibliothek sind. Dies führt häufig zu verspäteten Rückgaben und Missverständnissen zwischen Benutzern und Mitarbeitern.

## Szenario
Benutzer verwenden diese Applikation, wenn sie Bücher ausleihen möchten und den Überblick über ihre Ausleihen behalten wollen. Bei Bedarf können die Ausleihen verlängert werden. Dadurch wird das Problem der unübersichtlichen Verwaltung von Büchern und Ausleihen gelöst.

## Hauptfunktionen

### Administrator
- Bücher erfassen, bearbeiten und löschen
- Verfügbarkeit von Exemplaren verwalten
- Überfällige Bücher einen Reminder auslösen

### Benutzer
- Alle Bücher durchsuchen und anzeigen
- Beliebteste Bücher sehen auf der Startseite
- Bis zu 5 Bücher gleichzeitig ausleihen
- Man kann pro Buch 1x verlängern
- (Persönliche Merkliste verwalten)
- "Meine Ausleihe" mit aktuellen Ausleihen, das älteste zu oberst und das neuste zu unterst. 

### Ausleihe 
- 30 Tage Standard-Ausleihdauer
- Automatische Erinnerung bei < 7 Tagen Restlaufzeit
- Pop-up bei überfälligen Büchern
- Echtzeit-Status der Buchverfügbarkeit

## User Stories

### User Story 1: Bücher erfassen 
- Als Administrator möchte ich Bücher erfassen, damit die Bibliothek aktuell bleibt.

### User Story 2: Buchinformationen bearbeiten 
- Als Administrator möchte ich Buchinformationen bearbeiten können, damit Daten korrekt sind.

### User Story 3: Bücher löschen 
- Als Administrator möchte ich Bücher löschen, damit veraltete Medien entfernt werden.

### User Story 4: Bücher freigeben 
- Als Administrator möchte ich zurückgegebene Bücher wieder freigeben können, damit sie wieder ausgeliehen werden können.

### User Story 5: Bücher durchsuchen 
- Als Benutzer möchte ich alle Bücher durchsuchen, damit ich interessante Titel finde.

### User Story 6: Beliebte Bücher anzeigen 
- Als Benutzer möchte ich beliebteste Bücher sehen, damit ich weiss was gut ist.

### User Story 7: Bücher ausleihen 
- Als Benutzer möchte ich Bücher ausleihen, damit ich sie lesen kann.

### User Story 8: Ausleihe verlängern 
- Als Benutzer möchte ich Ausleihen verlängern, damit ich mehr Zeit zum Lesen habe.

### User Story 9: Eigene Ausleihe anzeigen
- Als Benutzer möchte ich meine Ausleihen sehen, damit ich den Überblick habe

### User Story 10: Bücher in die Merkliste hinzufügen 
- Als Benutzer möchte ich Bücher merken, damit ich sie später leicht finde.

## Use Cases

### USE CASE 1: Buch ausleihen (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer sucht nach einem Buch
3. System zeigt verfügbare Exemplare
4. Benutzer wählt ein Exemplar aus
5. System prüft ob Benutzer weniger als 5 Ausleihen hat
6. System erstellt Ausleih mit 30-Tage Frist
7. Exemplar-Status wird auf "ausgeliehen" gesetzt
8. Ausleih wird zu "Meine Ausleihe" hinzugefügt

### USE CASE 2: Buch erfassen (Administrator)
1. Administrator loggt sich ein
2. Administrator wählt "Buch erfassen"
3. Administrator gibt ISBN, Titel, Autor, Jahr ein
4. Administrator gibt Anzahl Exemplare an
5. System prüft ob ISBN bereits existiert
6. System erstellt Buch mit Exemplaren
7. Exemplare erhalten Status "verfügbar"

### USE CASE 3: Ausleih verlängern (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer öffnet "Meine Ausleihe"
3. Benutzer wählt auszuleihendes Buch
4. System prüft ob Verlängerung möglich (< 1x)
5. System fügt 14 Tage zur Frist hinzu
6. Ausleih-Verlängerungszähler wird erhöht

### USE CASE 4: Zurückgegebenes Buch wieder verfügbar machen (Administrator)
1. Administrator loggt sich ein
2. Administrator sieht zurückgegebene Bücher
3. Administrator wählt zurückgegebenes Exemplar
4. Administrator setzt Status auf "verfügbar"
5. System entfernt Ausleih-Eintrag
6. Exemplar ist wieder ausleihbar

### USE CASE 5: Buch zur Merkliste hinzufügen (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer findet interessantes Buch
3. Benutzer klickt "Zur Merkliste"
4. System fügt Buch zur Merkliste hinzu
5. Buch erscheint in persönlicher Merkliste

### Akteure
- Administrator
- Benutzer

## Mockup

## Architektur

