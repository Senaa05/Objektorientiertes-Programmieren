from modelle.benutzer import Administrator
from modelle.benutzer import User
from modelle.buch import Buch
from modelle.exemplar import Exemplar
from services.ausleihe_service import AusleiheService
import sys
import os

# Pfad zum Hauptverzeichnis hinzufügen
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from Datenbank.DatenbankManager import DatenbankManager
except ImportError:
    # Fallback für relative Imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Datenbank.DatenbankManager import DatenbankManager

# Beispiel für die Erstellung von Benutzern, Büchern und Exemplaren
def main():
    # Datenbank-Verbindung und Services
    db = DatenbankManager()
    ausleihe_service = AusleiheService(db)
    
    # Benutzer in Datenbank speichern
    db.benutzer_speichern("lilly2", "passwort123", "Lilly", "Müller", "lilly.mueller@example.com", "Benutzer")
    db.benutzer_speichern("admin1", "adminpass", "Max", "Mustermann", "max.mustermann@example.com", "Admin")
    
    # Bücher in Datenbank speichern
    db.buch_speichern("Der Alchimist", "Paulo Coelho", "978-3-123456-78-9", 1988)
    db.buch_speichern("Die Verwandlung", "Franz Kafka", "978-3-987654-32-1", 1915)
    
    # Exemplare in Datenbank speichern
    db.exemplar_speichern("1", "978-3-123456-78-9")
    db.exemplar_speichern("2", "978-3-123456-78-9")
    db.exemplar_speichern("3", "978-3-987654-32-1")
    
    # Modelle erstellen
    benutzer1 = User("lilly2", "passwort123", "Lilly", "Müller", "lilly.mueller@example.com")
    admin1 = Administrator("admin1", "adminpass", "Max", "Mustermann", "max.mustermann@example.com")
    
    buch1 = Buch("Der Alchimist", "Paulo Coelho", "978-3-123456-78-9", 1988)
    buch2 = Buch("Die Verwandlung", "Franz Kafka", "978-3-987654-32-1", 1915)
    
    exemplar1 = Exemplar(1, buch1)
    exemplar2 = Exemplar(2, buch1)
    exemplar3 = Exemplar(3, buch2)
    
    # Hinzufügen der Exemplare zu den Büchern
    buch1.exemplare.append(exemplar1)
    buch1.exemplare.append(exemplar2)
    buch2.exemplare.append(exemplar3)
    
    print("=== Bibliothekssystem Test ===")
    print(f"Benutzer: {benutzer1.vorname} {benutzer1.nachname}")
    print(f"Bücher: {buch1.titel}, {buch2.titel}")
    print(f"Exemplare: {len(buch1.exemplare)} für '{buch1.titel}', {len(buch2.exemplare)} für '{buch2.titel}'")
    
    # Ausleihe mit Datenbank testen
    try:
        ausleihe_id = ausleihe_service.buch_ausleihen("lilly2", "978-3-123456-78-9")
        print(f"\n✅ Buch ausgeliehen! Ausleih-ID: {ausleihe_id}")
        
        # Ausleihen des Benutzers anzeigen
        ausleihen = ausleihe_service.meine_ausleihen("lilly2")
        print(f"\n📚 Ausleihen von {benutzer1.vorname}:")
        for ausleihe in ausleihen:
            print(f"  - {ausleihe['titel']} (fällig: {ausleihe['faelligkeit']})")
            
    except ValueError as e:
        print(f"\n❌ Fehler bei Ausleihe: {e}")

if __name__ == "__main__":
    main()


