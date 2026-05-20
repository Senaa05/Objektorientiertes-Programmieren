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
- "Meine Ausleihen" mit aktuellen Ausleihen, das älteste zu oberst und das neuste zu unterst. 

### Ausleihe 
- 30 Tage Standard-Ausleihdauer
- Automatische Erinnerung bei < 7 Tagen Restlaufzeit
- Pop-up bei überfälligen Büchern
- Echtzeit-Status der Buchverfügbarkeit

## User Stories

### User Story 1: Bücher erfassen 
- Als Administrator möchte ich Bücher erfassen, damit die Bibliothek aktuell bleibt.
---
### User Story 2: Buchinformationen bearbeiten 
- Als Administrator möchte ich Buchinformationen bearbeiten können, damit Daten korrekt sind.
---
### User Story 3: Bücher löschen 
- Als Administrator möchte ich Bücher löschen, damit veraltete Medien entfernt werden.
---
### User Story 4: Bücher freigeben 
- Als Administrator möchte ich zurückgegebene Bücher wieder freigeben können, damit sie wieder ausgeliehen werden können.
---
### User Story 5: Bücher durchsuchen 
- Als Benutzer möchte ich alle Bücher durchsuchen, damit ich interessante Titel finde.
---
### User Story 6: Beliebte Bücher anzeigen 
- Als Benutzer möchte ich beliebteste Bücher sehen, damit ich weiss was gut ist.
---
### User Story 7: Bücher ausleihen 
- Als Benutzer möchte ich Bücher ausleihen, damit ich sie lesen kann.
---
### User Story 8: Ausleihe verlängern 
- Als Benutzer möchte ich Ausleihen verlängern, damit ich mehr Zeit zum Lesen habe.
---
### User Story 9: Eigene Ausleihe anzeigen
- Als Benutzer möchte ich meine Ausleihen sehen, damit ich den Überblick habe
---
### User Story 10: Bücher in die Merkliste hinzufügen 
- Als Benutzer möchte ich Bücher merken, damit ich sie später leicht finde.
---
## Use Cases
![UML Use Case Diagram](Diagramm/BibliothekUseCasesDiagramm.png)

### USE CASE 1: Registrieren (Benutzer)
1. Benutzer öffnet die Registrierungsseite
2. Benutzer gibt Benutzername, Passwort, Vorname, Nachname und E-Mail ein
3. System prüft Pflichtfelder und Validität
4. System prüft, ob Benutzername und E-Mail eindeutig sind
5. System speichert den neuen Benutzer mit Standardrolle "Benutzer"
6. Benutzer kann sich anschliessend einloggen

### USE CASE 2: Login mit rollenbasierter Ansicht (Benutzer/Admin)
1. Benutzer öffnet die Login-Seite
2. Benutzer gibt Benutzername und Passwort ein
3. System prüft die Zugangsdaten 
4. Bei korrekten Daten prüft das System die Rolle
5. Benutzer mit Rolle "Benutzer" gelangt zur Benutzeransicht
6. Benutzer mit Rolle "Admin" oder "Administrator" gelangt zur Admin-Ansicht

### USE CASE 3: Buch ausleihen (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer sucht nach einem Buch
3. System zeigt verfügbare Exemplare an
4. Benutzer wählt ein Exemplar aus
5. System prüft, ob Benutzer weniger als 5 aktive Ausleihen hat
6. System erstellt eine Ausleihe (Standardfrist 30 Tage) und speichert sie
7. Exemplar-Status wird auf "ausgeliehen" gesetzt
8. Ausleihe erscheint in "Meine Ausleihen"

### USE CASE 4: Buch erfassen (Administrator)
1. Administrator loggt sich ein
2. Administrator wählt "Buch erfassen"
3. Administrator gibt ISBN, Titel, Autor und Jahr ein
4. Administrator legt die Anzahl der Exemplare fest
5. System validiert ISBN (mind. 13 Ziffern), Jahr (4-stellig, nicht in Zukunft) und Eindeutigkeit
6. System speichert das Buch und legt Exemplare an
7. Exemplare erhalten den Status "verfügbar"

