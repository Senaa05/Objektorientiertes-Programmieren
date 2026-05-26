"""
tab_buecher.py – Bücher-Tab inkl. Karussell
============================================
"""

from nicegui import ui
from Frontend.buch_cover import zeige_buch_cover
from Frontend.state import buch_service, service, merkliste_service, ist_admin, aktueller_benutzer


def baue_buecher_tab(tab_refresh: dict):
    ui.label("Bücher suchen & ausleihen").classes("text-2xl font-semibold my-4")

    with ui.row().classes("items-center gap-2 mb-4"):
        such_input = ui.input(placeholder="Titel, Autor oder ISBN...").classes("w-72")
        ui.button("Suchen", on_click=lambda: buecher_laden(such_input.value)).classes(
            "bg-blue-600 text-white"
        )
        ui.button(
            "Zurücksetzen",
            on_click=lambda: (such_input.set_value(""), sortierung.update({"feld": None, "richtung": "asc"}), buecher_laden("")),
        ).props("outline")

    # ── Beliebteste Bücher Karussell ──
    ui.label("Unsere beliebtesten Ausleihen").classes("text-lg font-semibold mt-2 mb-1")
    beliebt = buch_service.beliebte_buecher_karussell()

    if beliebt:
        with ui.row().classes("w-full items-center gap-2 no-wrap"):
            ui.button(
                "←",
                on_click=lambda: karussell.run_method(
                    "scrollBy", {"left": -200, "behavior": "smooth"}
                ),
            ).props("flat dense").classes("text-xl min-w-8 shrink-0")

            with ui.row().classes(
                "flex-1 min-w-0 gap-4 overflow-x-auto overflow-y-hidden "
                "scroll-smooth pb-1 no-wrap"
            ) as karussell:
                for buch in beliebt:
                    with ui.card().classes(
                        "!w-40 !min-w-40 !max-w-40 p-0 overflow-hidden "
                        "shrink-0 grow-0 flex flex-col"
                    ):
                        zeige_buch_cover(
                            buch["isbn"],
                            buch["titel"],
                            buch["autor"],
                            karussell=True,
                        )
                        with ui.element("div").classes("p-2 flex flex-col gap-1 w-full box-border flex-1"):
                            ui.label(buch["titel"]).classes(
                                "font-bold text-[0.8rem] leading-[1.2] "
                                "min-h-[calc(0.8rem*1.2*2)] line-clamp-2"
                            )
                            ui.label(buch["autor"]).classes("text-xs text-gray-500")
                            ui.label(f"📖 {buch.get('anzahl_ausleihen', 0)}× ausgeliehen").classes("text-xs text-gray-400")
                            isbn_kopie = buch["isbn"]
                            verfuegbar = len(buch_service.verfuegbare_exemplare(isbn_kopie)) > 0
                            if verfuegbar and not ist_admin():
                                ui.button(
                                    "Ausleihen",
                                    on_click=lambda _, i=isbn_kopie: buch_ausleihen(i),
                                ).classes("w-full bg-blue-600 text-white mt-auto")
                            elif not verfuegbar:
                                ui.label("Nicht verfügbar").classes("text-red-600 text-xs mt-auto")

            ui.button(
                "→",
                on_click=lambda: karussell.run_method(
                    "scrollBy", {"left": 200, "behavior": "smooth"}
                ),
            ).props("flat dense").classes("text-xl min-w-8 shrink-0")
    else:
        ui.label(
            "Noch keine Ausleih-Statistik — lege Bücher aus, um Beliebtheit zu sehen."
        ).classes("text-sm text-gray-400 mb-2")

    ui.separator().classes("mb-4")

    # ── Filter-State ──
    sortierung = {"feld": None, "richtung": "asc"}

    # ── Sortierung setzen ──
    def sortierung_setzen(feld, richtung):
        sortierung["feld"] = feld
        sortierung["richtung"] = richtung
        buecher_laden(such_input.value)

    # ── Filter-Leiste ──
    with ui.row().classes("items-center gap-2 w-full flex-wrap mb-2"):
        ui.label("Sortieren:").classes("font-semibold text-sm")
        ui.button("Titel A-Z",  on_click=lambda: sortierung_setzen("titel", "asc")).props("outline").classes("text-xs")
        ui.button("Titel Z-A",  on_click=lambda: sortierung_setzen("titel", "desc")).props("outline").classes("text-xs")
        ui.button("Jahr ↑",     on_click=lambda: sortierung_setzen("jahr", "asc")).props("outline").classes("text-xs")
        ui.button("Jahr ↓",     on_click=lambda: sortierung_setzen("jahr", "desc")).props("outline").classes("text-xs")
        ui.button(
            "Zurücksetzen",
            on_click=lambda: (sortierung.update({"feld": None, "richtung": "asc"}), buecher_laden("")),
        ).props("outline").classes("text-xs")

    buecher_container = ui.element("div").classes("grid grid-cols-4 gap-4 w-full")

    # ── Bücher laden ──
    def buecher_laden(suchbegriff=""):
        buecher_container.clear()
        ergebnisse = (
            buch_service.bucher_suchen(suchbegriff) if suchbegriff else buch_service.alle_buecher_laden()
        )

        # Sortierung anwenden
        if sortierung["feld"] == "titel":
            ergebnisse = sorted(ergebnisse, key=lambda b: b["titel"].lower(), reverse=(sortierung["richtung"] == "desc"))
        elif sortierung["feld"] == "jahr":
            ergebnisse = sorted(ergebnisse, key=lambda b: b["jahr"], reverse=(sortierung["richtung"] == "desc"))

        if not ergebnisse:
            with buecher_container:
                hinweis = (
                    "Keine Treffer gefunden."
                    if suchbegriff and suchbegriff.strip()
                    else "Keine Bücher gefunden."
                )
                ui.label(hinweis).classes("text-gray-400")
            return

        for buch in ergebnisse:
            verfuegbar = len(buch_service.verfuegbare_exemplare(buch["isbn"])) > 0
            with buecher_container:
                with ui.card().classes("w-full flex flex-col p-3 gap-2"):
                    with ui.element("div").classes("flex justify-center w-full"):
                        zeige_buch_cover(buch["isbn"], buch["titel"], buch["autor"])
                    with ui.column().classes("w-full gap-1 items-start"):
                        ui.label(buch["titel"]).classes("font-semibold text-sm leading-snug")
                        ui.label(f"{buch['autor']} · {buch['jahr']}").classes("text-gray-500 text-xs")
                        ui.label(f"ISBN: {buch['isbn']}").classes("text-gray-400 text-xs")

                        anzahl_verfuegbar = len(buch_service.verfuegbare_exemplare(buch["isbn"]))
                        if anzahl_verfuegbar > 0:
                            ui.label(f"📗 Exemplare übrig: {anzahl_verfuegbar}").classes("text-green-600 text-xs")
                        else:
                            ui.label("❌ Nicht verfügbar").classes("text-red-600 text-xs")

                    with ui.row().classes("w-full gap-1 items-center justify-end"):
                        isbn_kopie = buch["isbn"]
                        if not ist_admin():
                            merkliste = merkliste_service.merkliste_laden(aktueller_benutzer())
                            ist_gemerkt = any(m["isbn"] == isbn_kopie for m in merkliste)
                            stern = "⭐" if ist_gemerkt else "☆"
                            ui.button(
                                stern,
                                on_click=lambda _, i=isbn_kopie: merkliste_toggle(i),
                            ).props("flat").classes("text-xl")
                        if not ist_admin() and verfuegbar:
                            ui.button(
                                "Ausleihen",
                                on_click=lambda _, i=isbn_kopie: buch_ausleihen(i),
                            ).classes("bg-blue-600 text-white text-xs")

    # ── Buch ausleihen ──
    def buch_ausleihen(isbn):
        try:
            service.buch_ausleihen(aktueller_benutzer(), isbn)
            ui.notify("✅ Erfolgreich ausgeliehen!", color="positive")
            buecher_laden("")
            if tab_refresh.get("ausleihen"):
                tab_refresh["ausleihen"]()
            if tab_refresh.get("merkliste"):
                tab_refresh["merkliste"]()
        except ValueError as e:
            ui.notify(f"❌ {e}", color="negative")
        except Exception as e:
            ui.notify(f"❌ Fehler: {e}", color="negative")

    # ── Merkliste toggle ──
    def merkliste_toggle(isbn):
        try:
            merkliste = merkliste_service.merkliste_laden(aktueller_benutzer())
            ist_gemerkt = any(m["isbn"] == isbn for m in merkliste)
            if ist_gemerkt:
                merkliste_service.merkliste_entfernen(aktueller_benutzer(), isbn)
                ui.notify("☆ Von Merkliste entfernt.", color="info")
            else:
                merkliste_service.merkliste_hinzufuegen(aktueller_benutzer(), isbn)
                ui.notify("⭐ Zur Merkliste hinzugefügt.", color="positive")
        except ValueError as e:
            ui.notify(f"❌ {e}", color="negative")
        buecher_laden("")
        if tab_refresh.get("merkliste"):
            tab_refresh["merkliste"]()

    # Initial alle Bücher laden
    buecher_laden()