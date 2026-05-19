"""
Bibliothek NiceGUI - Bibflow
==========================================
"""

from nicegui import ui
from datetime import date
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─────────────────────────────────────────────
#  DATENBANK  
# ─────────────────────────────────────────────
 
class DatenbankManager():
     
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
 
    def anzahl_ausleihen_benutzer(self, benutzername):
        return len(self.ausleihen_benutzer(benutzername))
 
    def anzahl_ausleihen_benutzer(self, benutzername):
        return self.anzahl_ausleihen_benutzer(benutzername)
 
    def ausleihen_benutzer(self, benutzername):
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
 
    def ausleih_laden(self, ausleih_id):
        ausleihen = {
            "abc-001": {"ausleih_id": "abc-001", "benutzername": "lilly2",
                        "exemplar_id": "EX-001", "ausleihdatum": "2025-04-01",
                        "faelligkeit": "2025-05-01", "rueckgabedatum": None,
                        "verlaengerungsanzahl": 0},
        }
        return ausleihen.get(ausleih_id)
 
    def ausleih_speichern(self, **kwargs):
        return True
 
    def ausleih_speichern(self, **kwargs):
        return True
 
    def exemplar_status_aktualisieren(self, exemplar_id, status):
        return True
 
    def ausleih_verlaengern(self, ausleih_id, neue_faelligkeit):
        return True
 
    def ausleih_verlaengern(self, ausleih_id, neue_faelligkeit):
        return True
 
    def ausleih_rueckgabe(self, ausleih_id):
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

basis_pfad = os.path.dirname(os.path.abspath(__file__))
projekt_pfad = os.path.dirname(basis_pfad)

# Alle nötigen Pfade hinzufügen
for pfad in [projekt_pfad,
             os.path.join(projekt_pfad, "Backend"),
             os.path.join(projekt_pfad, "Datenbank")]:
    if pfad not in sys.path:
        sys.path.insert(0, pfad)

db_pfad = os.path.join(projekt_pfad, "Backend", "bibliothek.db")

from Datenbank.DatenbankManager import DatenbankManager
db = DatenbankManager(db_pfad)

try:
    from Backend.services.ausleihe_service import AusleiheService
    _service = AusleiheService(db)

    # Wrapper damit Methodennamen zur UI passen
    class Service:
        def buch_ausleihen(self, b, i):
            return _service.buch_ausleihen(b, i)
        def meine_ausleihen(self, b):
            return _service.meine_ausleihen(b)
        def ausleih_verlaengern(self, i):       # UI ruft diesen Namen auf
            return _service.ausleihe_verlaengern(i)
        def buch_zurueckgeben(self, i):
            return _service.buch_zurueckgeben(i)
        def ueberfaellige_ausleihen(self):
            return _service.ueberfaellige_ausleihen()

    service = Service()
    print("✅ AusleiheService erfolgreich geladen.")

