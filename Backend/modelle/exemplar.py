class Exemplar:
    def __init__(self, exemplar_id: str, isbn: str, status: str = "verfuegbar"):
        # Reales Exemplar eines Buches mit eigenem Status.
        self.exemplar_id = exemplar_id
        self.isbn = isbn
        self.status = status

    def ist_verfuegbar(self) -> bool:
        return self.status == "verfuegbar"

    def als_dict(self) -> dict:
        return {
            "exemplar_id": self.exemplar_id,
            "isbn": self.isbn,
            "status": self.status
        }