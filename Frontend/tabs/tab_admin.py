"""
tab_admin.py – Admin-Tab
========================
"""
 
import uuid
from datetime import date
from nicegui import ui
from state import db, service, buch_service, zustand
 
 
def baue_admin_tab():
    """Erstellt den Admin-Tab-Inhalt."""
 
    ui.label("Admin-Bereich").style(
        "font-size:1.4rem; font-weight:600; margin:1rem 0"
    )
 
    with ui.row().classes("gap-4 w-full items-start"):
 
        # ── Linke Spalte ──
        with ui.column().classes("gap-4").style("flex:1"):
            _ueberfaellige_ausleihen()
            _exemplare_verwalten()
 
        # ── Rechte Spalte ──
        with ui.card().style("flex:1; padding:1rem"):
            _buch_hinzufuegen()
            ui.separator()
            _buch_loeschen()
            ui.separator()
            _buch_bearbeiten()
 
 
# ─────────────────────────────────────────────
#  Überfällige Ausleihen
# ─────────────────────────────────────────────
 
def _ueberfaellige_ausleihen():
    with ui.card().classes("w-full").style("padding:1rem"):
        ui.label("⚠️ Überfällige Ausleihen").style(
            "font-weight:600; margin-bottom:0.5rem"
        )
        try:
            ueberfaellig = service.ueberfaellige_ausleihen()
        except Exception:
            ueberfaellig = db.ueberfaellige_ausleihen()
 
        if not ueberfaellig:
            ui.label("Keine überfälligen Ausleihen.").style("color:#888")
        else:
            for e in ueberfaellig:
                with ui.card().style(
                    "background:#fef2f2; padding:0.75rem; margin:0.25rem 0"
                ):
                    ui.label(e.get("titel", "?")).style("font-weight:600")
                    ui.label(
                        f"Benutzer: {e['benutzername']}  ·  Fällig: {e['faelligkeit']}"
                    ).style("font-size:0.85rem; color:#dc2626")
 
 
# ─────────────────────────────────────────────
#  Exemplare verwalten
# ─────────────────────────────────────────────
 
