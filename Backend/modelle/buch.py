class Buch:
    def __init__(self, titel: str, autor: str, isbn: str, jahr: int):
        # Fachmodell fuer bibliografische Kerndaten.
        self.titel = titel
        self.autor = autor
        self.isbn = isbn
        self.jahr = jahr

    def als_dict(self) -> dict:
        return {
            "titel": self.titel,
            "autor": self.autor,
            "isbn": self.isbn,
            "jahr": self.jahr
        }