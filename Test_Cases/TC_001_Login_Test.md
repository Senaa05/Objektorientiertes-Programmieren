# Test Case: Login-Funktionalität

## 1. Test Case ID
**TC_001**

## 2. Test Case Titel/Beschreibung
**Benutzer-Login-Authentifizierung - Überprüfen, dass Benutzer sich erfolgreich mit gültigen Anmeldedaten authentifizieren und auf das Bibliotheks-Dashboard zugreifen können.**

## 3. Voraussetzungen
- NiceGUI-Anwendung läuft auf http://127.0.0.1:8080
- Datenbank enthält Test-Benutzer:
  - Benutzername: "lilly2", Rolle: "Benutzer"
  - Benutzername: "admin1", Rolle: "Admin"
- Mock-Datenbank ist korrekt initialisiert
- Web-Browser ist verfügbar und kann auf die Anwendungs-URL zugreifen

## 4. Test-Schritte
1. Web-Browser öffnen und zu http://127.0.0.1:8080 navigieren
2. Überprüfen, dass die Login-Seite angezeigt wird mit:
   - Titel "📚 Bibliothek"
   - Benutzername-Eingabefeld
   - Passwort-Eingabefeld
   - "Anmelden"-Button
   - Test-Kontoinformationen angezeigt
3. Gültigen Benutzernamen "lilly2" im Benutzernamen-Feld eingeben
4. Beliebiges Passwort eingeben (da Mock-Datenbank jedes Passwort für Test-Benutzer akzeptiert)
5. Auf "Anmelden"-Button klicken
6. Erfolgreiche Navigation zur Dashboard-Seite überprüfen
7. Überprüfen, dass Benutzerinformationen im Header angezeigt werden
8. Überprüfen, dass entsprechende Tabs basierend auf der Benutzerrolle sichtbar sind

## 5. Test-Daten/Eingabe
- **Gültiger Test-Benutzer 1:**
  - Benutzername: "lilly2"
  - Passwort: "test123" (beliebiges Passwort funktioniert im Mock)
  - Erwartete Rolle: "Benutzer"
  
- **Gültiger Test-Benutzer 2:**
  - Benutzername: "admin1" 
  - Passwort: "admin123" (beliebiges Passwort funktioniert im Mock)
  - Erwartete Rolle: "Admin"

- **Ungültige Test-Daten:**
  - Benutzername: "nichtvorhanden"
  - Passwort: "beliebigespasswort"

## 6. Erwartetes Ergebnis
**Bei gültigen Anmeldedaten:**
- Login erfolgreich ohne Fehler
- Benutzer wird zur Seite /dashboard weitergeleitet
- Header zeigt: "📚 Bibliothek" und Benutzerinformationen
- Benutzerrolle wird korrekt identifiziert und angewendet
- Entsprechende Navigations-Tabs werden angezeigt:
  - Für "Benutzer": "Bücher" und "Meine Ausleihen" Tabs
  - Für "Admin": "Bücher", "Meine Ausleihen" und "Admin" Tabs
- Keine Fehlermeldungen werden angezeigt

**Bei ungültigen Anmeldedaten:**
- Login schlägt fehl
- Benutzer bleibt auf der Login-Seite
- Entsprechende Fehlermeldung wird angezeigt
- Kein Zugriff auf das Dashboard wird gewährt

## 7. Tatsächliches Ergebnis
*Während der Testausführung auszufüllen*

## 8. Status
*Nach der Testausführung zu markieren*
- [ ] BESTANDEN
- [ ] FEHLGESCHLAGEN

## 9. Kommentare
**Test-Umgebung:**
- Browser: Chrome/Firefox/Safari
- OS: macOS
- Anwendungsversion: v1.0
- Test-Datum: [Datum der Ausführung]

**Zusätzliche Hinweise:**
- Mock-Datenbank akzeptiert jedes Passwort für vorhandene Benutzer
- Test-Konten sind in der UI-Anwendung hartcodiert
- Sitzungsverwaltung sollte überprüft werden (Benutzer bleibt beim Navigieren angemeldet)
- UI-Responsivität sollte auf verschiedenen Bildschirmgrößen überprüft werden
- Fehlerbehandlung sollte mit verschiedenen ungültigen Eingaben getestet werden

**Bekannte Probleme:**
- Passwort-Validierung wird in Mock-Implementierung umgangen
- Keine Passwort-Hashing in Test-Umgebung implementiert
- Sitzungs-Timeout in aktueller Version nicht implementiert

**Gefundene Fehler:**
*Zu dokumentieren, wenn bei der Tests Probleme entdeckt werden*
