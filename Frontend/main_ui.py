"""
main_ui.py - NiceGUI-Routen und App-Start
=========================================
Wird von main.py im Projektroot gestartet (siehe Pizza-App-Muster).
"""
import os

from nicegui import ui
from Frontend.login import zeige_login
from Frontend.dashboard import zeige_dashboard


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
    reload_aktiv = os.getenv("NICEGUI_RELOAD", "0") == "1"
    ui.run(
        title="Bibliothek",
        port=8080,
        reload=reload_aktiv,
        dark=False,
        show=True,
    )
 