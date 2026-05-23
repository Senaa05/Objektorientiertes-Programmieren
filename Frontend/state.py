"""
state.py - Gemeinsamer Zustand, Services und Hilfsfunktionen
============================================================
Diese Datei ist der einzige Ort, an dem Services initialisiert werden.
Alle anderen Module importieren von hier - nie umgekehrt.
"""

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