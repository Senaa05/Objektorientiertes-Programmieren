# Klasse erstellen für Buch
class Buch:
    def __init__(self, titel, autor, isbn, jahr):
        self.titel = titel
        self.autor = autor
        self.isbn = isbn
        self.jahr = jahr
        self.exemplare = []   