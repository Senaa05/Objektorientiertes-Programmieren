"""
tab_admin.py – Admin-Tab
========================
"""

import uuid
from datetime import date
from nicegui import ui
from Frontend.state import buch_service, service, zustand


def baue_admin_tab():
    """Erstellt den Admin-Tab-Inhalt."""

    ui.label("Admin-Bereich").classes("text-2xl font-semibold my-4")

    with ui.row().classes("gap-4 w-full items-start"):

        # ── Linke Spalte ──
        with ui.column().classes("gap-4 flex-1"):
            _ueberfaellige_ausleihen()
            _exemplare_verwalten()

        # ── Rechte Spalte ──
        with ui.card().classes("flex-1 p-4"):
            _buch_hinzufuegen()
            ui.separator()
            _buch_loeschen()
            ui.separator()
            _buch_bearbeiten()


# ─────────────────────────────────────────────
#  Überfällige Ausleihen
# ─────────────────────────────────────────────

def _ueberfaellige_ausleihen():
    with ui.card().classes("w-full p-4"):
        ui.label("⚠️ Überfällige Ausleihen").classes("font-semibold mb-2")
        try:
            ueberfaellig = service.ueberfaellige_ausleihen()
        except Exception:
            ueberfaellig = service.ueberfaellige_ausleihen()

        if not ueberfaellig:
            ui.label("Keine überfälligen Ausleihen.").classes("text-gray-400")
        else:
            for e in ueberfaellig:
                with ui.card().classes("bg-red-50 p-3 my-1"):
                    ui.label(e.get("titel", "?")).classes("font-semibold")
                    ui.label(
                        f"Benutzer: {e['benutzername']}  ·  Fällig: {e['faelligkeit']}"
                    ).classes("text-sm text-red-600")


# ─────────────────────────────────────────────
#  Exemplare verwalten
# ─────────────────────────────────────────────