def _exemplare_verwalten():
    with ui.card().classes("w-full").style("padding:1rem"):
        ui.label("📦 Exemplare verwalten").style(
            "font-weight:600; margin-bottom:0.5rem"
        )
 
        with ui.row().classes("items-center gap-2 mb-4"):
            isbn_such  = ui.input(placeholder="ISBN eingeben...").style("width:220px")
            titel_such = ui.input(placeholder="Titel...").style("width:200px")
            autor_such = ui.input(placeholder="Autor...").style("width:200px")
 
            exemplar_container = ui.column().classes("w-full gap-2")
 
            def suche_ausfuehren():
                isbn  = isbn_such.value.strip()
                titel = titel_such.value.strip().lower()
                autor = autor_such.value.strip().lower()
                alle_buecher = db.alle_buecher_laden()
                treffer = [
                    b for b in alle_buecher
                    if (not isbn  or isbn  in b["isbn"])
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
                        ui.label(
                            f"{len(treffer)} Bücher gefunden – bitte auswählen:"
                        ).style("color:#555; margin-bottom:0.5rem")
                        for b in treffer:
                            with ui.card().classes("w-full").style("padding:0.75rem"):
                                with ui.row().classes("justify-between items-center w-full"):
                                    with ui.column():
                                        ui.label(b["titel"]).style("font-weight:600")
                                        ui.label(
                                            f"{b['autor']} · ISBN: {b['isbn']}"
                                        ).style("color:#666; font-size:0.85rem")
                                    ui.button(
                                        "Auswählen",
                                        on_click=lambda _, i=b["isbn"]: exemplare_laden(i),
                                    ).style(
                                        "background:#2563eb; color:white; font-size:0.8rem"
                                    )
 
            ui.button("Suchen", on_click=suche_ausfuehren).style(
                "background:#2563eb; color:white"
            )
            ui.button(
                "Zurücksetzen",
                on_click=lambda: (
                    isbn_such.set_value(""),
                    titel_such.set_value(""),
                    autor_such.set_value(""),
                    exemplar_container.clear(),
                ),
            ).props("outline")
 
        exemplar_container = ui.column().classes("w-full gap-2")
 
        def exemplar_loeschen(exemplar_id, isbn):
            def bestaetigen():
                if db.exemplar_loeschen(exemplar_id):
                    ui.notify(f"✅ Exemplar {exemplar_id} gelöscht.", color="positive")
                else:
                    ui.notify("Exemplar konnte nicht gelöscht werden.", color="negative")
                    dialog.close()
                    return
                dialog.close()
                exemplare_laden(isbn)
 
            with ui.dialog() as dialog, ui.card():
                ui.label("Exemplar wirklich löschen?").style("font-weight:600")
                ui.label(f"Exemplar-ID: {exemplar_id}").style("color:#666")
                with ui.row().classes("gap-2 mt-2"):
                    ui.button("Ja, löschen", on_click=bestaetigen).style(
                        "background:#dc2626; color:white"
                    )
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
                ui.label(
                    f"Buch: {buch['titel']} — {len(alle)} Exemplar(e)"
                ).style("font-weight:600; margin-bottom:0.5rem")
                for ex in alle:
                    farbe = "#16a34a" if ex["status"] == "verfuegbar" else "#dc2626"
                    with ui.card().classes("w-full").style("padding:0.75rem"):
                        with ui.row().classes("justify-between items-center w-full"):
                            with ui.column():
                                ui.label(f"Exemplar-ID: {ex['exemplar_id']}").style(
                                    "font-size:0.9rem"
                                )
                                ui.label(f"Status: {ex['status']}").style(
                                    f"color:{farbe}; font-size:0.85rem"
                                )
                            ex_id = ex["exemplar_id"]
                            if ex["status"] != "verfuegbar":
                                ui.button(
                                    "✅ Verfügbar setzen",
                                    on_click=lambda _, i=ex_id, s=isbn: (
                                        db.exemplar_status_aktualisieren(i, "verfuegbar"),
                                        ui.notify("Status aktualisiert.", color="positive"),
                                        exemplare_laden(s),
                                    ),
                                ).style(
                                    "background:#16a34a; color:white; font-size:0.8rem"
                                )
                            ui.button(
                                "🗑️ Löschen",
                                on_click=lambda _, i=ex_id, s=isbn: exemplar_loeschen(i, s),
                            ).style("background:#dc2626; color:white; font-size:0.8rem")
 
                ui.separator()
                ui.label("Neues Exemplar hinzufügen").style(
                    "font-weight:600; margin-top:0.5rem"
                )
                with ui.row().classes("items-center gap-2"):
                    anzahl_in = ui.number("Anzahl Exemplare", min=1, max=20, value=1).style(
                        "width:200px"
                    )
 
                def exemplar_hinzufuegen(isbn=isbn):
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
                        ui.notify(
                            f"⚠️ {anzahl - fehler} hinzugefügt, {fehler} fehlgeschlagen.",
                            color="warning",
                        )
                    exemplare_laden(isbn)
 
                ui.button("Exemplare hinzufügen", on_click=exemplar_hinzufuegen).style(
                    "background:#2563eb; color:white; margin-top:0.5rem"
                )
 
 
# ─────────────────────────────────────────────
#  Neues Buch hinzufügen
# ─────────────────────────────────────────────
 
def _buch_hinzufuegen():
    ui.label("➕ Neues Buch hinzufügen").style(
        "font-weight:600; margin-bottom:0.5rem"
    )
    titel_in     = ui.input("Titel").classes("w-full")
    autor_in     = ui.input("Autor").classes("w-full")
    isbn_in      = ui.input("ISBN").classes("w-full")
    jahr_in      = ui.input("Erscheinungsjahr (JJJJ)").classes("w-full")
    anzahl_ex_in = ui.number("Anzahl Exemplare", min=1, max=20, value=1).classes("w-full")
 
    def buch_hinzufuegen():
        if not titel_in.value or not autor_in.value or not isbn_in.value or not jahr_in.value:
            ui.notify("Bitte alle Felder ausfüllen.", color="warning")
            return
 
        aktuelles_jahr = date.today().year
        jahr_text = str(jahr_in.value).strip()
        if len(jahr_text) != 4 or not jahr_text.isdigit():
            ui.notify("Das Jahr muss genau 4 Ziffern haben (z. B. 2020).", color="warning")
            return
        jahr = int(jahr_text)
        if jahr < 1000:
            ui.notify("Das Jahr muss mindestens 1000 sein.", color="warning")
            return
        if jahr > aktuelles_jahr:
            ui.notify(
                f"Das Jahr darf nicht in der Zukunft liegen (max. {aktuelles_jahr}).",
                color="warning",
            )
            return
 
        isbn_text = str(isbn_in.value).strip()
        if sum(1 for ch in isbn_text if ch.isdigit()) < 13:
            ui.notify("Die ISBN muss mindestens 13 Ziffern enthalten.", color="warning")
            return
        if db.buch_laden(isbn_text):
            ui.notify("ISBN bereits vorhanden.", color="warning")
            return
 
        ok = db.buch_speichern(titel_in.value, autor_in.value, isbn_text, jahr)
        if ok:
            anzahl = int(anzahl_ex_in.value or 1)
            for _ in range(anzahl):
                neue_id = "EX-" + str(uuid.uuid4())[:6].upper()
                db.exemplar_speichern(neue_id, isbn_in.value)
            ui.notify(
                f"✅ '{titel_in.value}' mit {anzahl} Exemplar(en) hinzugefügt.",
                color="positive",
            )
            titel_in.set_value("")
            autor_in.set_value("")
            isbn_in.set_value("")
            jahr_in.set_value(None)
            anzahl_ex_in.set_value(1)
        else:
            ui.notify("❌ Fehler beim Speichern – ISBN bereits vorhanden?", color="negative")
 
    ui.button("Buch speichern", on_click=buch_hinzufuegen).style(
        "background:#2563eb; color:white; margin-top:0.5rem"
    )
 
 
# ─────────────────────────────────────────────
#  Buch löschen
# ─────────────────────────────────────────────
 
def _buch_loeschen():
    ui.label("🗑️ Buch löschen").style("font-weight:600; margin-top:0.5rem")
 
    with ui.row().classes("gap-2"):
        isbn_loeschen  = ui.input("ISBN").style("width:150px")
        titel_loeschen = ui.input("Titel").style("width:150px")
        autor_loeschen = ui.input("Autor").style("width:150px")
 
    loeschen_container = ui.column().classes("w-full gap-2")
 
    def buecher_zum_loeschen_suchen():
        loeschen_container.clear()
        isbn  = isbn_loeschen.value.strip().lower()
        titel = titel_loeschen.value.strip().lower()
        autor = autor_loeschen.value.strip().lower()
 
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
                            ui.label(
                                f"{b['autor']} · {b['jahr']} · ISBN: {b['isbn']}"
                            ).style("color:#666; font-size:0.85rem")
                        ui.button(
                            "🗑️ Löschen",
                            on_click=lambda _, buch=b: buch_loeschen_bestaetigen(buch),
                        ).style("background:#dc2626; color:white; font-size:0.8rem")
 
    def buch_loeschen_bestaetigen(buch):
        def bestaetigen():
            try:
                buch_service.buch_loeschen(buch["isbn"], zustand.get("rolle", ""))
                ui.notify("✅ Buch wurde erfolgreich gelöscht.", color="positive")
                loeschen_container.clear()
                dialog.close()
            except ValueError as e:
                ui.notify(f"❌ {str(e)}", color="negative")
                dialog.close()
 
        with ui.dialog() as dialog, ui.card():
            ui.label("Buch wirklich löschen?").style("font-weight:600")
            ui.label(
                f"'{buch['titel']}' von {buch['autor']} wird unwiderruflich gelöscht."
            ).style("color:#666")
            with ui.row().classes("gap-2 mt-2"):
                ui.button("Ja, löschen", on_click=bestaetigen).style(
                    "background:#dc2626; color:white"
                )
                ui.button("Abbrechen", on_click=dialog.close).props("outline")
        dialog.open()
 
    with ui.row().classes("gap-2"):
        ui.button("Suchen", on_click=buecher_zum_loeschen_suchen).style(
            "background:#2563eb; color:white"
        )
        ui.button(
            "Zurücksetzen",
            on_click=lambda: (
                isbn_loeschen.set_value(""),
                titel_loeschen.set_value(""),
                autor_loeschen.set_value(""),
                loeschen_container.clear(),
            ),
        ).props("outline")
 
 
# ─────────────────────────────────────────────
#  Buch bearbeiten
# ─────────────────────────────────────────────
 
def _buch_bearbeiten():
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
                    ui.label(
                        f"{b['titel']} — {b['autor']} · {b['jahr']}"
                    ).style("font-weight:600")
                    ui.label(f"ISBN: {b['isbn']}").style("color:#888; font-size:0.8rem")
 
                    neue_isbn   = ui.input("Neue ISBN", value=b["isbn"]).classes("w-full")
                    neuer_titel = ui.input("Neuer Titel", value=b["titel"]).classes("w-full")
                    neuer_autor = ui.input("Neuer Autor", value=b["autor"]).classes("w-full")
                    neues_jahr  = ui.number("Neues Jahr", value=b["jahr"]).classes("w-full")
 
                    def speichern(
                        isbn=b["isbn"],
                        ni=neue_isbn,
                        t=neuer_titel,
                        a=neuer_autor,
                        j=neues_jahr,
                    ):
                        ok = db.buch_bearbeiten(
                            isbn,
                            isbn_neu=ni.value if ni.value else None,
                            titel=t.value if t.value else None,
                            autor=a.value if a.value else None,
                            jahr=int(j.value) if j.value else None,
                        )
                        if ok:
                            ui.notify("✅ Buch erfolgreich aktualisiert.", color="positive")
                            ni.set_value("")
                            t.set_value("")
                            a.set_value("")
                            j.set_value(None)
                            bearb_container.clear()
                        else:
                            ui.notify("❌ Fehler beim Bearbeiten.", color="negative")
 
                    ui.button("💾 Speichern", on_click=speichern).style(
                        "background:#2563eb; color:white; margin-top:0.5rem"
                    )
 
    with ui.row().classes("gap-2"):
        ui.button("Suchen", on_click=buecher_zum_bearbeiten_suchen).style(
            "background:#2563eb; color:white"
        )
        ui.button(
            "Zurücksetzen",
            on_click=lambda: (
                isbn_bearb_such.set_value(""),
                titel_bearb_such.set_value(""),
                autor_bearb_such.set_value(""),
                bearb_container.clear(),
            ),
        ).props("outline")