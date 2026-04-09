# Klasse erstellen für Buch
class Buch:
    def __init__(self, titel, autor, isbn, jahr):
        self.titel = titel
        self.autor = autor
        self.isbn = isbn
        self.jahr = jahr
        self.exemplare = []   

    # Methode verfügbare Exemplare eines Buches zurückgeben
    def verfuegbare_exemplare(self):
        return [e for e in self.exemplare if e.status == "verfuegbar"]
    
    def ist_verfuegbar(self):
        return len(self.verfuegbare_exemplare()) > 0        