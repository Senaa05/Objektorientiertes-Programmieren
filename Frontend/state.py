"""
state.py - Gemeinsamer Zustand, Services und Hilfsfunktionen
============================================================
Diese Datei ist der einzige Ort, an dem Services initialisiert werden.
Alle anderen Module importieren von hier - nie umgekehrt.
"""
 
import os
import sys
 
# ─────────────────────────────────────────────
#  PFADE KONFIGURIEREN
# ─────────────────────────────────────────────
 
basis_pfad   = os.path.dirname(os.path.abspath(__file__))
projekt_pfad = os.path.dirname(basis_pfad)
 
for pfad in [
    projekt_pfad,
    os.path.join(projekt_pfad, "Backend"),
    os.path.join(projekt_pfad, "Datenbank"),
]:
    if pfad not in sys.path:
        sys.path.insert(0, pfad)
 
# ─────────────────────────────────────────────
#  SERVICES INITIALISIEREN
# ─────────────────────────────────────────────
 
db_pfad = os.path.join(projekt_pfad, "bibliothek_orm.db")
 
from Datenbank.orm_manager import ORMDatenbankManager
from Backend.services.buch_service import BuchService
from Backend.services.benutzer_service import BenutzerService
from Backend.services.merkliste_service import MerklisteService
 
db               = ORMDatenbankManager(db_pfad)
buch_service     = BuchService(db)
benutzer_service = BenutzerService(db)
merkliste_service = MerklisteService(db)
 
try:
    from Backend.services.ausleihe_service import AusleiheService
    _service = AusleiheService(db)
 
    class Service:
        def buch_ausleihen(self, b, i):
            return _service.buch_ausleihen(b, i)
 
        def meine_ausleihen(self, b):
            return _service.meine_ausleihen(b)
 
        def ausleih_verlaengern(self, i):
            return _service.ausleihe_verlaengern(i)
 
        def buch_zurueckgeben(self, i):
            return _service.buch_zurueckgeben(i)
 
        def ueberfaellige_ausleihen(self):
            return _service.ueberfaellige_ausleihen()

        def popup_ueberfaellige_fuer_benutzer(self, b):
            return _service.popup_ueberfaellige_fuer_benutzer(b)

        def reminder_fuer_benutzer(self, b, tage=7):
            return [
                eintrag
                for eintrag in _service.reminder_kandidaten_holen(tage)
                if eintrag["benutzername"] == b
            ]
 
    service = Service()
    print("AusleiheService erfolgreich geladen.")
 
except Exception as e:
    print(f"Service-Fehler: {e} - DummyService wird verwendet.")
 
    class Service:
        def buch_ausleihen(self, b, i):    raise ValueError("Service nicht geladen")
        def meine_ausleihen(self, b):      return db.ausleihen_benutzer(b)
        def ausleih_verlaengern(self, i):  raise ValueError("Service nicht geladen")
        def buch_zurueckgeben(self, i):    raise ValueError("Service nicht geladen")
        def ueberfaellige_ausleihen(self): return db.ueberfaellige_ausleihen()
        def popup_ueberfaellige_fuer_benutzer(self, b):
            return [
                eintrag
                for eintrag in db.ueberfaellige_ausleihen()
                if eintrag["benutzername"] == b
            ]

        def reminder_fuer_benutzer(self, b, tage=7):
            if not hasattr(db, "bald_faellige_ausleihen"):
                return []
            return [
                eintrag
                for eintrag in db.bald_faellige_ausleihen(tage)
                if eintrag["benutzername"] == b
            ]
 
    service = Service()
 
# ─────────────────────────────────────────────
#  ZUSTAND (einfacher Login-State)
# ─────────────────────────────────────────────
 
zustand: dict = {
    "angemeldet":  False,
    "benutzername": "",
    "rolle":        "",
}
 
# ─────────────────────────────────────────────
#  HILFSFUNKTIONEN
# ─────────────────────────────────────────────
 
def ist_admin() -> bool:
    return zustand["rolle"] in ["Admin", "Administrator"]
 
def aktueller_benutzer() -> str:
    return zustand["benutzername"]