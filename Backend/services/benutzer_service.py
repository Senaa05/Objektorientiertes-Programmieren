from Backend.modelle.benutzer import User, Administrator


class BenutzerService:
    """Service fuer Registrierung, Login und Rollenpruefung von Benutzern."""

    def __init__(self, db):
        self.db = db

    def benutzer_registrieren(
        self,
        benutzername: str,
        passwort: str,
        vorname: str,
        nachname: str,
        email: str,
        rolle: str = "Benutzer"
    ) -> bool:
        """Registriert einen neuen Benutzer nach Pflichtfeld- und Eindeutigkeitspruefung."""
        # Grundvalidierung fuer Pflichtfelder bei der Registrierung.
        if not benutzername or not benutzername.strip():
            raise ValueError("Benutzername darf nicht leer sein.")

        if not passwort or not passwort.strip():
            raise ValueError("Passwort darf nicht leer sein.")

        if not vorname or not vorname.strip():
            raise ValueError("Vorname darf nicht leer sein.")

        if not nachname or not nachname.strip():
            raise ValueError("Nachname darf nicht leer sein.")

        if not email or not email.strip():
            raise ValueError("E-Mail darf nicht leer sein.")

        bestehender_benutzer = self.db.benutzer_laden(benutzername.strip())
        if bestehender_benutzer:
            raise ValueError("Benutzername existiert bereits.")

        bestehende_email = self.db.benutzer_mit_email_laden(email.strip())
        if bestehende_email:
            raise ValueError("E-Mail existiert bereits.")

        # Neue Benutzer werden direkt mit definierter Rolle gespeichert.
        erfolg = self.db.benutzer_speichern(
            benutzername=benutzername.strip(),
            passwort=passwort.strip(),
            vorname=vorname.strip(),
            nachname=nachname.strip(),
            email=email.strip(),
            rolle=rolle
        )

        if not erfolg:
            raise ValueError("Benutzer konnte nicht gespeichert werden.")

        return True

    def benutzer_laden(self, benutzername: str) -> User:
        """Laedt einen Benutzer und liefert je nach Rolle User oder Administrator."""
        daten = self.db.benutzer_laden(benutzername)
        if not daten:
            raise ValueError("Benutzer nicht gefunden.")

        if daten["rolle"] in ["Admin", "Administrator"]:
            return Administrator(
                benutzername=daten["benutzername"],
                passwort=daten["passwort"],
                vorname=daten["vorname"],
                nachname=daten["nachname"],
                email=daten["email"]
            )

        return User(**daten)

    def login(self, benutzername: str, passwort: str) -> User:
        """Fuehrt den Login durch und gibt das passende Benutzerobjekt zurueck."""
        # Aus Sicherheitsgruenden gleiche Fehlermeldung fuer Nutzer/Passwort.
        daten = self.db.benutzer_laden(benutzername)
        if not daten:
            raise ValueError("Benutzername oder Passwort ist falsch.")

        if daten["passwort"] != passwort:
            raise ValueError("Benutzername oder Passwort ist falsch.")

        if daten["rolle"] in ["Admin", "Administrator"]:
            return Administrator(
                benutzername=daten["benutzername"],
                passwort=daten["passwort"],
                vorname=daten["vorname"],
                nachname=daten["nachname"],
                email=daten["email"]
            )

        return User(**daten)

    def alle_benutzer(self) -> list[User]:
        """Liefert alle Benutzer aus der DB inkl. korrekter Rollentypen."""
        daten_liste = self.db.alle_benutzer_laden()
        benutzer_liste = []

        for daten in daten_liste:
            if daten["rolle"] in ["Admin", "Administrator"]:
                benutzer_liste.append(
                    Administrator(
                        benutzername=daten["benutzername"],
                        passwort=daten["passwort"],
                        vorname=daten["vorname"],
                        nachname=daten["nachname"],
                        email=daten["email"]
                    )
                )
            else:
                benutzer_liste.append(User(**daten))

        return benutzer_liste

    def ist_admin(self, benutzername: str) -> bool:
        """Prueft, ob ein Benutzer die Rolle Admin/Administrator besitzt."""
        daten = self.db.benutzer_laden(benutzername)
        if not daten:
            raise ValueError("Benutzer nicht gefunden.")

        return daten["rolle"] in ["Admin", "Administrator"]