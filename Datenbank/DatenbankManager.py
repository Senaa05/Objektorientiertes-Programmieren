
import sqlite3
from datetime import date, timedelta
from typing import List, Dict, Optional

class DatenbankManager:
    def __init__(self, db_path: str = "bibliothek.db"):
        self.db_path = db_path
        self.connection = None
        self.verbinden()
        self.tabellen_erstellen()
    
    def verbinden(self):
        """Stellt Verbindung zur SQLite-Datenbank her"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Ermöglicht Dictionary-Zugriff
            print(f"Datenbank verbunden: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Datenbank-Fehler: {e}")
    
    def tabellen_erstellen(self):
        """Erstellt alle notwendigen Tabellen basierend auf Backend-Modellen"""
        cursor = self.connection.cursor()
        
        # Bücher-Tabelle (basierend auf Backend/modelle/buch.py)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buecher (
                isbn TEXT PRIMARY KEY,
                titel TEXT NOT NULL,
                autor TEXT NOT NULL,
                jahr INTEGER NOT NULL
            )
        ''')
        
        # Exemplare-Tabelle (basierend auf Backend/modelle/exemplar.py)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exemplare (
                exemplar_id TEXT PRIMARY KEY,
                isbn TEXT NOT NULL,
                status TEXT DEFAULT 'verfuegbar',
                FOREIGN KEY (isbn) REFERENCES buecher(isbn)
            )
        ''')
        
        # Benutzer-Tabelle (basierend auf Backend/modelle/benutzer.py)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benutzer (
                benutzername TEXT PRIMARY KEY,
                passwort TEXT NOT NULL,
                vorname TEXT NOT NULL,
                nachname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                rolle TEXT DEFAULT 'Benutzer'
            )
        ''')
        
        # Ausleihen-Tabelle (basierend auf Backend/modelle/ausleihe.py)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ausleihen (
                ausleih_id TEXT PRIMARY KEY,
                benutzername TEXT NOT NULL,
                exemplar_id TEXT NOT NULL,
                ausleihdatum TEXT NOT NULL,
                faelligkeit TEXT NOT NULL,
                rueckgabedatum TEXT,
                verlaengerungsanzahl INTEGER DEFAULT 0,
                FOREIGN KEY (benutzername) REFERENCES benutzer(benutzername),
                FOREIGN KEY (exemplar_id) REFERENCES exemplare(exemplar_id)
            )
        ''')
        
        # Merkliste-Tabelle (für persönliche Merklisten)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS merkliste (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                benutzername TEXT NOT NULL,
                isbn TEXT NOT NULL,
                hinzugefuegt_am TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (benutzername) REFERENCES benutzer(benutzername),
                FOREIGN KEY (isbn) REFERENCES buecher(isbn),
                UNIQUE(benutzername, isbn)
            )
        ''')
        
        self.connection.commit()
        print("Tabellen erstellt/überprüft")
    
    # ==================== BÜCHER-CRUD ====================
    
    def buch_speichern(self, titel: str, autor: str, isbn: str, jahr: int) -> bool:
        """Speichert ein neues Buch in der Datenbank"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO buecher (titel, autor, isbn, jahr)
                VALUES (?, ?, ?, ?)
            ''', (titel, autor, isbn, jahr))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim Speichern des Buches: {e}")
            return False
    
    def buch_laden(self, isbn: str) -> Optional[Dict]:
        """Lädt ein Buch anhand der ISBN"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM buecher WHERE isbn = ?', (isbn,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def alle_buecher_laden(self) -> List[Dict]:
        """Lädt alle Bücher aus der Datenbank"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM buecher ORDER BY titel')
        return [dict(row) for row in cursor.fetchall()]
    
    def bucher_suchen(self, suchbegriff: str) -> List[Dict]:
        """Sucht Bücher nach Titel, Autor oder ISBN"""
        cursor = self.connection.cursor()
        suchbegriff = f"%{suchbegriff}%"
        cursor.execute('''
            SELECT * FROM buecher 
            WHERE titel LIKE ? OR autor LIKE ? OR isbn LIKE ?
            ORDER BY titel
        ''', (suchbegriff, suchbegriff, suchbegriff))
        return [dict(row) for row in cursor.fetchall()]
    
    def buch_bearbeiten(self, isbn: str, titel: str = None, autor: str = None, jahr: int = None) -> bool:
        """Aktualisiert Buch-Informationen"""
        try:
            cursor = self.connection.cursor()
            updates = []
            params = []
            
            if titel:
                updates.append("titel = ?")
                params.append(titel)
            if autor:
                updates.append("autor = ?")
                params.append(autor)
            if jahr:
                updates.append("jahr = ?")
                params.append(jahr)
            
            if updates:
                params.append(isbn)
                cursor.execute(f'''
                    UPDATE buecher SET {", ".join(updates)}
                    WHERE isbn = ?
                ''', params)
                self.connection.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Fehler beim Bearbeiten des Buches: {e}")
            return False
    
    def buch_loeschen(self, isbn: str) -> bool:
        """Löscht ein Buch und alle zugehörigen Exemplare"""
        try:
            cursor = self.connection.cursor()
            
            # Prüfen, ob Exemplare ausgeliehen sind
            cursor.execute('''
                SELECT COUNT(*) FROM exemplare 
                WHERE isbn = ? AND status = 'ausgeliehen'
            ''', (isbn,))
            if cursor.fetchone()[0] > 0:
                return False  # Kann nicht gelöscht werden, noch ausgeliehen
            
            # Exemplare löschen
            cursor.execute('DELETE FROM exemplare WHERE isbn = ?', (isbn,))
            
            # Buch löschen
            cursor.execute('DELETE FROM buecher WHERE isbn = ?', (isbn,))
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen des Buches: {e}")
            return False
    
    # ==================== EXEMPLARE-CRUD ====================
    
    def exemplar_speichern(self, exemplar_id: str, isbn: str) -> bool:
        """Speichert ein neues Exemplar"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO exemplare (exemplar_id, isbn)
                VALUES (?, ?)
            ''', (exemplar_id, isbn))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim Speichern des Exemplars: {e}")
            return False
    
    def exemplare_laden(self, isbn: str) -> List[Dict]:
        """Lädt alle Exemplare eines Buches"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM exemplare 
            WHERE isbn = ? 
            ORDER BY exemplar_id
        ''', (isbn,))
        return [dict(row) for row in cursor.fetchall()]
    
    def verfuegbare_exemplare(self, isbn: str) -> List[Dict]:
        """Gibt verfügbare Exemplare zurück (ähnlich wie Buch.verfuegbare_exemplare())"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM exemplare 
            WHERE isbn = ? AND status = 'verfuegbar'
            ORDER BY exemplar_id
        ''', (isbn,))
        return [dict(row) for row in cursor.fetchall()]
    
    def exemplar_status_aktualisieren(self, exemplar_id: str, status: str) -> bool:
        """Aktualisiert den Status eines Exemplars"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE exemplare 
                SET status = ?
                WHERE exemplar_id = ?
            ''', (status, exemplar_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Fehler beim Aktualisieren des Exemplar-Status: {e}")
            return False
    
    # ==================== BENUTZER-CRUD ====================
    
    def benutzer_speichern(self, benutzername: str, passwort: str, vorname: str, 
                         nachname: str, email: str, rolle: str = "Benutzer") -> bool:
        """Speichert einen neuen Benutzer"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO benutzer (benutzername, passwort, vorname, nachname, email, rolle)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (benutzername, passwort, vorname, nachname, email, rolle))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim Speichern des Benutzers: {e}")
            return False
    
    def benutzer_laden(self, benutzername: str) -> Optional[Dict]:
        """Lädt einen Benutzer anhand des Benutzernamens"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM benutzer WHERE benutzername = ?', (benutzername,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def benutzer_mit_email_laden(self, email: str) -> Optional[Dict]:
        """Lädt einen Benutzer anhand der E-Mail"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM benutzer WHERE email = ?', (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def alle_benutzer_laden(self) -> List[Dict]:
        """Lädt alle Benutzer"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM benutzer ORDER BY nachname, vorname')
        return [dict(row) for row in cursor.fetchall()]
    
    # ==================== AUSLEIHEN-CRUD ====================
    
    def ausleih_speichern(self, ausleih_id: str, benutzername: str, exemplar_id: str, 
                         ausleihdatum: str, faelligkeit: str) -> bool:
        """Speichert eine neue Ausleihe"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO ausleihen (ausleih_id, benutzername, exemplar_id, ausleihdatum, faelligkeit)
                VALUES (?, ?, ?, ?, ?)
            ''', (ausleih_id, benutzername, exemplar_id, ausleihdatum, faelligkeit))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim Speichern der Ausleihe: {e}")
            return False
    
    def ausleih_laden(self, ausleih_id: str) -> Optional[Dict]:
        """Lädt eine Ausleihe anhand der ID"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM ausleihen WHERE ausleih_id = ?', (ausleih_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def ausleihen_benutzer(self, benutzername: str) -> List[Dict]:
        """Lädt alle Ausleihen eines Benutzers"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT a.*, e.isbn, b.titel, b.autor
            FROM ausleihen a
            JOIN exemplare e ON a.exemplar_id = e.exemplar_id
            JOIN buecher b ON e.isbn = b.isbn
            WHERE a.benutzername = ?
            ORDER BY a.faelligkeit
        ''', (benutzername,))
        return [dict(row) for row in cursor.fetchall()]
    
    def anzahl_ausleihen_benutzer(self, benutzername: str) -> int:
        """Gibt die Anzahl der aktuellen Ausleihen eines Benutzers zurück"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM ausleihen 
            WHERE benutzername = ? AND rueckgabedatum IS NULL
        ''', (benutzername,))
        return cursor.fetchone()[0]
    
    def ueberfaellige_ausleihen(self) -> List[Dict]:
        """Gibt alle überfälligen Ausleihen zurück"""
        cursor = self.connection.cursor()
        heute = date.today().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT a.*, b.vorname, b.nachname, b.email, e.isbn, bu.titel
            FROM ausleihen a
            JOIN benutzer b ON a.benutzername = b.benutzername
            JOIN exemplare e ON a.exemplar_id = e.exemplar_id
            JOIN buecher bu ON e.isbn = bu.isbn
            WHERE a.faelligkeit < ? AND a.rueckgabedatum IS NULL
            ORDER BY a.faelligkeit
        ''', (heute,))
        return [dict(row) for row in cursor.fetchall()]
    
    def ausleih_verlaengern(self, ausleih_id: str, neue_faelligkeit: str) -> bool:
        """Verlängert eine Ausleihe"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE ausleihen 
                SET faelligkeit = ?, verlaengerungsanzahl = verlaengerungsanzahl + 1
                WHERE ausleih_id = ?
            ''', (neue_faelligkeit, ausleih_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Fehler beim Verlängern der Ausleihe: {e}")
            return False
    
    def ausleih_rueckgabe(self, ausleih_id: str) -> bool:
        """Verarbeitet die Rückgabe einer Ausleihe"""
        try:
            cursor = self.connection.cursor()
            heute = date.today().strftime('%Y-%m-%d')
            
            # Zuerst das Exemplar-Status aktualisieren
            cursor.execute('''
                UPDATE exemplare 
                SET status = 'verfuegbar'
                WHERE exemplar_id = (SELECT exemplar_id FROM ausleihen WHERE ausleih_id = ?)
            ''', (ausleih_id,))
            
            # Dann die Ausleihe als zurückgegeben markieren
            cursor.execute('''
                UPDATE ausleihen 
                SET rueckgabedatum = ?
                WHERE ausleih_id = ?
            ''', (heute, ausleih_id))
            
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Fehler bei der Ausleih-Rückgabe: {e}")
            return False
    
    # ==================== MERKLISTE-CRUD ====================
    
    def merkliste_hinzufuegen(self, benutzername: str, isbn: str) -> bool:
        """Fügt ein Buch zur Merkliste hinzu"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO merkliste (benutzername, isbn)
                VALUES (?, ?)
            ''', (benutzername, isbn))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen zur Merkliste: {e}")
            return False
    
    def merkliste_laden(self, benutzername: str) -> List[Dict]:
        """Lädt die Merkliste eines Benutzers"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT m.*, b.titel, b.autor, b.jahr
            FROM merkliste m
            JOIN buecher b ON m.isbn = b.isbn
            WHERE m.benutzername = ?
            ORDER BY m.hinzugefuegt_am DESC
        ''', (benutzername,))
        return [dict(row) for row in cursor.fetchall()]
    
    def merkliste_entfernen(self, benutzername: str, isbn: str) -> bool:
        """Entfernt ein Buch aus der Merkliste"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                DELETE FROM merkliste 
                WHERE benutzername = ? AND isbn = ?
            ''', (benutzername, isbn))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Fehler beim Entfernen aus der Merkliste: {e}")
            return False
    
    def schliessen(self):
        """Schließt die Datenbankverbindung"""
        if self.connection:
            self.connection.close()
            print("Datenbankverbindung geschlossen")
    
    def __del__(self):
        """Destructor - schließt Verbindung automatisch"""
        self.schliessen()