def _exemplare_verwalten():
    with ui.card().classes("w-full p-4"):
        ui.label("📦 Exemplare verwalten").classes("font-semibold mb-2")

        exemplar_container = ui.column().classes("w-full gap-2")

        with ui.row().classes("items-center gap-2 mb-4"):
            isbn_such  = ui.input(placeholder="ISBN eingeben...").classes("w-52")
            titel_such = ui.input(placeholder="Titel...").classes("w-48")
            autor_such = ui.input(placeholder="Autor...").classes("w-48")

            def suche_ausfuehren():
                isbn  = isbn_such.value.strip()
                titel = titel_such.value.strip().lower()
                autor = autor_such.value.strip().lower()
                alle_buecher = buch_service.alle_buecher_laden()
                treffer = [
                    b for b in alle_buecher
                    if (not isbn  or isbn  in b["isbn"])
                    and (not titel or titel in b["titel"].lower())
                    and (not autor or autor in b["autor"].lower())
                ]
                if not treffer:
                    exemplar_container.clear()
                    with exemplar_container:
                        ui.label("Keine Bücher gefunden.").classes("text-gray-400")
                    return
                if len(treffer) == 1:
                    exemplare_laden(treffer[0]["isbn"])
                else:
                    exemplar_container.clear()
                    with exemplar_container:
                        ui.label(
                            f"{len(treffer)} Bücher gefunden – bitte auswählen:"
                        ).classes("text-gray-500 mb-2")
                        for b in treffer:
                            with ui.card().classes("w-full p-3"):
                                with ui.row().classes("justify-between items-center w-full"):
                                    with ui.column():
                                        ui.label(b["titel"]).classes("font-semibold")
                                        ui.label(
                                            f"{b['autor']} · ISBN: {b['isbn']}"
                                        ).classes("text-gray-500 text-sm")
                                    ui.button(
                                        "Auswählen",
                                        on_click=lambda _, i=b["isbn"]: exemplare_laden(i),
                                    ).classes("bg-blue-600 text-white text-xs")

            ui.button("Suchen", on_click=suche_ausfuehren).classes("bg-blue-600 text-white")
            ui.button(
                "Zurücksetzen",
                on_click=lambda: (
                    isbn_such.set_value(""),
                    titel_such.set_value(""),
                    autor_such.set_value(""),
                    exemplar_container.clear(),
                ),
            ).props("outline")

        def exemplar_loeschen(exemplar_id, isbn):
            def bestaetigen():
                try:
                    erfolg = buch_service.exemplar_loeschen(exemplar_id)
                except ValueError as err:
                    ui.notify(str(err), color="negative")
                    dialog.close()
                    return
                except Exception:
                    ui.notify("Unbekannter Fehler beim Löschen des Exemplars.", color="negative")
                    dialog.close()
                    return

                if erfolg:
                    ui.notify(f"✅ Exemplar {exemplar_id} gelöscht.", color="positive")
                else:
                    ui.notify("Exemplar konnte nicht gelöscht werden.", color="negative")
                    dialog.close()
                    return

                dialog.close()
                exemplare_laden(isbn)

            with ui.dialog() as dialog, ui.card():
                ui.label("Exemplar wirklich löschen?").classes("font-semibold")
                ui.label(f"Exemplar-ID: {exemplar_id}").classes("text-gray-500")
                with ui.row().classes("gap-2 mt-2"):
                    ui.button("Ja, löschen", on_click=bestaetigen).classes("bg-red-600 text-white")
                    ui.button("Abbrechen", on_click=dialog.close).props("outline")
            dialog.open()

        def exemplare_laden(isbn):
            exemplar_container.clear()
            if not isbn:
                ui.notify("Bitte ISBN eingeben.", color="warning")
                return

            try:
                buch = buch_service.buch_laden(isbn)
            except ValueError:
                with exemplar_container:
                    ui.label("Kein Buch mit dieser ISBN gefunden.").classes("text-gray-400")
                return

            buch_titel = buch.titel if hasattr(buch, "titel") else buch.get("titel", "?")
            alle = buch_service.exemplare_laden(isbn)
            with exemplar_container:
                ui.label(
                    f"Buch: {buch_titel} — {len(alle)} Exemplar(e)"
                ).classes("font-semibold mb-2")
                for ex in alle:
                    farbe = "text-green-600" if ex["status"] == "verfuegbar" else "text-red-600"
                    with ui.card().classes("w-full p-3"):
                        with ui.row().classes("justify-between items-center w-full"):
                            with ui.column():
                                ui.label(f"Exemplar-ID: {ex['exemplar_id']}").classes("text-sm")
                                ui.label(f"Status: {ex['status']}").classes(f"{farbe} text-sm")
                            ex_id = ex["exemplar_id"]
                            if ex["status"] != "verfuegbar":
                                ui.button(
                                    "✅ Verfügbar setzen",
                                    on_click=lambda _, i=ex_id, s=isbn: (
                                        buch_service.exemplar_status_aktualisieren(i, "verfuegbar"),
                                        ui.notify("Status aktualisiert.", color="positive"),
                                        exemplare_laden(s),
                                    ),
                                ).classes("bg-green-600 text-white text-xs")

                            ui.button(
                                "🗑️ Löschen",
                                on_click=lambda _, i=ex_id, s=isbn: exemplar_loeschen(i, s),
                            ).classes("bg-red-600 text-white text-xs")

                ui.separator()
                ui.label("Neues Exemplar hinzufügen").classes("font-semibold mt-2")
                with ui.row().classes("items-center gap-2"):
                    anzahl_in = ui.number("Anzahl Exemplare", min=1, max=20, value=1).classes("w-48")

                def exemplar_hinzufuegen(isbn=isbn):
                    anzahl = int(anzahl_in.value or 1)
                    fehler = 0
                    for _ in range(anzahl):
                        neue_id = "EX-" + str(uuid.uuid4())[:6].upper()
                        try:
                            buch_service.exemplar_speichern(neue_id, isbn)
                        except ValueError:
                            fehler += 1
                    if fehler == 0:
                        ui.notify(f"✅ {anzahl} Exemplar(e) hinzugefügt.", color="positive")
                    else:
                        ui.notify(
                            f"⚠️ {anzahl - fehler} hinzugefügt, {fehler} fehlgeschlagen.",
                            color="warning",
                        )
                    exemplare_laden(isbn)

                ui.button("Exemplare hinzufügen", on_click=exemplar_hinzufuegen).classes(
                    "bg-blue-600 text-white mt-2"
                )


# ─────────────────────────────────────────────
#  Neues Buch hinzufügen
# ─────────────────────────────────────────────

def _buch_hinzufuegen():
    ui.label("➕ Neues Buch hinzufügen").classes("font-semibold mb-2")
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
        try:
            anzahl = int(anzahl_ex_in.value or 1)
            buch_service.buch_erstellen(
                titel=titel_in.value,
                autor=autor_in.value,
                isbn=isbn_text,
                jahr=jahr,
                exemplar_anzahl=anzahl,
            )
            ui.notify(
                f"✅ '{titel_in.value}' mit {anzahl} Exemplar(en) hinzugefügt.",
                color="positive",
            )
            titel_in.set_value("")
            autor_in.set_value("")
            isbn_in.set_value("")
            jahr_in.set_value(None)
            anzahl_ex_in.set_value(1)
        except ValueError as e:
            ui.notify(f"❌ {e}", color="negative")

    ui.button("Buch speichern", on_click=buch_hinzufuegen).classes("bg-blue-600 text-white mt-2")


# ─────────────────────────────────────────────
#  Buch löschen
# ─────────────────────────────────────────────

