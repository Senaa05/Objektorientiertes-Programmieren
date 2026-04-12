from modelle.benutzer import User, Administrator
from modelle.buch import Buch
from modelle.exemplar import Exemplar
from modelle.ausleihe import Ausleihe

# Beispiel für die Erstellung von Benutzern, Büchern, Exemplaren und Ausleihen
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

    # Erstellen von Ausleihen
    ausleihe1 = Ausleihe(benutzer1, exemplar1)
    benutzer1.ausleihen.append(ausleihe1)

    # ausleihen
    try:
        exemplar1.ausleihen()
        print(f"{benutzer1.vorname} hat '{exemplar1.buch.titel}' ausgeliehen.")
    except ValueError as e:
        print(e)

    # Rückgabe
    try:
        ausleihe1.rueckgabe_ausleihe()
        print(f"{benutzer1.vorname} hat '{exemplar1.buch.titel}' zurückgegeben.")   
    except ValueError as e:
        print(e)

    # Verlängerung
    try:    
        ausleihe1.verlaengern_ausleihe()
        print(f"{benutzer1.vorname} hat die Ausleihe von '{exemplar1.buch.titel}' verlängert.")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()