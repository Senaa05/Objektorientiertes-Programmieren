"""
tab_ausleihen.py – Meine Ausleihen Tab
=======================================
"""
 
from nicegui import ui
from Frontend.state import service, aktueller_benutzer
 
 
def baue_ausleihen_tab(tab_refresh: dict):
    """
    Erstellt den Ausleihen-Tab-Inhalt.
    Registriert außerdem tab_refresh["ausleihen"] für externe Aktualisierungen.
    """
    ui.label("Meine Ausleihen").style(
        "font-size:1.4rem; font-weight:600; margin:1rem 0"
    )
    ausleihen_container = ui.column().classes("w-full gap-2")
 
    def ausleihen_laden():
        ausleihen_container.clear()
        try:
            ausleihen = service.meine_ausleihen(aktueller_benutzer())
        except Exception as e:
            ui.notify(f"❌ Fehler beim Laden der Ausleihen: {e}", color="negative")
            ausleihen = []
 
        if not ausleihen:
            with ausleihen_container:
                ui.label("Du hast aktuell keine aktiven Ausleihen.").style("color:#888")
            return
 
        for a in ausleihen:
            with ausleihen_container:
                with ui.card().classes("w-full").style("padding:1rem"):
                    with ui.row().classes("justify-between items-center w-full"):
                        with ui.column():
                            ui.label(a.get("titel", "Unbekanntes Buch")).style(
                                "font-weight:600"
                            )
                            ui.label(
                                f"Ausgeliehen: {a['ausleihdatum']}  ·  Fällig: {a['faelligkeit']}"
                            ).style("color:#666; font-size:0.85rem")
                            verlaengerungen = a.get("verlaengerungsanzahl", 0)
                            ui.label(f"Verlängerungen: {verlaengerungen}/1").style(
                                "font-size:0.8rem; color:#999"
                            )
                        with ui.row().classes("gap-2"):
                            aid = a["ausleih_id"]
                            if a.get("verlaengerungsanzahl", 0) < 1:
                                ui.button(
                                    "Verlängern",
                                    on_click=lambda _, i=aid: ausleih_verlaengern(i),
                                ).props("outline").style("color:#2563eb")
                            ui.button(
                                "Zurückgeben",
                                on_click=lambda _, i=aid: buch_zurueckgeben(i),
                            ).style("background:#dc2626; color:white")
 
    def ausleih_verlaengern(ausleih_id):
        try:
            service.ausleih_verlaengern(ausleih_id)
            ui.notify("✅ Ausleihe um 14 Tage verlängert.", color="positive")
            ausleihen_laden()
        except ValueError as e:
            ui.notify(f"❌ {e}", color="negative")
        except Exception as e:
            ui.notify(f"❌ Fehler: {e}", color="negative")
 
    def buch_zurueckgeben(ausleih_id):
        try:
            service.buch_zurueckgeben(ausleih_id)
            ui.notify("✅ Buch zurückgegeben.", color="positive")
            ausleihen_laden()
        except ValueError as e:
            ui.notify(f"❌ {e}", color="negative")
        except Exception as e:
            ui.notify(f"❌ Fehler: {e}", color="negative")
 
    tab_refresh["ausleihen"] = ausleihen_laden
    ausleihen_laden()