from Backend.modelle.buch import Buch

class BuchService:
    """Service fuer Buchverwaltung, Suche, Verfuegbarkeit und Popularitaet."""

    def __init__(self, db):
        self.db = db

    def buch_erstellen(
        self,
        titel: str,
        autor: str,
        isbn: str,
        jahr: int,
        exemplar_anzahl: int = 1
    ) -> bool:
        """Erstellt ein neues Buch und legt die gewuenschte Anzahl Exemplare an."""
        # ISBN muss eindeutig sein.
        bestehendes_buch = self.db.buch_laden(isbn)
        if bestehendes_buch:
            raise ValueError("Ein Buch mit dieser ISBN existiert bereits.")

        if exemplar_anzahl < 1:
            raise ValueError("Ein Buch muss mindestens 1 Exemplar haben.")

        erfolg = self.db.buch_speichern(titel, autor, isbn, jahr)
        if not erfolg:
            raise ValueError("Buch konnte nicht gespeichert werden.")

        # Beim Erfassen werden die Exemplare direkt mitangelegt.
        exemplar_erfolg = self.db.exemplare_fuer_buch_anlegen(isbn, exemplar_anzahl)
        if not exemplar_erfolg:
            raise ValueError("Exemplare konnten nicht erstellt werden.")

        return True

    def buch_laden(self, isbn: str) -> Buch:
        """Laedt ein Buch anhand der ISBN als Buch-Objekt."""
        daten = self.db.buch_laden(isbn)
        if not daten:
            raise ValueError("Buch nicht gefunden.")

        return Buch(**daten)

    def alle_buecher(self) -> list[Buch]:
        """Gibt den gesamten Buchbestand als Objektliste zurueck."""
        daten_liste = self.db.alle_buecher_laden()
        return [Buch(**daten) for daten in daten_liste]

    def buecher_suchen(self, suchbegriff: str) -> list[Buch]:
        """Sucht Buecher ueber Titel, Autor oder ISBN."""
        # Leerer Suchbegriff liefert den Gesamtbestand.
        if not suchbegriff or not suchbegriff.strip():
            return self.alle_buecher()

        daten_liste = self.db.bucher_suchen(suchbegriff.strip())
        return [Buch(**daten) for daten in daten_liste]

    def buch_bearbeiten(
        self,
        isbn: str,
        titel: str = None,
        autor: str = None,
        jahr: int = None
    ) -> bool:
        """Aktualisiert einzelne Buchfelder; nicht angegebene Felder bleiben unveraendert."""
        bestehendes_buch = self.db.buch_laden(isbn)
        if not bestehendes_buch:
            raise ValueError("Buch nicht gefunden.")

        erfolg = self.db.buch_bearbeiten(
            isbn=isbn,
            titel=titel,
            autor=autor,
            jahr=jahr
        )

        if not erfolg:
            raise ValueError("Buch konnte nicht bearbeitet werden.")

        return True

    def buch_loeschen(self, isbn: str) -> bool:
        """Loescht ein Buch, sofern keine aktive Ausleihe dagegen spricht."""
        bestehendes_buch = self.db.buch_laden(isbn)
        if not bestehendes_buch:
            raise ValueError("Buch nicht gefunden.")

        erfolg = self.db.buch_loeschen(isbn)
        if not erfolg:
            raise ValueError("Buch konnte nicht gelöscht werden. Es ist möglicherweise noch ausgeliehen.")

        return True

    def verfuegbare_exemplare(self, isbn: str) -> list[dict]:
        """Liefert alle aktuell verfuegbaren Exemplare eines Buches."""
        buch = self.db.buch_laden(isbn)
        if not buch:
            raise ValueError("Buch nicht gefunden.")

        return self.db.verfuegbare_exemplare(isbn)

    def ist_buch_verfuegbar(self, isbn: str) -> bool:
        """True, wenn mindestens ein verfuegbares Exemplar existiert."""
        verfuegbare = self.verfuegbare_exemplare(isbn)
        return len(verfuegbare) > 0

    def beliebteste_buecher(self, limit: int = 5):
        """Gibt die am meisten ausgeliehenen Buecher in absteigender Reihenfolge zurueck."""
        # Datenbasis fuer die Startseite "Beliebteste Buecher".
        if limit < 1:
            raise ValueError("Limit muss mindestens 1 sein.")
        return self.db.beliebteste_buecher_laden(limit)