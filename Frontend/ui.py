"""
Bibliothek NiceGUI - Startdatei mit MockDB
==========================================
"""
 
from nicegui import ui
from datetime import date
 
# ─────────────────────────────────────────────
#  DATENBANK  
# ─────────────────────────────────────────────
 
class DatenbankManager():
    """Simuliert die Datenbank mit festen Testdaten."""
 
    def benutzer_laden(self, benutzername):
        nutzer = {
            "lilly2":  {"benutzername": "lilly2",  "vorname": "Lilly", "nachname": "Müller",    "email": "lilly@example.com",  "rolle": "Benutzer"},
            "admin1":  {"benutzername": "admin1",  "vorname": "Max",   "nachname": "Mustermann", "email": "max@example.com",    "rolle": "Admin"},
        }
        return nutzer.get(benutzername)
 
    def alle_benutzer_laden(self):
        return list(self._benutzer().values())
 
    def _benutzer(self):
        return {
            "lilly2": {"benutzername": "lilly2", "vorname": "Lilly", "nachname": "Müller",    "email": "lilly@example.com",  "rolle": "Benutzer"},
            "admin1": {"benutzername": "admin1", "vorname": "Max",   "nachname": "Mustermann", "email": "max@example.com",    "rolle": "Admin"},
        }
 
    def buch_laden(self, isbn):
        return next((b for b in self._buecher() if b["isbn"] == isbn), None)
 
    def alle_buecher_laden(self):
        return self._buecher()
 
    def bucher_suchen(self, suchbegriff):
        s = suchbegriff.lower()
        return [b for b in self._buecher()
                if s in b["titel"].lower() or s in b["autor"].lower() or s in b["isbn"]]
 
    def _buecher(self):
        return [
            {"isbn": "978-3-123456-78-9", "titel": "Der Alchimist",   "autor": "Paulo Coelho",  "jahr": 1988},
            {"isbn": "978-3-987654-32-1", "titel": "Die Verwandlung",  "autor": "Franz Kafka",   "jahr": 1915},
            {"isbn": "978-3-111111-11-1", "titel": "Faust",            "autor": "Goethe",        "jahr": 1808},
            {"isbn": "978-3-222222-22-2", "titel": "Der Prozess",      "autor": "Franz Kafka",   "jahr": 1925},
        ]
 
    def verfuegbare_exemplare(self, isbn):
        alle = {
            "978-3-123456-78-9": [{"exemplar_id": "EX-001"}, {"exemplar_id": "EX-002"}],
            "978-3-987654-32-1": [{"exemplar_id": "EX-003"}],
            "978-3-111111-11-1": [],
            "978-3-222222-22-2": [{"exemplar_id": "EX-004"}],
        }
        return alle.get(isbn, [])
 
    def anzahl_aktive_ausleihen_benutzer(self, benutzername):
        return len(self.aktive_ausleihen_benutzer(benutzername))
 
    def anzahl_ausleihen_benutzer(self, benutzername):
        return self.anzahl_aktive_ausleihen_benutzer(benutzername)
 
    def aktive_ausleihen_benutzer(self, benutzername):
        alle = {
            "lilly2": [
                {"ausleih_id": "abc-001", "benutzername": "lilly2", "exemplar_id": "EX-001",
                 "titel": "Der Alchimist", "autor": "Paulo Coelho",
                 "ausleihdatum": "2025-04-01", "faelligkeit": "2025-05-01",
                 "verlaengerungsanzahl": 0, "rueckgabedatum": None},
            ],
            "admin1": [],
        }
        return alle.get(benutzername, [])
 
    def ausleihe_laden(self, ausleih_id):
        ausleihen = {
            "abc-001": {"ausleih_id": "abc-001", "benutzername": "lilly2",
                        "exemplar_id": "EX-001", "ausleihdatum": "2025-04-01",
                        "faelligkeit": "2025-05-01", "rueckgabedatum": None,
                        "verlaengerungsanzahl": 0},
        }
        return ausleihen.get(ausleih_id)
 
    def ausleihe_speichern(self, **kwargs):
        return True
 
    def ausleih_speichern(self, **kwargs):
        return True
 
    def exemplar_status_aktualisieren(self, exemplar_id, status):
        return True
 
    def ausleihe_verlaengern(self, ausleih_id, neue_faelligkeit):
        return True
 
    def ausleih_verlaengern(self, ausleih_id, neue_faelligkeit):
        return True
 
    def ausleihe_rueckgabe(self, ausleih_id):
        return True
 
    def ausleih_rueckgabe(self, ausleih_id):
        return True
 
    def ueberfaellige_ausleihen(self):
        return [
            {"ausleih_id": "alt-001", "benutzername": "lilly2",
             "vorname": "Lilly", "nachname": "Müller",
             "titel": "Faust", "faelligkeit": "2025-03-01",
             "exemplar_id": "EX-003"},
        ]
 
    def bald_faellige_ausleihen(self, tage=7):
        return []
 
    def benutzer_hat_ueberfaellige_buecher(self, benutzername):
        return any(e["benutzername"] == benutzername for e in self.ueberfaellige_ausleihen())
 
    def benutzer_speichern(self, benutzername, passwort, vorname, nachname, email, rolle="Benutzer"):
        return True
 
    def buch_speichern(self, titel, autor, isbn, jahr):
        return True
 
    def merkliste_laden(self, benutzername):
        return []
 
    def merkliste_hinzufuegen(self, benutzername, isbn):
        return True
 
    def merkliste_entfernen(self, benutzername, isbn):
        return True
 
 
