"""
dashboard.py - Dashboard-Seite
================================
Baut die Navigationsleiste und die Tab-Panels zusammen.
Die eigentlichen Tab-Inhalte kommen aus den tab_*.py Modulen.
"""
 
from nicegui import ui
from Frontend.state import zustand, ist_admin, aktueller_benutzer, service
from Frontend.tabs.tab_buecher import baue_buecher_tab
from Frontend.tabs.tab_ausleihen import baue_ausleihen_tab
from Frontend.tabs.tab_merkliste import baue_merkliste_tab
from Frontend.tabs.tab_admin import baue_admin_tab
 
 
def zeige_dashboard():
    if not zustand["angemeldet"]:
        ui.navigate.to("/")
        return
 
    # Gemeinsames Dict für Tab-übergreifende Refresh-Callbacks
    tab_refresh = {"ausleihen": None, "merkliste": None}
 
    def nav_zu(tab_name: str):
        if tab_refresh.get(tab_name):
            tab_refresh[tab_name]()
        tabs.set_value(tab_name)

    def zeige_popup_ueberfaellig():
        if ist_admin():
            return

        eintraege = service.popup_ueberfaellige_fuer_benutzer(aktueller_benutzer())
        if not eintraege:
            return

        with ui.dialog() as dialog, ui.card().style("max-width:560px; width:100%"):
            ui.label("⚠️ Überfällige Bücher").style("font-size:1.1rem; font-weight:700")
            ui.label(
                "Mindestens eine deiner Ausleihen ist überfällig. Bitte gib das Buch zurück oder melde dich beim Admin."
            ).style("color:#555; margin-bottom:0.25rem")

            for eintrag in eintraege:
                titel = eintrag.get("titel", "Unbekanntes Buch")
                ui.label(f"• {titel} (fällig seit {eintrag['faelligkeit']})").style("color:#b91c1c")

            with ui.row().classes("justify-end w-full gap-2 mt-2"):
                ui.button(
                    "Zu meinen Ausleihen",
                    on_click=lambda: (dialog.close(), nav_zu("ausleihen")),
                ).style("background:#2563eb; color:white")
                ui.button("Schließen", on_click=dialog.close).props("outline")

        dialog.open()

    def zeige_reminder_bald_faellig():
        if ist_admin():
            return

        eintraege = service.reminder_fuer_benutzer(aktueller_benutzer(), tage=7)
        if not eintraege:
            return

        with ui.dialog() as dialog, ui.card().style("max-width:560px; width:100%"):
            ui.label("⏰ Erinnerung: Bald fällige Ausleihen").style("font-size:1.1rem; font-weight:700")
            ui.label(
                "Einige deiner Ausleihen werden in weniger als 7 Tagen fällig."
            ).style("color:#555; margin-bottom:0.25rem")

            for eintrag in eintraege:
                titel = eintrag.get("titel", "Unbekanntes Buch")
                ui.label(f"• {titel} (fällig am {eintrag['faelligkeit']})").style("color:#b45309")

            with ui.row().classes("justify-end w-full gap-2 mt-2"):
                ui.button(
                    "Zu meinen Ausleihen",
                    on_click=lambda: (dialog.close(), nav_zu("ausleihen")),
                ).style("background:#2563eb; color:white")
                ui.button("Schließen", on_click=dialog.close).props("outline")

        dialog.open()
 
    # ── Navigationsleiste ──
    with ui.header().style("background:#1e3a5f; color:white; padding:0.75rem 1.5rem"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("📚 Bibflow").style("font-size:1.3rem; font-weight:700")
            with ui.row().classes("gap-2"):
                ui.button("Bücher", on_click=lambda: tabs.set_value("buecher")).props("flat color=white")
                if not ist_admin():
                    ui.button("Meine Ausleihen", on_click=lambda: nav_zu("ausleihen")).props("flat color=white")
                if not ist_admin():
                    ui.button("Meine Merkliste", on_click=lambda: nav_zu("merkliste")).props("flat color=white")
                if ist_admin():
                    ui.button("Admin", on_click=lambda: tabs.set_value("admin")).props("flat color=white")
                ui.button(
                    f"Abmelden ({aktueller_benutzer()})",
                    on_click=lambda: (
                        zustand.update({"angemeldet": False, "benutzername": "", "rolle": ""}),
                        ui.navigate.to("/"),
                    ),
                ).props("flat color=white")
 
    # ── Haupt-Tabs (unsichtbar, nur zur Steuerung) ──
    with ui.tabs().props("dense").classes("hidden") as tabs:
        ui.tab("buecher")
        if not ist_admin():
            ui.tab("ausleihen")
        if not ist_admin():
            ui.tab("merkliste")
        if ist_admin():
            ui.tab("admin")
 
    # ── Tab-Panels ──
    with ui.tab_panels(tabs, value="buecher").classes("w-full"):
 
        with ui.tab_panel("buecher"):
            baue_buecher_tab(tab_refresh)
 
        if not ist_admin():
            with ui.tab_panel("ausleihen"):
                baue_ausleihen_tab(tab_refresh)
 
        if not ist_admin():
            with ui.tab_panel("merkliste"):
                baue_merkliste_tab(tab_refresh)
 
        if ist_admin():
            with ui.tab_panel("admin"):
                baue_admin_tab()

    if not ist_admin():
        zeige_reminder_bald_faellig()
        zeige_popup_ueberfaellig()