def _buch_loeschen():
    ui.label("🗑️ Buch löschen").classes("font-semibold mt-2")

    with ui.row().classes("gap-2"):
        isbn_loeschen  = ui.input("ISBN").classes("w-36")
        titel_loeschen = ui.input("Titel").classes("w-36")
        autor_loeschen = ui.input("Autor").classes("w-36")

    loeschen_container = ui.column().classes("w-full gap-2")

    def buecher_zum_loeschen_suchen():
        loeschen_container.clear()
        isbn  = isbn_loeschen.value.strip().lower()
        titel = titel_loeschen.value.strip().lower()
        autor = autor_loeschen.value.strip().lower()

        if not isbn and not titel and not autor:
            ui.notify("Bitte mindestens ein Suchfeld ausfüllen.", color="warning")
            return

        alle = buch_service.alle_buecher_laden()
        treffer = [
            b for b in alle
            if (not isbn  or isbn  in b["isbn"].lower())
            and (not titel or titel in b["titel"].lower())
            and (not autor or autor in b["autor"].lower())
        ]

        if not treffer:
            with loeschen_container:
                ui.label("Keine Bücher gefunden.").classes("text-gray-400")
            return

        with loeschen_container:
            for b in treffer:
                with ui.card().classes("w-full p-3"):
                    with ui.row().classes("justify-between items-center w-full"):
                        with ui.column():
                            ui.label(b["titel"]).classes("font-semibold")
                            ui.label(
                                f"{b['autor']} · {b['jahr']} · ISBN: {b['isbn']}"
                            ).classes("text-gray-500 text-sm")
                        ui.button(
                            "🗑️ Löschen",
                            on_click=lambda _, buch=b: buch_loeschen_bestaetigen(buch),
                        ).classes("bg-red-600 text-white text-xs")

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
            ui.label("Buch wirklich löschen?").classes("font-semibold")
            ui.label(
                f"'{buch['titel']}' von {buch['autor']} wird unwiderruflich gelöscht."
            ).classes("text-gray-500")
            with ui.row().classes("gap-2 mt-2"):
                ui.button("Ja, löschen", on_click=bestaetigen).classes("bg-red-600 text-white")
                ui.button("Abbrechen", on_click=dialog.close).props("outline")
        dialog.open()

    with ui.row().classes("gap-2"):
        ui.button("Suchen", on_click=buecher_zum_loeschen_suchen).classes("bg-blue-600 text-white")
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
    ui.label("✏️ Buch bearbeiten").classes("font-semibold mt-2")

    with ui.row().classes("gap-2"):
        isbn_bearb_such  = ui.input("ISBN").classes("w-36")
        titel_bearb_such = ui.input("Titel").classes("w-36")
        autor_bearb_such = ui.input("Autor").classes("w-36")

    bearb_container = ui.column().classes("w-full gap-2")

    def buecher_zum_bearbeiten_suchen():
        bearb_container.clear()
        isbn  = isbn_bearb_such.value.strip().lower()
        titel = titel_bearb_such.value.strip().lower()
        autor = autor_bearb_such.value.strip().lower()

        if not isbn and not titel and not autor:
            ui.notify("Bitte mindestens ein Suchfeld ausfüllen.", color="warning")
            return

        alle = buch_service.alle_buecher_laden()
        treffer = [
            b for b in alle
            if (not isbn  or isbn  in b["isbn"].lower())
            and (not titel or titel in b["titel"].lower())
            and (not autor or autor in b["autor"].lower())
        ]

        if not treffer:
            with bearb_container:
                ui.label("Keine Bücher gefunden.").classes("text-gray-400")
            return

        with bearb_container:
            for b in treffer:
                with ui.card().classes("w-full p-3"):
                    ui.label(
                        f"{b['titel']} — {b['autor']} · {b['jahr']}"
                    ).classes("font-semibold")
                    ui.label(f"ISBN: {b['isbn']}").classes("text-gray-400 text-xs")

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
                        try:
                            ok = buch_service.buch_bearbeiten(
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
                        except ValueError as e:
                            ui.notify(f"❌ {e}", color="negative")
                        except Exception:
                            ui.notify("❌ Fehler beim Speichern.", color="negative")

                    ui.button("💾 Speichern", on_click=speichern).classes(
                        "bg-blue-600 text-white mt-2"
                    )

    with ui.row().classes("gap-2"):
        ui.button("Suchen", on_click=buecher_zum_bearbeiten_suchen).classes("bg-blue-600 text-white")
        ui.button(
            "Zurücksetzen",
            on_click=lambda: (
                isbn_bearb_such.set_value(""),
                titel_bearb_such.set_value(""),
                autor_bearb_such.set_value(""),
                bearb_container.clear(),
            ),
        ).props("outline")