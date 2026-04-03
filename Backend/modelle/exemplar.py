# Klasse für Exemplar eines Buches
class Exemplar:
    def __init__(self, buch, exemplar_id):
        self.buch = buch
        self.exemplar_id = exemplar_id
        self.status = "verfuegbar" 
    
    # Methoden für Status des Exemplars
    def ausgeliehen(self):
        pass

    def zurueckgegeben(self):
        pass

    