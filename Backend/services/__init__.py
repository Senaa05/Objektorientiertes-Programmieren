"""
Backend.services - zentrale Initialisierung der Services
Diese Datei initialisiert die Datenbank und erstellt die Service-Instanzen.
Die UI importiert Services von hier und greift nicht direkt auf `db` zu.
"""
import logging
import os

projekt_pfad = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_pfad = os.path.join(projekt_pfad, "bibliothek_orm.db")
log_pfad = os.path.join(projekt_pfad, "logs")
log_datei = os.path.join(log_pfad, "bibflow.log")


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
from Datenbank.seed_demo_daten import seed_demo_buecher
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


# Dokumentierter lokaler Admin (README Abschnitt „Lokaler Admin-Zugang“)
LOKALER_ADMIN = {
    "benutzername": "admin1",
    "passwort": "admin123",
    "vorname": "Lokal",
    "nachname": "Admin",
    "email": "admin1@bibflow.local",
    "rolle": "Admin",
}

# Optionaler Demo-Benutzer zum Testen der Benutzer-Ansicht
LOKALER_DEMO_BENUTZER = {
    "benutzername": "demo",
    "passwort": "demo123",
    "vorname": "Demo",
    "nachname": "Benutzer",
    "email": "demo@bibflow.local",
    "rolle": "Benutzer",
}


def _konto_anlegen_wenn_fehlt(benutzer_service: BenutzerService, konto: dict) -> None:
    if benutzer_service.db.benutzer_laden(konto["benutzername"]):
        return
    try:
        benutzer_service.benutzer_registrieren(**konto)
        logger.info("Lokales Konto '%s' wurde angelegt.", konto["benutzername"])
    except ValueError as exc:
        logger.warning(
            "Lokales Konto '%s' konnte nicht angelegt werden: %s",
            konto["benutzername"],
            exc,
        )


def _ensure_lokaler_admin(benutzer_service: BenutzerService) -> None:
    """Stellt den dokumentierten Admin admin1 immer bereit (anlegen oder README-Passwort sicherstellen)."""
    from Backend.services.benutzer_service import _passwort_hashen

    bn = LOKALER_ADMIN["benutzername"]
    pw = LOKALER_ADMIN["passwort"]

    try:
        benutzer_service.login(bn, pw)
        return
    except ValueError:
        pass

    if benutzer_service.db.benutzer_laden(bn):
        benutzer_service.db.benutzer_passwort_aktualisieren(bn, _passwort_hashen(pw))
        logger.info("Lokaler Admin '%s': Passwort auf README-Wert gesetzt.", bn)
        return

    try:
        benutzer_service.benutzer_registrieren(**LOKALER_ADMIN)
        logger.info("Lokaler Admin '%s' wurde angelegt.", bn)
    except ValueError as exc:
        logger.warning("Lokaler Admin '%s' konnte nicht angelegt werden: %s", bn, exc)


def _ensure_lokale_zugaenge(benutzer_service: BenutzerService) -> None:
    """Lokaler Admin ist immer vorhanden; Demo-Benutzer nur bei Bedarf."""
    _ensure_lokaler_admin(benutzer_service)
    _konto_anlegen_wenn_fehlt(benutzer_service, LOKALER_DEMO_BENUTZER)


def _ensure_demo_bibliotheksbestand(buch_service: BuchService) -> None:
    """Legt den Demo-Buchkatalog an, wenn die DB noch keine Bücher enthält."""
    angelegt = seed_demo_buecher(buch_service)
    if angelegt:
        logger.info("Demo-Bibliotheksbestand angelegt: %s Bücher.", angelegt)


# Datenbank und Services initialisieren
db, buch_service, benutzer_service, merkliste_service, _ausleihe_service = _initialisiere_services()
_ensure_lokale_zugaenge(benutzer_service)
_ensure_demo_bibliotheksbestand(buch_service)

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
