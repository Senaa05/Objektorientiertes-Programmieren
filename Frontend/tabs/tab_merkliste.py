"""
tab_merkliste.py – Meine Merkliste Tab
=======================================
"""

from nicegui import ui
from Frontend.buch_cover import zeige_buch_cover
from Frontend.state import buch_service, service, merkliste_service, aktueller_benutzer


def baue_merkliste_tab(tab_refresh: dict):
    """
    Erstellt den Merkliste-Tab-Inhalt.
    Registriert außerdem tab_refresh["merkliste"] für externe Aktualisierungen.
    """
    ui.label("Meine Merkliste").classes("text-2xl font-semibold my-4")
    merkliste_container = ui.column().classes("w-full gap-2")

    def merkliste_laden_seite():
        merkliste_container.clear()
        eintraege = merkliste_service.merkliste_laden(aktueller_benutzer())

        if not eintraege:
            with merkliste_container:
                ui.label("Deine Merkliste ist leer.").classes("text-gray-400")
            return

        for eintrag in eintraege:
            verfuegbar = len(buch_service.verfuegbare_exemplare(eintrag["isbn"])) > 0
            with merkliste_container:
                with ui.card().classes("w-full p-4"):
                    with ui.row().classes("items-stretch w-full gap-4 no-wrap"):
                        zeige_buch_cover(
                            eintrag["isbn"], eintrag["titel"], eintrag["autor"]
                        )
                        with ui.column().classes("flex-1 min-w-0 justify-center gap-1"):
                            ui.label(eintrag["titel"]).classes("font-semibold text-base")
                            ui.label(
                                f"{eintrag['autor']} · ISBN: {eintrag['isbn']}"
                            ).classes("text-gray-500 text-sm")
                            anzahl = len(buch_service.verfuegbare_exemplare(eintrag["isbn"]))
                            if anzahl > 0:
                                ui.label(f"📗 Exemplare übrig: {anzahl}").classes("text-green-600")
                            else:
                                ui.label("❌ Nicht verfügbar").classes("text-red-600")

                        with ui.row().classes("gap-2"):
                            isbn_kopie = eintrag["isbn"]
                            if verfuegbar:
                                ui.button(
                                    "Ausleihen",
                                    on_click=lambda _, i=isbn_kopie: buch_ausleihen(i),
                                ).classes("bg-blue-600 text-white")
                            ui.button(
                                "⭐ Entfernen",
                                on_click=lambda _, i=isbn_kopie: eintrag_entfernen(i),
                            ).props("outline").classes("text-red-600")

    def buch_ausleihen(isbn):
        try:
            service.buch_ausleihen(aktueller_benutzer(), isbn)
            ui.notify("✅ Erfolgreich ausgeliehen!", color="positive")
            merkliste_laden_seite()
            if tab_refresh.get("ausleihen"):
                tab_refresh["ausleihen"]()
        except ValueError as e:
            ui.notify(f"❌ {e}", color="negative")
        except Exception as e:
            ui.notify(f"❌ Fehler: {e}", color="negative")

    def eintrag_entfernen(isbn):
        merkliste_service.merkliste_entfernen(aktueller_benutzer(), isbn)
        ui.notify("☆ Von Merkliste entfernt.", color="info")
        merkliste_laden_seite()

    tab_refresh["merkliste"] = merkliste_laden_seite
    merkliste_laden_seite()