from Backend.modelle.merkliste import MerklisteEintrag


class MerklisteService:
    """Service fuer persoenliche Merklisten der Benutzer."""

    def __init__(self, db):
        self.db = db

    def zur_merkliste_hinzufuegen(self, benutzername: str, isbn: str) -> bool:
        """Fuegt ein Buch zur Merkliste hinzu, falls es noch nicht vorhanden ist."""
        # Vor dem Speichern wird geprueft, ob Nutzer und Buch existieren.
        benutzer = self.db.benutzer_laden(benutzername)
        if not benutzer:
            raise ValueError("Benutzer nicht gefunden.")

        buch = self.db.buch_laden(isbn)
        if not buch:
            raise ValueError("Buch nicht gefunden.")

        if hasattr(self.db, "merkliste_eintrag_laden"):
            # Duplikate auf der Merkliste verhindern.
            bestehend = self.db.merkliste_eintrag_laden(benutzername, isbn)
            if bestehend:
                raise ValueError("Buch ist bereits auf der Merkliste.")

        if not hasattr(self.db, "merkliste_eintrag_speichern"):
            raise NotImplementedError(
                "Für die Merkliste fehlt die DB-Methode merkliste_eintrag_speichern(benutzername, isbn)."
            )

        erfolg = self.db.merkliste_eintrag_speichern(benutzername, isbn)
        if not erfolg:
            raise ValueError("Buch konnte nicht zur Merkliste hinzugefügt werden.")

        return True

    def merkliste_anzeigen(self, benutzername: str):
        """Liefert alle Merkliste-Eintraege eines Benutzers als Objekte."""
        # Gibt alle gespeicherten Merkliste-Eintraege fuer einen Benutzer zurueck.
        benutzer = self.db.benutzer_laden(benutzername)
        if not benutzer:
            raise ValueError("Benutzer nicht gefunden.")

        if not hasattr(self.db, "merkliste_benutzer_laden"):
            raise NotImplementedError(
                "Für die Merkliste fehlt die DB-Methode merkliste_benutzer_laden(benutzername)."
            )

        daten_liste = self.db.merkliste_benutzer_laden(benutzername)
        return [MerklisteEintrag(**daten) for daten in daten_liste]

    def aus_merkliste_entfernen(self, benutzername: str, isbn: str) -> bool:
        """Entfernt ein Buch aus der Merkliste eines Benutzers."""
        if not hasattr(self.db, "merkliste_eintrag_loeschen"):
            raise NotImplementedError(
                "Für die Merkliste fehlt die DB-Methode merkliste_eintrag_loeschen(benutzername, isbn)."
            )

        erfolg = self.db.merkliste_eintrag_loeschen(benutzername, isbn)
        if not erfolg:
            raise ValueError("Buch konnte nicht aus der Merkliste entfernt werden.")

        return True

    def merkliste_laden(self, benutzername: str) -> list[dict]:
        daten_liste = self.merkliste_anzeigen(benutzername)
        return [
            {
                "benutzername": eintrag.benutzername,
                "isbn": eintrag.isbn,
                "hinzugefuegt_am": eintrag.hinzugefuegt_am,
                "titel": eintrag.titel,
                "autor": eintrag.autor,
                "jahr": eintrag.jahr,
            }
            for eintrag in daten_liste
        ]

    def merkliste_hinzufuegen(self, benutzername: str, isbn: str) -> bool:
        """Fügt ein Buch zur Merkliste hinzu."""
        return self.zur_merkliste_hinzufuegen(benutzername, isbn)

    def merkliste_entfernen(self, benutzername: str, isbn: str) -> bool:
        """Entfernt ein Buch aus der Merkliste."""
        return self.aus_merkliste_entfernen(benutzername, isbn)
