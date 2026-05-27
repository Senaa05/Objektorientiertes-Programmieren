"""
Backend.services - zentrale Initialisierung der Services
Diese Datei initialisiert die Datenbank und erstellt die Service-Instanzen.
Die UI importiert Services von hier und greift nicht direkt auf `db` zu.
"""
import os

from log_util import get_logger

projekt_pfad = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_pfad = os.path.join(projekt_pfad, "bibliothek_orm.db")

logger = get_logger("services")

from Datenbank.orm_manager import ORMDatenbankManager
from Backend.bootstrap import (
    ensure_demo_ausleihen,
    ensure_demo_bibliotheksbestand,
    ensure_lokale_zugaenge,
)
from Backend.services.buch_service import BuchService
from Backend.services.benutzer_service import BenutzerService
from Backend.services.merkliste_service import MerklisteService
from Backend.services.ausleihe_service import AusleiheService

class ServiceInitialisierungFehler(RuntimeError):
    """Wird ausgelöst, wenn die Datenbank- oder Service-Initialisierung scheitert."""


def _initialisiere_services():
    try:
        db = ORMDatenbankManager(db_pfad)
        buch_service = BuchService(db)
        benutzer_service = BenutzerService(db)
        merkliste_service = MerklisteService(db)
        ausleihe_service = AusleiheService(db)
        return db, buch_service, benutzer_service, merkliste_service, ausleihe_service
    except Exception as exc:
        logger.exception("Initialisierung von Datenbank oder Services fehlgeschlagen")
        raise ServiceInitialisierungFehler(
            "Bibflow konnte nicht gestartet werden, weil die Datenbank- oder Service-"
            f"Initialisierung fehlgeschlagen ist: {exc}"
        ) from exc


# Datenbank und Services initialisieren
db, buch_service, benutzer_service, merkliste_service, _ausleihe_service = _initialisiere_services()
ensure_lokale_zugaenge(benutzer_service, logger)
ensure_demo_bibliotheksbestand(db, buch_service)
ensure_demo_ausleihen(db)

class Service:
    def buch_ausleihen(self, b, i):
        return _ausleihe_service.buch_ausleihen(b, i)

    def meine_ausleihen(self, b):
        return _ausleihe_service.meine_ausleihen(b)

    def ausleih_verlaengern(self, i):
        return _ausleihe_service.ausleihe_verlaengern(i)

    def buch_zurueckgeben(self, i):
        return _ausleihe_service.buch_zurueckgeben(i)

    def ueberfaellige_ausleihen(self):
        return _ausleihe_service.ueberfaellige_ausleihen()

    def popup_ueberfaellige_fuer_benutzer(self, b):
        return _ausleihe_service.popup_ueberfaellige_fuer_benutzer(b)

    def reminder_fuer_benutzer(self, b, tage=7):
        return [
            eintrag
            for eintrag in _ausleihe_service.reminder_kandidaten_holen(tage)
            if eintrag.get("benutzername") == b
        ]

service = Service()

__all__ = [
    "ServiceInitialisierungFehler",
    "buch_service",
    "benutzer_service",
    "merkliste_service",
    "service",
]
