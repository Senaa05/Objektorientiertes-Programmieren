"""
dashboard.py - Dashboard-Seite
================================
Baut die Navigationsleiste und die Tab-Panels zusammen.
Die eigentlichen Tab-Inhalte kommen aus den tab_*.py Modulen.
"""
 
from nicegui import ui
from state import zustand, ist_admin, aktueller_benutzer
from tabs.tab_buecher import baue_buecher_tab
from tabs.tab_ausleihen import baue_ausleihen_tab
from tabs.tab_merkliste import baue_merkliste_tab
from tabs.tab_admin import baue_admin_tab
 
 
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