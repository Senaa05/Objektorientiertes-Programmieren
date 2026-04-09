# Klasse für Exemplar eines Buches
class Exemplar:
    def __init__(self, exemplar_id, buch):
        self.exemplar_id = exemplar_id
        self.buch = buch
        self.status = "verfuegbar" 
    
    # Methoden für Status des Exemplars
    def ausgeleihen(self):
        self.status = "ausgeliehen"

    def zurueckgeben(self):
        self.status = "verfuegbar"
