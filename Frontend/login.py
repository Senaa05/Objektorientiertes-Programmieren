"""
login.py - Login- und Registrierungsseite
=========================================
"""
 
from nicegui import ui
from state import zustand, benutzer_service
 
 
def zeige_login():
    ui.query("body").style("background: #f0f4f8")
 
    with ui.card().classes("absolute-center").style("width:400px; padding:2rem"):
        ui.label("Willkommen bei Bibflow").style(
            "font-size:1.6rem; font-weight:700; margin-bottom:1.5rem; text-align:center"
        )
 
        # ── Tab-Buttons ──
        with ui.row().classes("w-full mb-4").style(
            "border:1px solid #ddd; border-radius:6px; overflow:hidden"
        ):
            login_btn = ui.button("Login", on_click=lambda: zeige_tab("login")).style(
                "flex:1; border-radius:0; background:black; color:white"
            )
            reg_btn = ui.button("Registrieren", on_click=lambda: zeige_tab("register")).style(
                "flex:1; border-radius:0; background:white; color:black; border:none"
            )
 
        fehler_label = ui.label("").style("color:red; font-size:0.85rem")
 
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
                auge_btn = ui.icon("visibility").on("click", toggle_passwort).style("cursor:pointer")
 
            def anmelden():
                bn = bn_input.value.strip()
                pw = pw_input.value
                try:
                    benutzer = benutzer_service.login(bn, pw)
                except ValueError:
                    fehler_label.set_text("Benutzername oder Passwort ist falsch.")
                    return
                zustand["angemeldet"]    = True
                zustand["benutzername"]  = bn
                zustand["rolle"]         = benutzer.rolle
                ui.navigate.to("/dashboard")
 
            ui.button("Login", on_click=anmelden).classes("w-full").style(
                "background:black; color:white; margin-top:0.5rem"
            )
 
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
 
            ui.button("Registrieren", on_click=registrieren).classes("w-full").style(
                "background:black; color:white; margin-top:0.5rem"
            )
 
        # ── Tab-Wechsel Logik ──
        def zeige_tab(tab: str):
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