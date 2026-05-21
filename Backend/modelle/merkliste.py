class MerklisteEintrag:
    def __init__(self, benutzername: str, isbn: str, hinzugefuegt_am: str = None, id=None, titel: str = None, autor: str = None, jahr=None):
        self.id = id
        self.benutzername = benutzername
        self.isbn = isbn
        self.hinzugefuegt_am = hinzugefuegt_am
        self.titel = titel
        self.autor = autor
        self.jahr = jahr

    def als_dict(self) -> dict:
        return {
            "benutzername": self.benutzername,
            "isbn": self.isbn,
            "hinzugefuegt_am": self.hinzugefuegt_am,
            "titel": self.titel,
            "autor": self.autor,
            "jahr": self.jahr
        }
