"""
main_ui.py - NiceGUI-Routen und App-Start
=========================================
Wird von main.py im Projektroot gestartet.
"""
import os

from nicegui import ui
from Frontend.login import zeige_login
from Frontend.dashboard import zeige_dashboard
from Frontend.buch_cover import registriere_cover_route


# ─────────────────────────────────────────────
#  ROUTEN
# ─────────────────────────────────────────────

@ui.page("/")
def login_seite():
    zeige_login()


@ui.page("/dashboard")
def dashboard_seite():
    zeige_dashboard()


def start() -> None:
    """Startet die Bibflow-Web-Oberfläche."""
    registriere_cover_route()
    reload_aktiv = os.getenv("NICEGUI_RELOAD", "0") == "1"
    ui.run(
        title="Bibliothek",
        port=8080,
        reload=reload_aktiv,
        dark=False,
        show=True,
    )
 