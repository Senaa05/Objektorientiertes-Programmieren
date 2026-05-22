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
 
for pfad in [projekt_pfad]:
    if pfad not in sys.path:
        sys.path.insert(0, pfad)
 
# ─────────────────────────────────────────────
#  SERVICES INITIALISIEREN
# ─────────────────────────────────────────────
 
from Backend.services import buch_service, benutzer_service, merkliste_service, service
 
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