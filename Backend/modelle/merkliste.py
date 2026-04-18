class MerklisteEintrag:
    def __init__(self, benutzername: str, isbn: str, hinzugefuegt_am: str = None):
        self.benutzername = benutzername
        self.isbn = isbn
        self.hinzugefuegt_am = hinzugefuegt_am

    def als_dict(self) -> dict:
        return {
            "benutzername": self.benutzername,
            "isbn": self.isbn,
            "hinzugefuegt_am": self.hinzugefuegt_am
        }
