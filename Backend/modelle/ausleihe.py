# Bestimmte Funktionen des Moduls DateTime importieren
from datetime import date, timedelta
# Klasse für Buch Ausleihe
class Ausleihe:
    def __init__(self, user, exemplar):
        self.user = user
        self.exemplar = exemplar
        # Ausleihdatum als den heutigen Datum festlegen
        self.ausleihdatum = date.today()
        # Fälligkeit des Buches in 30 Tagen
        self.faelligkeit = self.ausleihdatum + timedelta(days=30)
        self.verlaengern = 0
        self.rueckgabedatum = None
        
      