### USE CASE 5: Exemplar verwalten (Administrator)
1. Administrator loggt sich ein
2. Administrator öffnet die Exemplarverwaltung / Buchverwaltung
3. Administrator wählt ein Buch und sieht die zugehörigen Exemplare
4. Administrator kann Exemplare hinzufügen (Anzahl erhöhen)
5. Administrator kann ein Exemplar löschen (sofern nicht ausgeliehen)
6. Administrator kann den Status eines Exemplars manuell setzen (z. B. "verfügbar", "ausgeliehen")
7. System speichert die Änderungen und aktualisiert die Verfügbarkeit

### USE CASE 6: Buch löschen (Administrator)
1. Administrator loggt sich ein
2. Administrator öffnet die Buchverwaltung
3. Administrator wählt ein Buch zum Löschen aus
4. System prüft, ob das Buch existiert
5. System verhindert das Löschen, falls noch Exemplare ausgeliehen sind
6. Falls möglich, löscht das System die Exemplare und das Buch
7. Buch erscheint nicht mehr im Bestand

### USE CASE 6: Ausleih verlängern (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer öffnet "Meine Ausleihe"
3. Benutzer wählt eine aktive Ausleihe
4. System prüft, ob die Ausleihe noch verlängerbar ist (nur 1x erlaubt)
5. System verlängert die Frist um 14 Tage und speichert die Änderung

### USE CASE 7: Buch verfügbar machen (Administrator)
1. Administrator loggt sich ein
2. Administrator wählt ein zurückgegebenes Exemplar
3. System setzt den Exemplar-Status auf "verfügbar"
4. System markiert die Ausleihe als zurückgegeben
5. Exemplar ist wieder ausleihbar

### USE CASE 8: Buch zur Merkliste hinzufügen (Benutzer)
1. Benutzer loggt sich ein
2. Benutzer merkt ein Buch
3. System prüft, ob Benutzer und Buch existieren
4. System verhindert Duplikate auf der Merkliste
5. System speichert den Merkliste-Eintrag

### Akteure
- Administrator
- Benutzer

## Mockup

## Architektur
<img width="861" height="671" alt="Architektur" src="https://github.com/user-attachments/assets/f24a27e7-d921-4457-998d-bda20b477337" />

## Datenbank 

### ER-Diagramm
![ERM Diagramm](Diagramm/BibflowERM.png)
## Projektanforderungen
## Projektmanagement
| Name      | Beitrag |
|-----------|--------------|
| Sena | Backend + Dokumentation |
| Naomi | Datenbanken & ORM + Dokumentation |
| Giulia | Frontend UI + Dokumentation |

---

### Browser-Based App

### Datenvalidierung
Die Applikation stellt sicher, dass alle Eingaben und Operationen durch geeignete Validierungen geprüft werden. Diese Validierungen sind hauptsächlich in den Service-Klassen implementiert, bevor Daten in der Datenbank gespeichert und verarbeitet werden.

### 1. Benutzer
Bei der Registrierung wird geprüft, ob alle Pflichtfelder ausgefüllt sind und ob Benutzername sowie E-Mail eindeutig sind. Beim Login werden die Zugangsdaten validiert; bei Fehlern wird eine einheitliche Fehlermeldung verwendet.
### 2. Buch
In der Buchverwaltung wird sichergestellt, dass jede ISBN nur einmal existiert. Ein Buch kann nur gelöscht werden, wenn keine zugehörigen Exemplare aktuell ausgeliehen sind.
### 3. Ausleihe
Ein Benutzer darf maximal fünf Bücher gleichzeitig ausleihen. Die Standard-Ausleihdauer beträgt 30 Tage. Eine Verlängerung ist nur einmal pro Ausleihe möglich und verlängert die Frist um 14 Tage.
### 4. Merkliste
Beim Hinzufügen zur Merkliste wird geprüft, ob Benutzer und Buch existieren. Zusätzlich werden doppelte Einträge verhindert.
