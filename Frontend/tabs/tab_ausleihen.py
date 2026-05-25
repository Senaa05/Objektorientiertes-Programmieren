"""
tab_ausleihen.py – Meine Ausleihen Tab
=======================================
"""

from nicegui import ui
from Frontend.buch_cover import zeige_buch_cover
from Frontend.state import service, aktueller_benutzer


def baue_ausleihen_tab(tab_refresh: dict):
    """
    Erstellt den Ausleihen-Tab-Inhalt.
    Registriert außerdem tab_refresh["ausleihen"] für externe Aktualisierungen.
    """
    ui.label("Meine Ausleihen").classes("text-2xl font-semibold my-4")
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
                ui.label("Du hast aktuell keine aktiven Ausleihen.").classes("text-gray-400")
            return

        for a in ausleihen:
            with ausleihen_container:
                with ui.card().classes("w-full p-4"):
                    with ui.row().classes("items-stretch w-full gap-4 no-wrap"):
                        isbn = a.get("isbn", "")
                        titel = a.get("titel", "Unbekanntes Buch")
                        if isbn:
                            zeige_buch_cover(isbn, titel, a.get("autor", ""))
                        with ui.column().classes("flex-1 min-w-0 justify-center gap-1"):
                            ui.label(titel).classes("font-semibold")
                            ui.label(
                                f"Ausgeliehen: {a['ausleihdatum']}  ·  Fällig: {a['faelligkeit']}"
                            ).classes("text-gray-500 text-sm")
                            verlaengerungen = a.get("verlaengerungsanzahl", 0)
                            ui.label(f"Verlängerungen: {verlaengerungen}/1").classes("text-xs text-gray-400")
                        with ui.row().classes("gap-2"):
                            aid = a["ausleih_id"]
                            if a.get("verlaengerungsanzahl", 0) < 1:
                                ui.button(
                                    "Verlängern",
                                    on_click=lambda _, i=aid: ausleih_verlaengern(i),
                                ).props("outline").classes("text-blue-600")
                            ui.button(
                                "Zurückgeben",
                                on_click=lambda _, i=aid: buch_zurueckgeben(i),
                            ).classes("bg-red-600 text-white")

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