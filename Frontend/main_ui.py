"""
main_ui.py - Einstiegspunkt für Bibflow
========================================
Nur drei Aufgaben:
  1. Alle Seiten-Module importieren
  2. Routen registrieren (@ui.page)
  3. ui.run() starten
"""
 
from nicegui import ui
from login import zeige_login
from dashboard import zeige_dashboard
 
 
# ─────────────────────────────────────────────
#  ROUTEN
# ─────────────────────────────────────────────
 
@ui.page("/")
def login_seite():
    zeige_login()
 
 
@ui.page("/dashboard")
def dashboard_seite():
    zeige_dashboard()
 
 
# ─────────────────────────────────────────────
#  START
# ─────────────────────────────────────────────
 
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Bibliothek",
        port=8080,
        reload=True,
        dark=False,
        show=True,
    )
 