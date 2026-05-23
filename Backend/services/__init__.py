"""
Backend.services - zentrale Initialisierung der Services
Diese Datei initialisiert die Datenbank und erstellt die Service-Instanzen.
Die UI importiert Services von hier und greift nicht direkt auf `db` zu.
"""
import logging
import os
import sys
import traceback

projekt_pfad = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_pfad = os.path.join(projekt_pfad, "bibliothek_orm.db")
log_pfad = os.path.join(projekt_pfad, "logs")
log_datei = os.path.join(log_pfad, "bibflow.log")

# Ensure project root and Datenbank folder are importable for modules that use
# top-level imports like `from orm_models import ...`.
for pfad in [projekt_pfad, os.path.join(projekt_pfad, "Datenbank"), os.path.join(projekt_pfad, "Backend")]:
    if pfad not in sys.path:
        sys.path.insert(0, pfad)


def _erzeuge_logger() -> logging.Logger:
    os.makedirs(log_pfad, exist_ok=True)
    logger = logging.getLogger("bibflow.services")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_datei, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(handler)
        logger.propagate = False
    return logger


logger = _erzeuge_logger()

from Datenbank.orm_manager import ORMDatenbankManager
from .buch_service import BuchService
from .benutzer_service import BenutzerService
from .merkliste_service import MerklisteService
from .ausleihe_service import AusleiheService

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
        logger.error(
            "Initialisierung von Datenbank oder Services fehlgeschlagen:\n%s",
            traceback.format_exc(),
        )
        raise ServiceInitialisierungFehler(
            "Bibflow konnte nicht gestartet werden, weil die Datenbank- oder Service-"
            f"Initialisierung fehlgeschlagen ist: {exc}"
        ) from exc


# Datenbank und Services initialisieren
db, buch_service, benutzer_service, merkliste_service, _ausleihe_service = _initialisiere_services()

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
