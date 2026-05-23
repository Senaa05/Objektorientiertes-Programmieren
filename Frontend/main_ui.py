"""
main_ui.py - Einstiegspunkt für Bibflow
========================================
Nur drei Aufgaben:
  1. Alle Seiten-Module importieren
  2. Routen registrieren (@ui.page)
  3. ui.run() starten
"""
 
import os
from nicegui import ui


STARTFEHLER = None

try:
    from login import zeige_login
    from dashboard import zeige_dashboard
except Exception as exc:
    STARTFEHLER = exc


def zeige_startfehler():
    with ui.card().classes("absolute-center").style("width:520px; padding:2rem"):
        ui.label("Bibflow konnte nicht gestartet werden").style(
            "font-size:1.4rem; font-weight:700; margin-bottom:0.75rem; text-align:center"
        )
        ui.label(
            "Beim Laden der Services oder der Datenbank ist ein Fehler aufgetreten. "
            "Bitte prüfe die Datenbankdatei oder starte die Anwendung später erneut."
        ).style("color:#555; text-align:center; margin-bottom:1rem")
        ui.label(f"Fehlerdetails: {STARTFEHLER}").style(
            "color:#b91c1c; font-size:0.9rem; white-space:pre-wrap"
        )
 
 
# ─────────────────────────────────────────────
#  ROUTEN
# ─────────────────────────────────────────────
 
@ui.page("/")
def login_seite():
    if STARTFEHLER is not None:
        zeige_startfehler()
    else:
        zeige_login()
 
 
@ui.page("/dashboard")
def dashboard_seite():
    if STARTFEHLER is not None:
        zeige_startfehler()
    else:
        zeige_dashboard()
 
 
# ─────────────────────────────────────────────
#  START
# ─────────────────────────────────────────────
 
if __name__ in {"__main__", "__mp_main__"}:
    reload_aktiv = os.getenv("NICEGUI_RELOAD", "0") == "1"
    ui.run(
        title="Bibliothek",
        port=8080,
        reload=reload_aktiv,
        dark=False,
        show=True,
    )
 