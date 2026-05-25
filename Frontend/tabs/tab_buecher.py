"""
tab_buecher.py – Bücher-Tab inkl. Karussell
============================================
"""

from nicegui import ui
from Frontend.buch_cover import zeige_buch_cover
from Frontend.state import buch_service, service, merkliste_service, ist_admin, aktueller_benutzer


def baue_buecher_tab(tab_refresh: dict):
    """
    Erstellt den Bücher-Tab-Inhalt.
    tab_refresh ist ein gemeinsames Dict, über das andere Tabs
    nach einer Ausleihe/Merklisten-Aktion neu geladen werden können.
    """
    ui.label("Bücher suchen & ausleihen").style(
        "font-size:1.4rem; font-weight:600; margin:1rem 0"
    )

    with ui.row().classes("items-center gap-2 mb-4"):
        such_input = ui.input(placeholder="Titel, Autor oder ISBN...").style("width:300px")
        ui.button("Suchen", on_click=lambda: buecher_laden(such_input.value)).style(
            "background:#2563eb; color:white"
        )
        ui.button(
    "Zurücksetzen",
        on_click=lambda: (such_input.set_value(""), buecher_laden("")),
    ).props("outline")

    # ── Beliebteste Bücher Karussell ──
    ui.label("Unsere beliebtesten Ausleihen").style(
        "font-size:1.1rem; font-weight:600; margin:0.5rem 0"
    )
    beliebt = buch_service.beliebte_buecher_karussell()

    if beliebt:
        with ui.row().classes("w-full items-center gap-2"):
            pfeil_links = ui.button(
                "←",
                on_click=lambda: karussell.run_method(
                    "scrollBy", {"left": -200, "behavior": "smooth"}
                ),
            ).props("flat dense").style("font-size:1.2rem; min-width:2rem")

            with ui.element("div").style(
                "display:flex; gap:1rem; overflow-x:auto; overflow-y:hidden; "
                "flex:1; scroll-behavior:smooth; padding-bottom:0.25rem;"
            ) as karussell:
                for buch in beliebt:
                    with ui.card().style(
                        "min-width:160px; max-width:160px; padding:0; overflow:hidden; "
                        "flex-shrink:0; display:flex; flex-direction:column;"
                    ):
                        zeige_buch_cover(
                            buch["isbn"],
                            buch["titel"],
                            buch["autor"],
                            karussell=True,
                        )
                        with ui.element("div").style(
                            "padding:0.5rem; flex:1; display:flex; flex-direction:column; "
                            "gap:0.25rem; width:100%; box-sizing:border-box;"
                        ):
                            ui.label(buch["titel"]).style(
                                "font-weight:700; font-size:0.8rem; line-height:1.2; "
                                "display:-webkit-box; -webkit-line-clamp:2; "
                                "-webkit-box-orient:vertical; overflow:hidden;"
                            )
                            ui.label(buch["autor"]).style("font-size:0.75rem; color:#666")
                            ui.label(f"📖 {buch.get('anzahl_ausleihen', 0)}× ausgeliehen").style(
                                "font-size:0.7rem; color:#999"
                            )
                            isbn_kopie = buch["isbn"]
                            verfuegbar = len(buch_service.verfuegbare_exemplare(isbn_kopie)) > 0
                            if verfuegbar and not ist_admin():
                                ui.button(
                                    "Ausleihen",
                                    on_click=lambda _, i=isbn_kopie: buch_ausleihen(i),
                                ).classes("w-full").style("background:#2563eb; color:white")
                            elif not verfuegbar:
                                ui.label("Nicht verfügbar").style(
                                    "color:#dc2626; font-size:0.75rem; margin-top:0.25rem"
                                )

            ui.button(
                "→",
                on_click=lambda: karussell.run_method(
                    "scrollBy", {"left": 200, "behavior": "smooth"}
                ),
            ).props("flat dense").style("font-size:1.2rem; min-width:2rem")
    else:
        ui.label(
            "Noch keine Ausleih-Statistik — lege Bücher aus, um Beliebtheit zu sehen."
        ).style("color:#888; font-size:0.9rem; margin-bottom:0.5rem")

    ui.separator().classes("mb-4")

    # ── Filter-State ──
    sortierung = {"feld": None, "richtung": "asc"}

    # ── Sortierung setzen ──
    def sortierung_setzen(feld, richtung):
        sortierung["feld"] = feld
        sortierung["richtung"] = richtung
        buecher_laden(such_input.value)

    # ── Filter-Leiste ──
    with ui.row().classes("items-center gap-2 w-full flex-wrap").style("margin-bottom:0.5rem;"):
        ui.label("Sortieren:").style("font-weight:600; font-size:0.9rem;")
        ui.button("Titel A-Z",  on_click=lambda: sortierung_setzen("titel", "asc")).props("outline").style("font-size:0.8rem;")
        ui.button("Titel Z-A",  on_click=lambda: sortierung_setzen("titel", "desc")).props("outline").style("font-size:0.8rem;")
        ui.button("Jahr ↑",     on_click=lambda: sortierung_setzen("jahr", "asc")).props("outline").style("font-size:0.8rem;")
        ui.button("Jahr ↓",     on_click=lambda: sortierung_setzen("jahr", "desc")).props("outline").style("font-size:0.8rem;")
        ui.button(
            "Zurücksetzen",
            on_click=lambda: (sortierung.update({"feld": None, "richtung": "asc"}), buecher_laden("")),
        ).props("outline")

    buecher_container = ui.column().classes("w-full gap-2")

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
                ui.label(hinweis).style("color:#888")
            return

        for buch in ergebnisse:
            verfuegbar = len(buch_service.verfuegbare_exemplare(buch["isbn"])) > 0
            with buecher_container:
                with ui.card().classes("w-full").style(
                    "padding:1rem; box-sizing:border-box;"
                ):
                    with ui.row().classes("items-stretch w-full gap-4 no-wrap").style(
                        "width:100%;"
                    ):
                        zeige_buch_cover(buch["isbn"], buch["titel"], buch["autor"])
                        with ui.column().style(
                            "flex:1; min-width:0; justify-content:center; gap:0.25rem;"
                        ):
                            ui.label(buch["titel"]).style(
                                "font-weight:600; font-size:1rem; line-height:1.3;"
                            )
                            ui.label(f"{buch['autor']} · {buch['jahr']}").style(
                                "color:#666; font-size:0.85rem"
                            )
                            ui.label(f"ISBN: {buch['isbn']}").style(
                                "color:#999; font-size:0.8rem"
                            )
                        with ui.row().classes("items-center gap-2 flex-shrink-0"):
                            anzahl_verfuegbar = len(buch_service.verfuegbare_exemplare(buch["isbn"]))
                            if anzahl_verfuegbar > 0:
                                ui.label(f"📗 Exemplare übrig: {anzahl_verfuegbar}").style(
                                    "color:#16a34a"
                                )
                            else:
                                ui.label("❌ Nicht verfügbar").style("color:#dc2626")

                            isbn_kopie = buch["isbn"]
                            if not ist_admin():
                                merkliste = merkliste_service.merkliste_laden(aktueller_benutzer())
                                ist_gemerkt = any(m["isbn"] == isbn_kopie for m in merkliste)
                                stern = "⭐" if ist_gemerkt else "☆"
                                ui.button(
                                    stern,
                                    on_click=lambda _, i=isbn_kopie: merkliste_toggle(i),
                                ).props("flat").style("font-size:1.3rem")
                            if not ist_admin() and verfuegbar:
                                ui.button(
                                    "Ausleihen",
                                    on_click=lambda _, i=isbn_kopie: buch_ausleihen(i),
                                ).style("background:#2563eb; color:white")



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