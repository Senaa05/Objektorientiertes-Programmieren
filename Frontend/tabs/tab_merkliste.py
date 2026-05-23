"""
tab_merkliste.py – Meine Merkliste Tab
=======================================
"""

from nicegui import ui
from Frontend.state import buch_service, service, merkliste_service, aktueller_benutzer


def baue_merkliste_tab(tab_refresh: dict):
    """
    Erstellt den Merkliste-Tab-Inhalt.
    Registriert außerdem tab_refresh["merkliste"] für externe Aktualisierungen.
    """
    ui.label("Meine Merkliste").style(
        "font-size:1.4rem; font-weight:600; margin:1rem 0"
    )
    merkliste_container = ui.column().classes("w-full gap-2")

    def merkliste_laden_seite():
        merkliste_container.clear()
        eintraege = merkliste_service.merkliste_laden(aktueller_benutzer())

        if not eintraege:
            with merkliste_container:
                ui.label("Deine Merkliste ist leer.").style("color:#888")
            return

        for eintrag in eintraege:
            verfuegbar = len(buch_service.verfuegbare_exemplare(eintrag["isbn"])) > 0
            with merkliste_container:
                with ui.card().classes("w-full").style("padding:1rem"):
                    with ui.row().classes("justify-between items-center w-full"):
                        with ui.column():
                            ui.label(eintrag["titel"]).style(
                                "font-weight:600; font-size:1rem"
                            )
                            ui.label(
                                f"{eintrag['autor']} · ISBN: {eintrag['isbn']}"
                            ).style("color:#666; font-size:0.85rem")
                            anzahl = len(buch_service.verfuegbare_exemplare(eintrag["isbn"]))
                            if anzahl > 0:
                                ui.label(f"📗 Exemplare übrig: {anzahl}").style(
                                    "color:#16a34a"
                                )
                            else:
                                ui.label("❌ Nicht verfügbar").style("color:#dc2626")

                        with ui.row().classes("gap-2"):
                            isbn_kopie = eintrag["isbn"]
                            if verfuegbar:
                                ui.button(
                                    "Ausleihen",
                                    on_click=lambda _, i=isbn_kopie: buch_ausleihen(i),
                                ).style("background:#2563eb; color:white")
                            ui.button(
                                "⭐ Entfernen",
                                on_click=lambda _, i=isbn_kopie: eintrag_entfernen(i),
                            ).props("outline").style("color:#dc2626")

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
