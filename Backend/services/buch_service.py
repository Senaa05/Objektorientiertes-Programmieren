from Backend.modelle.buch import Buch
from datetime import date

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
        jahr_text = str(jahr).strip()
        aktuelles_jahr = date.today().year
        if len(jahr_text) != 4 or not jahr_text.isdigit():
            raise ValueError("Jahr muss genau 4 Ziffern enthalten.")
        jahr_int = int(jahr_text)
        if jahr_int < 1000:
            raise ValueError("Ein Buch muss mindestens 1000 sein.")
        if jahr_int > aktuelles_jahr:
            raise ValueError(f"Jahr darf nicht in der Zukunft liegen (max. {aktuelles_jahr}).")

        if sum(1 for z in (isbn or "") if z.isdigit()) < 13:
            raise ValueError("ISBN muss mindestens 13 Ziffern enthalten.")
        
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

    def buch_speichern(self, titel: str, autor: str, isbn: str, jahr: int) -> bool:
        """Wrapper für das direkte Speichern eines Buches in der DB."""
        jahr_text = str(jahr).strip()
        aktuelles_jahr = date.today().year
        if len(jahr_text) != 4 or not jahr_text.isdigit():
            raise ValueError("Jahr muss genau 4 Ziffern enthalten.")
        jahr_int = int(jahr_text)
        if jahr_int < 1000:
            raise ValueError("Ein Buch muss mindestens 1000 sein.")
        if jahr_int > aktuelles_jahr:
            raise ValueError(f"Jahr darf nicht in der Zukunft liegen (max. {aktuelles_jahr}).")

        if sum(1 for z in (isbn or "") if z.isdigit()) < 13:
            raise ValueError("ISBN muss mindestens 13 Ziffern enthalten.")

        bestehendes_buch = self.db.buch_laden(isbn)
        if bestehendes_buch:
            raise ValueError("Ein Buch mit dieser ISBN existiert bereits.")

        erfolg = self.db.buch_speichern(titel, autor, isbn, jahr)
        if not erfolg:
            raise ValueError("Buch konnte nicht gespeichert werden.")

        return True

    def alle_buecher_laden(self) -> list[dict]:
        """Lädt alle Bücher als Rohdaten aus der DB."""
        return self.db.alle_buecher_laden()

    def bucher_suchen(self, suchbegriff: str) -> list[dict]:
        """Sucht Bücher mit Rohdatenformat."""
        if not suchbegriff or not suchbegriff.strip():
            return self.alle_buecher_laden()
        return self.db.bucher_suchen(suchbegriff.strip())

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
        jahr: int = None,
        isbn_neu: str = None
    ) -> bool:
        """Aktualisiert einzelne Buchfelder; nicht angegebene Felder bleiben unveraendert."""
        bestehendes_buch = self.db.buch_laden(isbn)
        if not bestehendes_buch:
            raise ValueError("Buch nicht gefunden.")

        if isbn_neu is not None:
            isbn_neu = str(isbn_neu).strip()
            if not isbn_neu:
                isbn_neu = None
            elif isbn_neu != isbn:
                if sum(1 for z in isbn_neu if z.isdigit()) < 13:
                    raise ValueError("ISBN muss mindestens 13 Ziffern enthalten.")
                if self.db.buch_laden(isbn_neu):
                    raise ValueError("Ein Buch mit dieser neuen ISBN existiert bereits.")

        try:
            erfolg = self.db.buch_bearbeiten(
                isbn=isbn,
                titel=titel,
                autor=autor,
                jahr=jahr,
                isbn_neu=isbn_neu,
            )
        except TypeError:
            if isbn_neu and isbn_neu != isbn:
                raise ValueError("ISBN-Aenderung wird von dieser Datenbank-Version nicht unterstuetzt.")
            erfolg = self.db.buch_bearbeiten(
                isbn=isbn,
                titel=titel,
                autor=autor,
                jahr=jahr,
            )

        if not erfolg:
            raise ValueError("Buch konnte nicht bearbeitet werden.")

        return True

    def buch_loeschen(self, isbn: str, benutzer_rolle: str) -> bool:
        """Loescht ein Buch, sofern keine aktive Ausleihe dagegen spricht."""
        if benutzer_rolle not in ["Admin", "Administrator"]:
            raise ValueError("Nur Admins duerfen Buecher loeschen.")

        bestehendes_buch = self.db.buch_laden(isbn)
        if not bestehendes_buch:
            raise ValueError("Buch nicht gefunden.")

        erfolg = self.db.buch_loeschen(isbn)
        if not erfolg:
            raise ValueError("Buch kann nicht geloescht werden, solange mindestens ein Exemplar ausgeliehen ist.")

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

    def beliebte_buecher_karussell(self, limit: int = 5):
        """Gibt die Buchdaten fuer das Karussell zurueck."""
        if limit < 1:
            raise ValueError("Limit muss mindestens 1 sein.")
        if not hasattr(self.db, "beliebte_buecher_karussell"):
            raise NotImplementedError("Die DB unterstützt keine Karussell-Abfrage.")
        karussell = self.db.beliebte_buecher_karussell(limit)
        if karussell:
            return karussell
        # Frische Demo-DB: noch keine Buch-Titel mit 2+ aktiven Ausleihen
        return self.db.beliebteste_buecher_laden(limit)

    def exemplare_laden(self, isbn: str) -> list[dict]:
        """Lädt alle Exemplare eines Buches."""
        buch = self.db.buch_laden(isbn)
        if not buch:
            raise ValueError("Buch nicht gefunden.")
        return self.db.exemplare_laden(isbn)

    def exemplar_speichern(self, exemplar_id: str, isbn: str) -> bool:
        """Speichert ein einzelnes Exemplar zu einem Buch."""
        buch = self.db.buch_laden(isbn)
        if not buch:
            raise ValueError("Buch nicht gefunden.")
        erfolg = self.db.exemplar_speichern(exemplar_id, isbn)
        if not erfolg:
            raise ValueError("Exemplar konnte nicht gespeichert werden.")
        return True

    def exemplar_loeschen(self, exemplar_id: str) -> bool:
        """Löscht ein Exemplar, sofern es nicht ausgeliehen ist."""
        if not hasattr(self.db, "exemplar_loeschen"):
            raise NotImplementedError("Die DB unterstützt das Löschen von Exemplaren nicht.")
        erfolg = self.db.exemplar_loeschen(exemplar_id)
        if not erfolg:
            raise ValueError("Exemplar konnte nicht gelöscht werden.")
        return True

    def exemplar_ausleihe_laden(self, exemplar_id: str):
        """Lädt die aktive Ausleihe zu einem Exemplar, falls vorhanden."""
        if not hasattr(self.db, "exemplar_ausleihe_laden"):
            raise NotImplementedError("Die DB unterstützt diese Abfrage nicht.")
        return self.db.exemplar_ausleihe_laden(exemplar_id)

    def exemplar_status_aktualisieren(self, exemplar_id: str, status: str) -> bool:
        """Aktualisiert den Status eines Exemplars."""
        if status not in ["verfuegbar", "ausgeliehen"]:
            raise ValueError("Ungültiger Exemplar-Status.")
        if not hasattr(self.db, "exemplar_status_aktualisieren"):
            raise NotImplementedError("Die DB unterstützt keine Statusaktualisierung für Exemplare.")
        erfolg = self.db.exemplar_status_aktualisieren(exemplar_id, status)
        if not erfolg:
            raise ValueError("Exemplarstatus konnte nicht aktualisiert werden.")
        return True