except Exception as e:
    print(f"⚠️ Service-Fehler: {e} – DummyService wird verwendet.")

    class Service:
        def buch_ausleihen(self, b, i):     raise ValueError("Service nicht geladen")
        def meine_ausleihen(self, b):       return db.ausleihen_benutzer(b)
        def ausleih_verlaengern(self, i):   raise ValueError("Service nicht geladen")
        def buch_zurueckgeben(self, i):     raise ValueError("Service nicht geladen")
        def ueberfaellige_ausleihen(self):  return db.ueberfaellige_ausleihen()

    service = Service()
 
 
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
    with ui.card().classes("absolute-center").style("width:400px; padding:2rem"):
        ui.label("Willkommen bei Bibflow").style(
            "font-size:1.6rem; font-weight:700; margin-bottom:1.5rem; text-align:center")

        # Tab-Buttons
        with ui.row().classes("w-full mb-4").style("border:1px solid #ddd; border-radius:6px; overflow:hidden"):
            login_btn = ui.button("Login", on_click=lambda: zeige_tab("login")).style(
                "flex:1; border-radius:0; background:black; color:white")
            reg_btn = ui.button("Registrieren", on_click=lambda: zeige_tab("register")).style(
                "flex:1; border-radius:0; background:white; color:black; border:none")

        fehler_label = ui.label("").style("color:red; font-size:0.85rem")

        # ── LOGIN FELDER ──
        login_panel = ui.column().classes("w-full gap-2")
        with login_panel:
            bn_input = ui.input(placeholder="Benutzername").classes("w-full")
            pw_input = ui.input(placeholder="Passwort", password=True).classes("w-full")

            def anmelden():
                bn = bn_input.value.strip()
                pw = pw_input.value
                benutzer = db.benutzer_laden(bn)
                if not benutzer:
                    fehler_label.set_text("Benutzername nicht gefunden.")
                    return
                if benutzer.get("passwort") != pw:
                    fehler_label.set_text("Falsches Passwort.")
                    return
                zustand["angemeldet"]   = True
                zustand["benutzername"] = bn
                zustand["rolle"]        = benutzer.get("rolle", "Benutzer")
                ui.navigate.to("/dashboard")

            ui.button("Login", on_click=anmelden).classes("w-full").style(
                "background:black; color:white; margin-top:0.5rem")

        # ── REGISTRIEREN FELDER ──
        reg_panel = ui.column().classes("w-full gap-2").style("display:none")
        with reg_panel:
            vorname_in  = ui.input(placeholder="Vorname").classes("w-full")
            nachname_in = ui.input(placeholder="Nachname").classes("w-full")
            email_in    = ui.input(placeholder="Email").classes("w-full")
            reg_bn_in   = ui.input(placeholder="Benutzername").classes("w-full")
            reg_pw_in   = ui.input(placeholder="Passwort", password=True).classes("w-full")

            def registrieren():
                if not all([vorname_in.value, nachname_in.value, email_in.value,
                            reg_bn_in.value, reg_pw_in.value]):
                    fehler_label.set_text("Bitte alle Felder ausfüllen.")
                    return

                # Prüfen ob Benutzername schon existiert
                if db.benutzer_laden(reg_bn_in.value):
                    fehler_label.set_text("Benutzername bereits vergeben.")
                    return

                ok = db.benutzer_speichern(
                    benutzername=reg_bn_in.value,
                    passwort=reg_pw_in.value,
                    vorname=vorname_in.value,
                    nachname=nachname_in.value,
                    email=email_in.value
                )
                if ok:
                    # Direkt prüfen ob der Benutzer wirklich in der DB ist
                    gespeichert = db.benutzer_laden(reg_bn_in.value)
                    if gespeichert:
                        ui.notify("✅ Registrierung erfolgreich! Bitte einloggen.", color="positive")
                        zeige_tab("login")
                    else:
                        fehler_label.set_text("Benutzer wurde nicht gespeichert – Datenbankfehler.")
                else:
                    fehler_label.set_text("Fehler – Benutzername oder Email bereits vergeben.")

            ui.button("Registrieren", on_click=registrieren).classes("w-full").style(
                "background:black; color:white; margin-top:0.5rem")

        # Tab-Wechsel Logik
        def zeige_tab(tab):
            fehler_label.set_text("")
            if tab == "login":
                login_panel.style("display:block")
                reg_panel.style("display:none")
                login_btn.style("background:black; color:white")
                reg_btn.style("background:white; color:black")
            else:
                login_panel.style("display:none")
                reg_panel.style("display:block")
                login_btn.style("background:white; color:black")
                reg_btn.style("background:black; color:white")
 
