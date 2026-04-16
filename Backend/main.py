from modelle.benutzer import Administrator
from modelle.benutzer import User
from modelle.buch import Buch
from modelle.exemplar import Exemplar
from services.ausleihe_service import AusleiheService


# Beispiel für die Erstellung von Benutzern, Büchern und Exemplaren
def main():
    # Erstellen von Benutzern
    benutzer1 = User("lilly2", "passwort123", "Lilly", "Müller", "lilly.mueller@example.com")
    admin1 = Administrator("admin1", "adminpass", "Max", "Mustermann", "max.mustermann@example.com")

    # Erstellen von Büchern
    buch1 = Buch("Der Alchimist", "Paulo Coelho", "978-3-123456-78-9", 1988)
    buch2 = Buch("Die Verwandlung", "Franz Kafka", "978-3-987654-32-1", 1915)

    # Erstellen von Exemplaren
    exemplar1 = Exemplar(1, buch1)
    exemplar2 = Exemplar(2, buch1)
    exemplar3 = Exemplar(3, buch2)

    # Hinzufügen der Exemplare zu den Büchern
    buch1.exemplare.append(exemplar1)
    buch1.exemplare.append(exemplar2)
    buch2.exemplare.append(exemplar3)

    # Service erstellen
    service = AusleiheService()

    # Ausleihe testen
    try:
        ausleihe = service.ausleihen(benutzer1, buch1)
        print(f"{benutzer1.vorname} hat '{ausleihe.exemplar.buch.titel}' ausgeliehen.")
        print(f"Exemplar-ID: {ausleihe.exemplar.exemplar_id}")
        print(f"Status: {ausleihe.exemplar.status}")
        print(f"Fällig am: {ausleihe.faelligkeit}")
    except ValueError as e:
        print(e)

    # Ausleihe testen, wenn das gleiche Buch bereits ausgeliehen wurde
    try:
        service.ausleihen(benutzer1, buch1)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()