# ─────────────────────────────────────────────
#  SERVICE INITIALISIEREN
# ─────────────────────────────────────────────
 
# ⬇️  Hier später austauschen:
# from Backend.datenbank.datenbank_manager import DatenbankManager
# db = DatenbankManager()
 
db = DatenbankManager()
 
try:
    from Backend.services.ausleihe_service import AusleiheService
    service = AusleiheService(db)
except ImportError:
    # Falls Backend-Pfad noch nicht passt, Dummy-Service
    class DummyService:
        def buch_ausleihen(self, b, i):     raise ValueError("Service nicht geladen")
        def meine_ausleihen(self, b):       return db.aktive_ausleihen_benutzer(b)
        def ausleihe_verlaengern(self, i):  raise ValueError("Service nicht geladen")
        def buch_zurueckgeben(self, i):     raise ValueError("Service nicht geladen")
        def ueberfaellige_ausleihen(self):  return db.ueberfaellige_ausleihen()
    service = DummyService()
 
 
# ─────────────────────────────────────────────
#  ZUSTAND (einfacher Login-State)
# ─────────────────────────────────────────────
 
zustand = {
    "angemeldet": False,
    "benutzername": "",
    "rolle": "",
}
 
 
# ─────────────────────────────────────────────
#  HILFS-FUNKTIONEN
# ─────────────────────────────────────────────
 
def ist_admin():
    return zustand["rolle"] == "Admin"
 
def aktueller_benutzer():
    return zustand["benutzername"]
 
 
# ─────────────────────────────────────────────
#  SEITEN
# ─────────────────────────────────────────────
 
def zeige_login():
    ui.query("body").style("background: #f0f4f8")
    with ui.card().classes("absolute-center").style("width:360px; padding:2rem"):
        ui.label("📚 Bibliothek").style("font-size:1.8rem; font-weight:700; margin-bottom:1rem")
        benutzername_input = ui.input("Benutzername").classes("w-full")
        passwort_input     = ui.input("Passwort", password=True).classes("w-full")
        fehler_label       = ui.label("").style("color:red; font-size:0.85rem")
 
        def anmelden():
            bn = benutzername_input.value.strip()
            benutzer = db.benutzer_laden(bn)
            if not benutzer:
                fehler_label.set_text("Benutzername nicht gefunden.")
                return
            # Passwort-Prüfung: In Produktion mit Hash!
            if benutzer["passwort"] != passwort_input.value if "passwort" in benutzer else False:
                fehler_label.set_text("Falsches Passwort.")
                return
            zustand["angemeldet"]   = True
            zustand["benutzername"] = bn
            zustand["rolle"]        = benutzer.get("rolle", "Benutzer")
            ui.navigate.to("/dashboard")
 
        ui.button("Anmelden", on_click=anmelden).classes("w-full").style(
            "background:#2563eb; color:white; margin-top:1rem")
 
        ui.label("Testkonten: lilly2 | admin1  (Passwort beliebig)").style(
            "font-size:0.75rem; color:#888; margin-top:0.5rem")
 
 
