import bcrypt

from Backend.modelle.benutzer import User, Administrator


def _ist_gehasht(gespeichert: str) -> bool:
    return bool(gespeichert) and gespeichert.startswith(("$2a$", "$2b$", "$2y$"))


def _passwort_hashen(klartext: str) -> str:
    return bcrypt.hashpw(klartext.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _passwort_pruefen(klartext: str, gespeichert: str) -> bool:
    try:
        return bcrypt.checkpw(klartext.encode("utf-8"), gespeichert.encode("utf-8"))
    except (ValueError, TypeError):
        return False


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

        passwort_hash = _passwort_hashen(passwort.strip())
        erfolg = self.db.benutzer_speichern(
            benutzername=benutzername.strip(),
            passwort=passwort_hash,
            vorname=vorname.strip(),
            nachname=nachname.strip(),
            email=email.strip(),
            rolle=rolle
        )

        if not erfolg:
            raise ValueError("Benutzer konnte nicht gespeichert werden.")

        return True

    def _benutzer_aus_daten(self, daten: dict) -> User:
        """Erzeugt User/Admin ohne Klartext-Passwort im Objekt."""
        kwargs = {
            "benutzername": daten["benutzername"],
            "vorname": daten["vorname"],
            "nachname": daten["nachname"],
            "email": daten["email"],
        }
        if daten["rolle"] in ["Admin", "Administrator"]:
            return Administrator(**kwargs)
        return User(**kwargs, rolle=daten["rolle"])

    def benutzer_laden(self, benutzername: str) -> User:
        """Laedt einen Benutzer und liefert je nach Rolle User oder Administrator."""
        daten = self.db.benutzer_laden(benutzername)
        if not daten:
            raise ValueError("Benutzer nicht gefunden.")
        return self._benutzer_aus_daten(daten)

    def login(self, benutzername: str, passwort: str) -> User:
        """Fuehrt den Login durch und gibt das passende Benutzerobjekt zurueck."""
        daten = self.db.benutzer_laden(benutzername)
        if not daten:
            raise ValueError("Benutzername oder Passwort ist falsch.")

        gespeichert = daten["passwort"]
        if _ist_gehasht(gespeichert):
            ok = _passwort_pruefen(passwort, gespeichert)
        else:
            # Legacy-Klartext (sollte nach Migration nicht mehr vorkommen)
            ok = gespeichert == passwort

        if not ok:
            raise ValueError("Benutzername oder Passwort ist falsch.")

        return self._benutzer_aus_daten(daten)

    def alle_benutzer(self) -> list[User]:
        """Liefert alle Benutzer aus der DB inkl. korrekter Rollentypen."""
        return [self._benutzer_aus_daten(d) for d in self.db.alle_benutzer_laden()]

    def ist_admin(self, benutzername: str) -> bool:
        """Prueft, ob ein Benutzer die Rolle Admin/Administrator besitzt."""
        daten = self.db.benutzer_laden(benutzername)
        if not daten:
            raise ValueError("Benutzer nicht gefunden.")
        return daten["rolle"] in ["Admin", "Administrator"]
