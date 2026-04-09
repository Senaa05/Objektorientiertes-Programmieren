# Klasse für Exemplar eines Buches
class Exemplar:
    def __init__(self, exemplar_id, buch):
        self.exemplar_id = exemplar_id
        self.buch = buch
        self.status = "verfuegbar" 
    
    # Methoden für Status des Exemplars
    def ausleihen(self):
        # Überprüfen, ob Exemplar bereits ausgeliehen ist
        if self.status == "ausgeliehen":
            raise ValueError("Exemplar ist bereits ausgeliehen")
        self.status = "ausgeliehen"

    def zurueckgeben(self):
        # Überprüfen, ob Exemplar bereits zurückgegeben ist
        if self.status == "verfuegbar":
            raise ValueError("Exemplar ist bereits zurueckgegeben")
        self.status = "verfuegbar"