def zeige_dashboard():
    if not zustand["angemeldet"]:
        ui.navigate.to("/")
        return
 
    # ── Navigationsleiste ──
    with ui.header().style("background:#1e3a5f; color:white; padding:0.75rem 1.5rem"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("📚 Bibflow").style("font-size:1.3rem; font-weight:700")
            with ui.row().classes("gap-2"):
                ui.button("Bücher", on_click=lambda: tabs.set_value("buecher")).props("flat color=white")
                if not ist_admin():
                    ui.button("Meine Ausleihen", on_click=lambda: tabs.set_value("ausleihen")).props("flat color=white")
                if not ist_admin():
                    ui.button("Meine Merkliste", on_click=lambda: tabs.set_value("merkliste")).props("flat color=white")
                if ist_admin():
                    ui.button("Admin", on_click=lambda: tabs.set_value("admin")).props("flat color=white")
                ui.button(f"Abmelden ({aktueller_benutzer()})",
                          on_click=lambda: (zustand.update({"angemeldet": False, "benutzername": "", "rolle": ""}),
                                            ui.navigate.to("/"))
                          ).props("flat color=white")
 
    # ── Haupt-Tabs ──
    with ui.tabs().props("dense").classes("hidden") as tabs:
        ui.tab("buecher")
        if not ist_admin():
            ui.tab("ausleihen")
        if not ist_admin():
            ui.tab("merkliste")
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
                ui.button("Zurücksetzen", on_click=lambda: (such_input.set_value(""), buecher_laden(""))).props("outline")

            # ── Beliebteste Bücher Karussell ──
            ui.label("Unsere beliebtesten Ausleihen").style("font-size:1.1rem; font-weight:600; margin:0.5rem 0")

            cursor = db.connection.cursor()
            cursor.execute('''
                SELECT b.isbn, b.titel, b.autor, b.jahr,
                    COUNT(a.ausleih_id) AS anzahl_ausleihen
                FROM buecher b
                JOIN exemplare e ON b.isbn = e.isbn
                JOIN ausleihen a ON e.exemplar_id = a.exemplar_id
                WHERE a.rueckgabedatum IS NULL
                GROUP BY b.isbn
                HAVING COUNT(a.ausleih_id) >= 2
                ORDER BY anzahl_ausleihen DESC
                LIMIT 5
            ''')
            beliebt = [dict(row) for row in cursor.fetchall()]

            if beliebt:
                with ui.row().classes("w-full items-center gap-2"):

                    # Pfeil links
                    pfeil_links = ui.button("←", on_click=lambda: karussell.run_method(
                        "scrollBy", {"left": -200, "behavior": "smooth"}
                    )).props("flat dense").style("font-size:1.2rem; min-width:2rem")

                    # Scrollbarer Container
                    with ui.element("div").style(
                        "display:flex; gap:1rem; overflow:hidden; flex:1; scroll-behavior:smooth"
                    ) as karussell:
                        farben = ["#fce7f3", "#dbeafe", "#dcfce7", "#fef9c3", "#ede9fe"]
                        for idx, buch in enumerate(beliebt):
                            with ui.card().style(
                                "min-width:160px; max-width:160px; padding:0; overflow:hidden; flex-shrink:0"):
                                farbe = farben[idx % len(farben)]
                                with ui.element("div").style(
                                    f"background:{farbe}; height:120px; display:flex; "
                                    f"align-items:center; justify-content:center; padding:0.5rem"):
                                    ui.label(buch["titel"]).style(
                                        "font-weight:700; font-size:0.85rem; text-align:center; "
                                        "word-break:break-word")
                                with ui.element("div").style("padding:0.5rem"):
                                    ui.label(buch["autor"]).style("font-size:0.75rem; color:#666")
                                    ui.label(f"📖 {buch.get('anzahl_ausleihen', 0)}x ausgeliehen"
                                            ).style("font-size:0.7rem; color:#999")
                                    isbn_kopie = buch["isbn"]
                                    verfuegbar = len(db.verfuegbare_exemplare(isbn_kopie)) > 0
                                    if verfuegbar:
                                        ui.button("Ausleihen",
                                            on_click=lambda _, i=isbn_kopie: buch_ausleihen(i)
                                        ).classes("w-full").style(
                                            "background:#1e3a5f; color:white; font-size:0.75rem; "
                                            "margin-top:0.25rem")
                                    else:
                                        ui.label("Nicht verfügbar").style(
                                            "color:#dc2626; font-size:0.75rem; margin-top:0.25rem")

                    # Pfeil rechts
                    ui.button("→", on_click=lambda: karussell.run_method(
                        "scrollBy", {"left": 200, "behavior": "smooth"}
                    )).props("flat dense").style("font-size:1.2rem; min-width:2rem")

            ui.separator().classes("mb-4")

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
                                    anzahl_verfuegbar = len(db.verfuegbare_exemplare(buch["isbn"]))
                                    if anzahl_verfuegbar > 0:
                                        ui.label(f"📗 Exemplare übrig: {anzahl_verfuegbar}").style("color:#16a34a")
                                    else:
                                        ui.label("❌ Nicht verfügbar").style("color:#dc2626")
                                    isbn_kopie = buch["isbn"]
                                    if not ist_admin():
                                        merkliste = db.merkliste_laden(aktueller_benutzer())
                                        ist_gemerkt = any(m["isbn"] == isbn_kopie for m in merkliste)
                                        stern = "⭐" if ist_gemerkt else "☆"
                                        ui.button(stern,
                                            on_click=lambda _, i=isbn_kopie: merkliste_toggle(i)
                                        ).props("flat").style("font-size:1.3rem")
                                    if not ist_admin() and verfuegbar:
                                        ui.button("Ausleihen", on_click=lambda _, i=isbn_kopie: buch_ausleihen(i)
                                                  ).style("background:#2563eb; color:white")
 
            def buch_ausleihen(isbn):
                try:
                    ausleih_id = service.buch_ausleihen(aktueller_benutzer(), isbn)
                    ui.notify(f"✅ Erfolgreich ausgeliehen!", color="positive")
                    buecher_laden("")
                except ValueError as e:
                    ui.notify(f"❌ {e}", color="negative")

            def merkliste_toggle(isbn):
                merkliste = db.merkliste_laden(aktueller_benutzer())
                ist_gemerkt = any(m["isbn"] == isbn for m in merkliste)
                if ist_gemerkt:
                    db.merkliste_entfernen(aktueller_benutzer(), isbn)
                    ui.notify("☆ Von Merkliste entfernt.", color="info")
                else:
                    db.merkliste_hinzufuegen(aktueller_benutzer(), isbn)
                    ui.notify("⭐ Zur Merkliste hinzugefügt.", color="positive")
                buecher_laden("")
            # Initial alle Bücher laden
            buecher_laden()
 
        # ── TAB: MEINE AUSLEIHEN ──
        if not ist_admin():
            with ui.tab_panel("ausleihen"):
                ui.label("Meine Ausleihen").style("font-size:1.4rem; font-weight:600; margin:1rem 0")
                ausleihen_container = ui.column().classes("w-full gap-2")
    
                def ausleihen_laden():
                    ausleihen_container.clear()
                    try:
                        ausleihen = service.meine_ausleihen(aktueller_benutzer())
                    except Exception:
                        ausleihen = db.ausleihen_benutzer(aktueller_benutzer())
    
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
                                                    on_click=lambda _, i=aid: ausleih_verlaengern(i)
                                                    ).props("outline").style("color:#2563eb")
                                        ui.button("Zurückgeben",
                                                on_click=lambda _, i=aid: buch_zurueckgeben(i)
                                                ).style("background:#dc2626; color:white")
 
            def ausleih_verlaengern(ausleih_id):
                try:
                    service.ausleih_verlaengern(ausleih_id)
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

        # ── TAB: MEINE MERKLISTE ──
        if not ist_admin():
            with ui.tab_panel("merkliste"):
                ui.label("Meine Merkliste").style("font-size:1.4rem; font-weight:600; margin:1rem 0")
                merkliste_container = ui.column().classes("w-full gap-2")

                def merkliste_laden_seite():
                    merkliste_container.clear()
                    eintraege = db.merkliste_laden(aktueller_benutzer())
                    if not eintraege:
                        with merkliste_container:
                            ui.label("Deine Merkliste ist leer.").style("color:#888")
                        return
                    for eintrag in eintraege:
                        verfuegbar = len(db.verfuegbare_exemplare(eintrag["isbn"])) > 0
                        with merkliste_container:
                            with ui.card().classes("w-full").style("padding:1rem"):
                                with ui.row().classes("justify-between items-center w-full"):
                                    with ui.column():
                                        ui.label(eintrag["titel"]).style("font-weight:600; font-size:1rem")
                                        ui.label(f"{eintrag['autor']} · ISBN: {eintrag['isbn']}"
                                                 ).style("color:#666; font-size:0.85rem")
                                        anzahl = len(db.verfuegbare_exemplare(eintrag["isbn"]))
                                        if anzahl > 0:
                                            ui.label(f"📗 Exemplare übrig: {anzahl}").style("color:#16a34a")
                                        else:
                                            ui.label("❌ Nicht verfügbar").style("color:#dc2626")
                                    with ui.row().classes("gap-2"):
                                        isbn_kopie = eintrag["isbn"]
                                        if verfuegbar:
                                            ui.button("Ausleihen",
                                                on_click=lambda _, i=isbn_kopie: buch_ausleihen(i)
                                            ).style("background:#2563eb; color:white")
                                        ui.button("⭐ Entfernen",
                                            on_click=lambda _, i=isbn_kopie: (
                                                db.merkliste_entfernen(aktueller_benutzer(), i),
                                                ui.notify("☆ Von Merkliste entfernt.", color="info"),
                                                merkliste_laden_seite()
                                            )
                                        ).props("outline").style("color:#dc2626")

                merkliste_laden_seite()

        # ── TAB: ADMIN ──
        if ist_admin():
            with ui.tab_panel("admin"):
                ui.label("Admin-Bereich").style("font-size:1.4rem; font-weight:600; margin:1rem 0")
 
                with ui.row().classes("gap-4 w-full items-start"):

                    #Linke Spalte
                    with ui.column().classes("gap-4").style('flex:1'): 
                    # Überfällige Ausleihen
                        with ui.card().classes("w-full").style("padding:1rem"):
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
                        # ── Exemplare verwalten ──
                        with ui.card().classes("w-full").style("padding:1rem"):
                            ui.label("📦 Exemplare verwalten").style("font-weight:600; margin-bottom:0.5rem")

                            with ui.row().classes("items-center gap-2 mb-4"):
                                isbn_such = ui.input(placeholder="ISBN eingeben...").style("width:220px")
                                titel_such = ui.input(placeholder="Titel...").style("width:200px")
                                autor_such = ui.input(placeholder="Autor...").style("width:200px")

                                def suche_ausfuehren():
                                    isbn = isbn_such.value.strip()
                                    titel = titel_such.value.strip().lower()
                                    autor = autor_such.value.strip().lower()
                                    alle_buecher = db.alle_buecher_laden()
                                    treffer = [
                                        b for b in alle_buecher
                                        if (not isbn or isbn in b["isbn"])
                                        and (not titel or titel in b["titel"].lower())
                                        and (not autor or autor in b["autor"].lower())
                                    ]
                                    if not treffer:
                                        exemplar_container.clear()
                                        with exemplar_container:
                                            ui.label("Keine Bücher gefunden.").style("color:#888")
                                        return
                                    if len(treffer) == 1:
                                        exemplare_laden(treffer[0]["isbn"])
                                    else:
                                        exemplar_container.clear()
                                        with exemplar_container:
                                            ui.label(f"{len(treffer)} Bücher gefunden – bitte auswählen:").style("color:#555; margin-bottom:0.5rem")
                                            for b in treffer:
                                                with ui.card().classes("w-full").style("padding:0.75rem"):
                                                    with ui.row().classes("justify-between items-center w-full"):
                                                        with ui.column():
                                                            ui.label(b["titel"]).style("font-weight:600")
                                                            ui.label(f"{b['autor']} · ISBN: {b['isbn']}").style("color:#666; font-size:0.85rem")
                                                        ui.button("Auswählen",
                                                            on_click=lambda _, i=b["isbn"]: exemplare_laden(i)
                                                        ).style("background:#2563eb; color:white; font-size:0.8rem")

                                ui.button("Suchen", on_click=suche_ausfuehren).style("background:#2563eb; color:white")
                                ui.button("Zurücksetzen", on_click=lambda: (
                                    isbn_such.set_value(""),
                                    titel_such.set_value(""),
                                    autor_such.set_value(""),
                                    exemplar_container.clear()
                                )).props("outline")

                            exemplar_container = ui.column().classes("w-full gap-2")
                            def exemplar_loeschen(exemplar_id, isbn):
                                def bestaetigen():
                                    cursor = db.connection.cursor()
                                    cursor.execute("DELETE FROM exemplare WHERE exemplar_id = ?", (exemplar_id,))
                                    db.connection.commit()
                                    ui.notify(f"✅ Exemplar {exemplar_id} gelöscht.", color="positive")
                                    dialog.close()
                                    exemplare_laden(isbn)

                                with ui.dialog() as dialog, ui.card():
                                    ui.label("Exemplar wirklich löschen?").style("font-weight:600")
                                    ui.label(f"Exemplar-ID: {exemplar_id}").style("color:#666")
                                    with ui.row().classes("gap-2 mt-2"):
                                        ui.button("Ja, löschen", on_click=bestaetigen).style("background:#dc2626; color:white")
                                        ui.button("Abbrechen", on_click=dialog.close).props("outline")
                                dialog.open()

                            def exemplare_laden(isbn):
                                exemplar_container.clear()
                                if not isbn:
                                    ui.notify("Bitte ISBN eingeben.", color="warning")
                                    return
                                buch = db.buch_laden(isbn)
                                if not buch:
                                    with exemplar_container:
                                        ui.label("Kein Buch mit dieser ISBN gefunden.").style("color:#888")
                                    return
                                alle = db.exemplare_laden(isbn)
                                with exemplar_container:
                                    ui.label(f"Buch: {buch['titel']} — {len(alle)} Exemplar(e)").style(
                                        "font-weight:600; margin-bottom:0.5rem")
                                    for ex in alle:
                                        farbe = "#16a34a" if ex["status"] == "verfuegbar" else "#dc2626"
                                        with ui.card().classes("w-full").style("padding:0.75rem"):
                                            with ui.row().classes("justify-between items-center w-full"):
                                                with ui.column():
                                                    ui.label(f"Exemplar-ID: {ex['exemplar_id']}").style("font-size:0.9rem")
                                                    ui.label(f"Status: {ex['status']}").style(f"color:{farbe}; font-size:0.85rem")
                                                ex_id = ex["exemplar_id"]
                                                if ex["status"] != "verfuegbar":
                                                    ui.button("✅ Verfügbar setzen",
                                                        on_click=lambda _, i=ex_id, s=isbn: (
                                                            db.exemplar_status_aktualisieren(i, "verfuegbar"),
                                                            ui.notify("Status aktualisiert.", color="positive"),
                                                            exemplare_laden(s)
                                                        )).style("background:#16a34a; color:white; font-size:0.8rem")

                                                ui.button("🗑️ Löschen",
                                                    on_click=lambda _, i=ex_id, s=isbn: exemplar_loeschen(i, s)
                                                ).style("background:#dc2626; color:white; font-size:0.8rem")
                                    ui.separator()
                                    ui.label("Neues Exemplar hinzufügen").style("font-weight:600; margin-top:0.5rem")
                                    with ui.row().classes("items-center gap-2"):
                                        anzahl_in = ui.number("Anzahl Exemplare", min=1, max=20, value=1).style("width:200px")

                                    def exemplar_hinzufuegen(isbn=isbn):
                                        import uuid
                                        anzahl = int(anzahl_in.value or 1)
                                        fehler = 0
                                        for _ in range(anzahl):
                                            neue_id = "EX-" + str(uuid.uuid4())[:6].upper()
                                            ok = db.exemplar_speichern(neue_id, isbn)
                                            if not ok:
                                                fehler += 1
                                        if fehler == 0:
                                            ui.notify(f"✅ {anzahl} Exemplar(e) hinzugefügt.", color="positive")
                                        else:
                                            ui.notify(f"⚠️ {anzahl - fehler} hinzugefügt, {fehler} fehlgeschlagen.", color="warning")
                                        exemplare_laden(isbn)

                                    ui.button("Exemplare hinzufügen", on_click=exemplar_hinzufuegen).style(
                                        "background:#2563eb; color:white; margin-top:0.5rem")
                    #Rechte Spalte
                    # Neues Buch hinzufügen
                    with ui.card().style("flex:1; padding:1rem"):
                        ui.label("➕ Neues Buch hinzufügen").style("font-weight:600; margin-bottom:0.5rem")
                        titel_in  = ui.input("Titel").classes("w-full")
                        autor_in  = ui.input("Autor").classes("w-full")
                        isbn_in   = ui.input("ISBN").classes("w-full")
                        jahr_in = ui.number("Erscheinungsjahr", min=1000, max=2100).classes("w-full")
                        anzahl_ex_in = ui.number("Anzahl Exemplare", min=1, max=20, value=1).classes("w-full") 

                        def buch_hinzufuegen():
                            if not titel_in.value or not autor_in.value or not isbn_in.value or not jahr_in.value:
                                ui.notify("Bitte alle Felder ausfüllen.", color="warning")
                                return
                            ok = db.buch_speichern(titel_in.value, autor_in.value,
                                                isbn_in.value, int(jahr_in.value or 1000))
                            if ok:
                                # Exemplare automatisch hinzufügen
                                import uuid
                                anzahl = int(anzahl_ex_in.value or 1)
                                for _ in range(anzahl):
                                    neue_id = "EX-" + str(uuid.uuid4())[:6].upper()
                                    db.exemplar_speichern(neue_id, isbn_in.value)

                                ui.notify(f"✅ '{titel_in.value}' mit {anzahl} Exemplar(en) hinzugefügt.", color="positive")
                                titel_in.set_value("")
                                autor_in.set_value("")
                                isbn_in.set_value("")
                                jahr_in.set_value(None)
                                anzahl_ex_in.set_value(1)
                            else:
                                ui.notify("❌ Fehler beim Speichern – ISBN bereits vorhanden?", color="negative")

                        ui.button("Buch speichern", on_click=buch_hinzufuegen).style(
                            "background:#2563eb; color:white; margin-top:0.5rem")

                        ui.separator()
                        ui.label("🗑️ Buch löschen").style("font-weight:600; margin-top:0.5rem")

                        with ui.row().classes("gap-2"):
                            isbn_loeschen  = ui.input("ISBN").style("width:150px")
                            titel_loeschen = ui.input("Titel").style("width:150px")
                            autor_loeschen = ui.input("Autor").style("width:150px")

                        loeschen_container = ui.column().classes("w-full gap-2")

                        def buecher_zum_loeschen_suchen():
                            loeschen_container.clear()
                            isbn   = isbn_loeschen.value.strip().lower()
                            titel  = titel_loeschen.value.strip().lower()
                            autor  = autor_loeschen.value.strip().lower()

                            if not isbn and not titel and not autor:
                                ui.notify("Bitte mindestens ein Suchfeld ausfüllen.", color="warning")
                                return

                            alle = db.alle_buecher_laden()
                            treffer = [
                                b for b in alle
                                if (not isbn  or isbn  in b["isbn"].lower())
                                and (not titel or titel in b["titel"].lower())
                                and (not autor or autor in b["autor"].lower())
                            ]

                            if not treffer:
                                with loeschen_container:
                                    ui.label("Keine Bücher gefunden.").style("color:#888")
                                return

                            with loeschen_container:
                                for b in treffer:
                                    with ui.card().classes("w-full").style("padding:0.75rem"):
                                        with ui.row().classes("justify-between items-center w-full"):
                                            with ui.column():
                                                ui.label(b["titel"]).style("font-weight:600")
                                                ui.label(f"{b['autor']} · {b['jahr']} · ISBN: {b['isbn']}"
                                                        ).style("color:#666; font-size:0.85rem")
                                            ui.button("🗑️ Löschen",
                                                    on_click=lambda _, buch=b: buch_loeschen_bestaetigen(buch)
                                                    ).style("background:#dc2626; color:white; font-size:0.8rem")

                        def buch_loeschen_bestaetigen(buch):
                            def bestaetigen():
                                ok = db.buch_loeschen(buch["isbn"])
                                if ok:
                                    ui.notify("✅ Buch wurde erfolgreich gelöscht.", color="positive")
                                    loeschen_container.clear()
                                    dialog.close()
                                else:
                                    ui.notify("❌ Löschen fehlgeschlagen – möglicherweise noch Exemplare ausgeliehen.", color="negative")
                                    dialog.close()

                            with ui.dialog() as dialog, ui.card():
                                ui.label("Buch wirklich löschen?").style("font-weight:600")
                                ui.label(f"'{buch['titel']}' von {buch['autor']} wird unwiderruflich gelöscht."
                                        ).style("color:#666")
                                with ui.row().classes("gap-2 mt-2"):
                                    ui.button("Ja, löschen", on_click=bestaetigen).style("background:#dc2626; color:white")
                                    ui.button("Abbrechen", on_click=dialog.close).props("outline")
                            dialog.open()

                        with ui.row().classes("gap-2"):
                            ui.button("Suchen", on_click=buecher_zum_loeschen_suchen).style("background:#2563eb; color:white")
                            ui.button("Zurücksetzen", on_click=lambda: (
                                        isbn_loeschen.set_value(""),
                                        titel_loeschen.set_value(""),
                                        autor_loeschen.set_value(""),
                                        loeschen_container.clear()
                                    )).props("outline")
                            
                        # ── Bücher bearbeiten ──
                        ui.separator()
                        ui.label("✏️ Buch bearbeiten").style("font-weight:600; margin-top:0.5rem")

                        with ui.row().classes("gap-2"):
                            isbn_bearb_such  = ui.input("ISBN").style("width:150px")
                            titel_bearb_such = ui.input("Titel").style("width:150px")
                            autor_bearb_such = ui.input("Autor").style("width:150px")

                        bearb_container = ui.column().classes("w-full gap-2")

                        def buecher_zum_bearbeiten_suchen():
                            bearb_container.clear()
                            isbn  = isbn_bearb_such.value.strip().lower()
                            titel = titel_bearb_such.value.strip().lower()
                            autor = autor_bearb_such.value.strip().lower()

                            if not isbn and not titel and not autor:
                                ui.notify("Bitte mindestens ein Suchfeld ausfüllen.", color="warning")
                                return

                            alle = db.alle_buecher_laden()
                            treffer = [
                                b for b in alle
                                if (not isbn  or isbn  in b["isbn"].lower())
                                and (not titel or titel in b["titel"].lower())
                                and (not autor or autor in b["autor"].lower())
                            ]

                            if not treffer:
                                with bearb_container:
                                    ui.label("Keine Bücher gefunden.").style("color:#888")
                                return

                            with bearb_container:
                                for b in treffer:
                                    with ui.card().classes("w-full").style("padding:0.75rem"):
                                        ui.label(f"{b['titel']} — {b['autor']} · {b['jahr']}").style("font-weight:600")
                                        ui.label(f"ISBN: {b['isbn']}").style("color:#888; font-size:0.8rem")

                                        neuer_titel = ui.input("Neuer Titel", value=b["titel"]).classes("w-full")
                                        neuer_autor = ui.input("Neuer Autor", value=b["autor"]).classes("w-full")
                                        neues_jahr = ui.number("Neues Jahr", value=b["jahr"]).classes("w-full")

                                        def speichern(isbn=b["isbn"], t=neuer_titel, a=neuer_autor, j=neues_jahr):
                                            ok = db.buch_bearbeiten(
                                                isbn,
                                                titel=t.value if t.value else None,
                                                autor=a.value if a.value else None,
                                                jahr=int(j.value) if j.value else None
                                            )
                                            if ok:
                                                ui.notify("✅ Buch erfolgreich aktualisiert.", color="positive")
                                                t.set_value("")
                                                a.set_value("")
                                                j.set_value(None)
                                                bearb_container.clear()
                                            else:
                                                ui.notify("❌ Fehler beim Bearbeiten.", color="negative")

                                        ui.button("💾 Speichern", on_click=speichern).style(
                                            "background:#2563eb; color:white; margin-top:0.5rem")

                        with ui.row().classes("gap-2"):
                            ui.button("Suchen", on_click=buecher_zum_bearbeiten_suchen).style("background:#2563eb; color:white")
                            ui.button("Zurücksetzen", on_click=lambda: (
                                        isbn_bearb_such.set_value(""),
                                        titel_bearb_such.set_value(""),
                                        autor_bearb_such.set_value(""),
                                        bearb_container.clear()
                                )).props("outline")

                    
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
        show=True,           # Browser automatisch öffnen
    )