def zeige_dashboard():
    if not zustand["angemeldet"]:
        ui.navigate.to("/")
        return
 
    # ── Navigationsleiste ──
    with ui.header().style("background:#1e3a5f; color:white; padding:0.75rem 1.5rem"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("📚 Bibliothek").style("font-size:1.3rem; font-weight:700")
            with ui.row().classes("gap-2"):
                ui.button("Bücher",        on_click=lambda: tabs.set_value("buecher")).props("flat color=white")
                ui.button("Meine Ausleihen", on_click=lambda: tabs.set_value("ausleihen")).props("flat color=white")
                if ist_admin():
                    ui.button("Admin", on_click=lambda: tabs.set_value("admin")).props("flat color=white")
                ui.button(f"Abmelden ({aktueller_benutzer()})",
                          on_click=lambda: (zustand.update({"angemeldet": False, "benutzername": "", "rolle": ""}),
                                            ui.navigate.to("/"))
                          ).props("flat color=white")
 
    # ── Haupt-Tabs ──
    with ui.tabs().props("dense").classes("hidden") as tabs:
        ui.tab("buecher")
        ui.tab("ausleihen")
        if ist_admin():
            ui.tab("admin")
 
    with ui.tab_panels(tabs, value="buecher").classes("w-full"):
 
        # ── TAB: BÜCHER ──
        with ui.tab_panel("buecher"):
            ui.label("Bücher suchen & ausleihen").style("font-size:1.4rem; font-weight:600; margin:1rem 0")
 
            with ui.row().classes("items-center gap-2 mb-4"):
                such_input = ui.input(placeholder="Titel, Autor oder ISBN...").style("width:300px")
                ui.button("Suchen", on_click=lambda: buecher_laden(such_input.value)).style(
                    "background:#2563eb; color:white")
                ui.button("Alle anzeigen", on_click=lambda: buecher_laden("")).props("outline")
 
            buecher_container = ui.column().classes("w-full gap-2")
 
            def buecher_laden(suchbegriff=""):
                buecher_container.clear()
                ergebnisse = db.bucher_suchen(suchbegriff) if suchbegriff else db.alle_buecher_laden()
                if not ergebnisse:
                    with buecher_container:
                        ui.label("Keine Bücher gefunden.").style("color:#888")
                    return
                for buch in ergebnisse:
                    verfuegbar = len(db.verfuegbare_exemplare(buch["isbn"])) > 0
                    with buecher_container:
                        with ui.card().classes("w-full").style("padding:1rem"):
                            with ui.row().classes("justify-between items-center w-full"):
                                with ui.column():
                                    ui.label(buch["titel"]).style("font-weight:600; font-size:1rem")
                                    ui.label(f"{buch['autor']} · {buch['jahr']}").style("color:#666; font-size:0.85rem")
                                    ui.label(f"ISBN: {buch['isbn']}").style("color:#999; font-size:0.8rem")
                                with ui.row().classes("items-center gap-2"):
                                    status_text = "✅ Verfügbar" if verfuegbar else "❌ Nicht verfügbar"
                                    status_farbe = "color:#16a34a" if verfuegbar else "color:#dc2626"
                                    ui.label(status_text).style(status_farbe)
                                    if verfuegbar:
                                        isbn_kopie = buch["isbn"]
                                        ui.button("Ausleihen", on_click=lambda _, i=isbn_kopie: buch_ausleihen(i)
                                                  ).style("background:#2563eb; color:white")
 
            def buch_ausleihen(isbn):
                try:
                    ausleih_id = service.buch_ausleihen(aktueller_benutzer(), isbn)
                    ui.notify(f"✅ Erfolgreich ausgeliehen! ID: {ausleih_id[:8]}...", color="positive")
                    buecher_laden("")
                except ValueError as e:
                    ui.notify(f"❌ {e}", color="negative")
 
            # Initial alle Bücher laden
            buecher_laden()
 
        # ── TAB: MEINE AUSLEIHEN ──
        with ui.tab_panel("ausleihen"):
            ui.label("Meine Ausleihen").style("font-size:1.4rem; font-weight:600; margin:1rem 0")
            ausleihen_container = ui.column().classes("w-full gap-2")
 
            def ausleihen_laden():
                ausleihen_container.clear()
                try:
                    ausleihen = service.meine_ausleihen(aktueller_benutzer())
                except Exception:
                    ausleihen = db.aktive_ausleihen_benutzer(aktueller_benutzer())
 
                if not ausleihen:
                    with ausleihen_container:
                        ui.label("Du hast aktuell keine aktiven Ausleihen.").style("color:#888")
                    return
 
                for a in ausleihen:
                    with ausleihen_container:
                        with ui.card().classes("w-full").style("padding:1rem"):
                            with ui.row().classes("justify-between items-center w-full"):
                                with ui.column():
                                    ui.label(a.get("titel", "Unbekanntes Buch")).style("font-weight:600")
                                    ui.label(f"Ausgeliehen: {a['ausleihdatum']}  ·  Fällig: {a['faelligkeit']}"
                                             ).style("color:#666; font-size:0.85rem")
                                    verlaengerungen = a.get("verlaengerungsanzahl", 0)
                                    ui.label(f"Verlängerungen: {verlaengerungen}/1").style(
                                        "font-size:0.8rem; color:#999")
                                with ui.row().classes("gap-2"):
                                    aid = a["ausleih_id"]
                                    if a.get("verlaengerungsanzahl", 0) < 1:
                                        ui.button("Verlängern",
                                                  on_click=lambda _, i=aid: ausleihe_verlaengern(i)
                                                  ).props("outline").style("color:#2563eb")
                                    ui.button("Zurückgeben",
                                              on_click=lambda _, i=aid: buch_zurueckgeben(i)
                                              ).style("background:#dc2626; color:white")
 
            def ausleihe_verlaengern(ausleih_id):
                try:
                    service.ausleihe_verlaengern(ausleih_id)
                    ui.notify("✅ Ausleihe um 14 Tage verlängert.", color="positive")
                    ausleihen_laden()
                except ValueError as e:
                    ui.notify(f"❌ {e}", color="negative")
 
            def buch_zurueckgeben(ausleih_id):
                try:
                    service.buch_zurueckgeben(ausleih_id)
                    ui.notify("✅ Buch zurückgegeben.", color="positive")
                    ausleihen_laden()
                except ValueError as e:
                    ui.notify(f"❌ {e}", color="negative")
 
            ausleihen_laden()
 
        # ── TAB: ADMIN ──
        if ist_admin():
            with ui.tab_panel("admin"):
                ui.label("Admin-Bereich").style("font-size:1.4rem; font-weight:600; margin:1rem 0")
 
                with ui.row().classes("gap-4 w-full"):
 
                    # Überfällige Ausleihen
                    with ui.card().style("flex:1; padding:1rem"):
                        ui.label("⚠️ Überfällige Ausleihen").style("font-weight:600; margin-bottom:0.5rem")
                        try:
                            ueberfaellig = service.ueberfaellige_ausleihen()
                        except Exception:
                            ueberfaellig = db.ueberfaellige_ausleihen()
 
                        if not ueberfaellig:
                            ui.label("Keine überfälligen Ausleihen.").style("color:#888")
                        else:
                            for e in ueberfaellig:
                                with ui.card().style("background:#fef2f2; padding:0.75rem; margin:0.25rem 0"):
                                    ui.label(e.get("titel", "?")).style("font-weight:600")
                                    ui.label(f"Benutzer: {e['benutzername']}  ·  Fällig: {e['faelligkeit']}"
                                             ).style("font-size:0.85rem; color:#dc2626")
 
                    # Neues Buch hinzufügen
                    with ui.card().style("flex:1; padding:1rem"):
                        ui.label("➕ Neues Buch hinzufügen").style("font-weight:600; margin-bottom:0.5rem")
                        titel_in  = ui.input("Titel").classes("w-full")
                        autor_in  = ui.input("Autor").classes("w-full")
                        isbn_in   = ui.input("ISBN").classes("w-full")
                        jahr_in   = ui.number("Erscheinungsjahr", min=1000, max=2100).classes("w-full")
 
                        def buch_hinzufuegen():
                            if not titel_in.value or not autor_in.value or not isbn_in.value:
                                ui.notify("Bitte alle Felder ausfüllen.", color="warning")
                                return
                            ok = db.buch_speichern(titel_in.value, autor_in.value,
                                                   isbn_in.value, int(jahr_in.value or 0))
                            if ok:
                                ui.notify(f"✅ '{titel_in.value}' hinzugefügt.", color="positive")
                                titel_in.set_value("")
                                autor_in.set_value("")
                                isbn_in.set_value("")
                                jahr_in.set_value(None)
                            else:
                                ui.notify("❌ Fehler beim Speichern.", color="negative")
 
                        ui.button("Buch speichern", on_click=buch_hinzufuegen).style(
                            "background:#2563eb; color:white; margin-top:0.5rem")
 
 
# ─────────────────────────────────────────────
#  ROUTEN REGISTRIEREN
# ─────────────────────────────────────────────
 
@ui.page("/")
def login_seite():
    zeige_login()
 
@ui.page("/dashboard")
def dashboard_seite():
    zeige_dashboard()
 
 
# ─────────────────────────────────────────────
#  START
# ─────────────────────────────────────────────
 
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Bibliothek",
        port=8080,
        reload=True,       # Hot-Reload: Änderungen sofort sichtbar
        dark=False,
    )