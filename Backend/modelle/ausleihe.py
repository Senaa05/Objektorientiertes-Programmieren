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
        self.verlaengerungsanzahl = 0
        self.rueckgabedatum = None
        
    # Methode für Verlängerung der Ausleihe
    def verlaengern_ausleihe(self):
        # Überprüfen, ob die Ausleihe bereits verlängert wurde
        if self.verlaengerungsanzahl >= 1:
            raise ValueError("Ausleihe kann nur einmal verlängert werden")
        # Verlängerung um weitere 14 Tage
        self.faelligkeit += timedelta(days=14)
        self.verlaengerungsanzahl += 1

    # Methode für Rückgabe der Ausleihe
    def rueckgabe_ausleihe(self):
        # Überprüfen, ob die Ausleihe bereits zurückgegeben wurde
        if self.rueckgabedatum is not None:
            raise ValueError("Ausleihe wurde bereits zurückgegeben")
        self.rueckgabedatum = date.today()
        self.exemplar.zurueckgeben()
    
