"""
login.py - Login- und Registrierungsseite
=========================================
"""

from nicegui import ui
from Frontend.state import zustand, benutzer_service


def zeige_login():
    ui.query("body").style("background: #f0f4f8")

    with ui.card().classes("absolute-center w-96 p-8"):
        ui.label("Willkommen bei Bibflow").classes(
            "text-2xl font-bold mb-6 text-center w-full"
        )

        # ── Tab-Buttons ──
        with ui.row().classes("w-full mb-4 overflow-hidden rounded border border-gray-300"):
            login_btn = ui.button("Login", on_click=lambda: zeige_tab("login")).classes(
                "flex-1 rounded-none bg-blue-600 text-white"
            )
            reg_btn = ui.button("Registrieren", on_click=lambda: zeige_tab("register")).classes(
                "flex-1 rounded-none text-blue-600"
            ).props("outline")

        fehler_label = ui.label("").classes("text-red-500 text-sm")

        # ── LOGIN FELDER ──
        login_panel = ui.column().classes("w-full gap-2")
        with login_panel:
            bn_input = ui.input(placeholder="Benutzername").classes("w-full")
            pw_input = ui.input(placeholder="Passwort", password=True).classes("w-full")
            pw_input.props("type=password")

            def toggle_passwort():
                if pw_input.props.get("type") == "password":
                    pw_input.props("type=text")
                    auge_btn.props("icon=visibility_off")
                else:
                    pw_input.props("type=password")
                    auge_btn.props("icon=visibility")

            with pw_input.add_slot("append"):
                auge_btn = ui.icon("visibility").on("click", toggle_passwort).classes("cursor-pointer")

            def anmelden():
                bn = bn_input.value.strip()
                pw = pw_input.value
                try:
                    benutzer = benutzer_service.login(bn, pw)
                except ValueError:
                    fehler_label.set_text("Benutzername oder Passwort ist falsch.")
                    return
                zustand["angemeldet"]   = True
                zustand["benutzername"] = bn
                zustand["rolle"]        = benutzer.rolle
                ui.navigate.to("/dashboard")

            ui.button("Login", on_click=anmelden).classes(
                "w-full bg-blue-600 text-white mt-2"
            )

        # ── REGISTRIEREN FELDER ──
        reg_panel = ui.column().classes("w-full gap-2").style("display:none")
        with reg_panel:
            vorname_in  = ui.input(placeholder="Vorname").classes("w-full")
            nachname_in = ui.input(placeholder="Nachname").classes("w-full")
            email_in    = ui.input(placeholder="Email").classes("w-full")
            reg_bn_in   = ui.input(placeholder="Benutzername").classes("w-full")
            reg_pw_in   = ui.input(placeholder="Passwort", password=True).classes("w-full")
            reg_pw_in.props("type=password")

            def toggle_reg_passwort():
                if reg_pw_in.props.get("type") == "password":
                    reg_pw_in.props("type=text")
                    reg_auge_btn.props("icon=visibility_off")
                else:
                    reg_pw_in.props("type=password")
                    reg_auge_btn.props("icon=visibility")

            with reg_pw_in.add_slot("append"):
                reg_auge_btn = ui.icon("visibility").on("click", toggle_reg_passwort).classes("cursor-pointer")

            def registrieren():
                if not all([vorname_in.value, nachname_in.value, email_in.value,
                            reg_bn_in.value, reg_pw_in.value]):
                    fehler_label.set_text("Bitte alle Felder ausfüllen.")
                    return
                try:
                    benutzer_service.benutzer_registrieren(
                        benutzername=reg_bn_in.value,
                        passwort=reg_pw_in.value,
                        vorname=vorname_in.value,
                        nachname=nachname_in.value,
                        email=email_in.value,
                    )
                    ui.notify("✅ Registrierung erfolgreich! Bitte einloggen.", color="positive")
                    zeige_tab("login")
                except ValueError as e:
                    fehler_label.set_text(str(e))
                except Exception:
                    fehler_label.set_text("Fehler beim Speichern des Benutzers.")

            ui.button("Registrieren", on_click=registrieren).classes(
                "w-full bg-blue-600 text-white mt-2"
            )

        # ── Tab-Wechsel Logik ──
        def zeige_tab(tab: str):
            fehler_label.set_text("")
            if tab == "login":
                login_panel.style("display:block")
                reg_panel.style("display:none")
                login_btn.classes(remove="text-blue-600").classes(add="bg-blue-600 text-white")
                login_btn.props(remove="outline")
                reg_btn.classes(remove="bg-blue-600 text-white").classes(add="text-blue-600")
                reg_btn.props(add="outline")
            else:
                login_panel.style("display:none")
                reg_panel.style("display:block")
                login_btn.classes(remove="bg-blue-600 text-white").classes(add="text-blue-600")
                login_btn.props(add="outline")
                reg_btn.classes(remove="text-blue-600").classes(add="bg-blue-600 text-white")
                reg_btn.props(remove="outline")