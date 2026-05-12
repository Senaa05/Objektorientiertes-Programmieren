from datetime import date, timedelta
import uuid

from modelle.ausleihe import Ausleihe

class AusleiheService:
    """Service fuer alle Geschäftsregeln rund um Ausleihe, Verlängerung und Rueckgabe."""

    def __init__(self, db):
        self.db = db

    def buch_ausleihen(self, benutzername: str, isbn: str) -> str:
        """Leiht ein verfuegbares Exemplar fuer 30 Tage aus und liefert die Ausleih-ID zurueck."""
        # Voraussetzungen fuer eine gueltige Ausleihe pruefen.
        benutzer = self.db.benutzer_laden(benutzername)
        if not benutzer:
            raise ValueError("Benutzer existiert nicht.")

        buch = self.db.buch_laden(isbn)
        if not buch:
            raise ValueError("Buch existiert nicht.")

        aktive_anzahl = self.db.anzahl_ausleihen_benutzer(benutzername)
        if aktive_anzahl >= 5:
            raise ValueError("Benutzer darf maximal 5 Bücher gleichzeitig ausleihen.")

        verfuegbare_exemplare = self.db.verfuegbare_exemplare(isbn)
        if not verfuegbare_exemplare:
            raise ValueError("Kein verfügbares Exemplar vorhanden.")

        exemplar_id = verfuegbare_exemplare[0]["exemplar_id"]

        # Standardfrist gemaess Anforderung: 30 Tage.
        ausleih_id = str(uuid.uuid4())
        ausleihdatum = date.today()
        faelligkeit = ausleihdatum + timedelta(days=30)

        erfolg = self.db.ausleih_speichern(
            ausleih_id=ausleih_id,
            benutzername=benutzername,
            exemplar_id=exemplar_id,
            ausleihdatum=ausleihdatum.strftime("%Y-%m-%d"),
            faelligkeit=faelligkeit.strftime("%Y-%m-%d")
        )

        if not erfolg:
            raise ValueError("Ausleihe konnte nicht gespeichert werden.")

        status_aktualisiert = self.db.exemplar_status_aktualisieren(exemplar_id, "ausgeliehen")
        if not status_aktualisiert:
            raise ValueError("Exemplarstatus konnte nicht aktualisiert werden.")

        return ausleih_id

    def ausleihe_verlaengern(self, ausleih_id: str) -> bool:
        """Verlaengert eine aktive Ausleihe einmalig um 14 Tage."""
        # Verlaengerung ist nur einmal erlaubt und erhoeht um 14 Tage.
        ausleihe = self.db.ausleih_laden(ausleih_id)
        if not ausleihe:
            raise ValueError("Ausleihe nicht gefunden.")

        ausleihe_obj = Ausleihe(**ausleihe)

        if not ausleihe_obj.ist_verlaengerbar():
            raise ValueError("Ausleihe kann nicht verlängert werden.")

        aktuelle_faelligkeit = date.fromisoformat(ausleihe_obj.faelligkeit)
        neue_faelligkeit = aktuelle_faelligkeit + timedelta(days=14)

        erfolg = self.db.ausleih_verlaengern(
            ausleih_id=ausleih_id,
            neue_faelligkeit=neue_faelligkeit.strftime("%Y-%m-%d")
        )

        if not erfolg:
            raise ValueError("Verlängerung fehlgeschlagen.")

        return True

    def buch_zurueckgeben(self, ausleih_id: str) -> bool:
        """Markiert eine Ausleihe als zurueckgegeben und setzt das Exemplar auf verfuegbar."""
        # Rueckgabe markiert Ausleihe und gibt Exemplar wieder frei.
        ausleihe = self.db.ausleih_laden(ausleih_id)
        if not ausleihe:
            raise ValueError("Ausleihe nicht gefunden.")

        ausleihe_obj = Ausleihe(**ausleihe)

        if ausleihe_obj.ist_zurueckgegeben():
            raise ValueError("Buch wurde bereits zurückgegeben.")

        erfolg = self.db.ausleih_rueckgabe(ausleih_id)
        if not erfolg:
            raise ValueError("Rückgabe fehlgeschlagen.")

        status_aktualisiert = self.db.exemplar_status_aktualisieren(
            ausleihe_obj.exemplar_id,
            "verfuegbar"
        )
        if not status_aktualisiert:
            raise ValueError("Exemplarstatus konnte nicht auf 'verfuegbar' gesetzt werden.")

        return True

    def meine_ausleihen(self, benutzername: str):
        """Liefert alle aktiven Ausleihen eines Benutzers, sortiert von alt nach neu."""
        # Anzeige-Reihenfolge: aelteste Ausleihe zuerst.
        ausleihen = self.db.ausleihen_benutzer(benutzername)
        return sorted(ausleihen, key=lambda eintrag: eintrag["ausleihdatum"])

    def ueberfaellige_ausleihen(self):
        """Gibt alle aktuell ueberfaelligen Ausleihen zurueck."""
        return self.db.ueberfaellige_ausleihen()

    def bald_faellige_ausleihen(self, tage: int = 7):
        """Liefert aktive Ausleihen, deren Faelligkeit innerhalb der naechsten Tage liegt."""
        return self.db.bald_faellige_ausleihen(tage)

    def hat_ueberfaellige_buecher(self, benutzername: str) -> bool:
        """Prueft, ob ein Benutzer mindestens eine ueberfaellige Ausleihe hat."""
        return self.db.benutzer_hat_ueberfaellige_buecher(benutzername)

    def reminder_kandidaten_holen(self, tage: int = 7):
        """Hilfsmethode fuer die UI: Datenbasis fuer Reminder-Liste holen."""
        # Liefert die Datenbasis fuer UI-Reminder.
        return self.bald_faellige_ausleihen(tage)

    def popup_ueberfaellige_fuer_benutzer(self, benutzername: str):
        """Filtert ueberfaellige Ausleihen fuer genau den angemeldeten Benutzer."""
        # Liefert nur ueberfaellige Eintraege des aktiven Benutzers.
        return [
            eintrag
            for eintrag in self.ueberfaellige_ausleihen()
            if eintrag["benutzername"] == benutzername
        ]