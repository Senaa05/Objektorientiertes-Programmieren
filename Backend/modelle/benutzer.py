class User:
    def __init__(
        self,
        benutzername: str,
        vorname: str,
        nachname: str,
        email: str,
        rolle: str = "Benutzer",
        passwort: str = "",
    ):
        self.benutzername = benutzername
        self.vorname = vorname
        self.nachname = nachname
        self.email = email
        self.rolle = rolle
        # Passwort wird nicht nach außen gegeben (nur intern/leer)
        self._passwort = passwort

    def ist_admin(self) -> bool:
        return self.rolle in ["Admin", "Administrator"]

    def als_dict(self) -> dict:
        return {
            "benutzername": self.benutzername,
            "vorname": self.vorname,
            "nachname": self.nachname,
            "email": self.email,
            "rolle": self.rolle,
        }


class Administrator(User):
    def __init__(self, benutzername, vorname, nachname, email, passwort: str = ""):
        super().__init__(
            benutzername, vorname, nachname, email, rolle="Admin", passwort=passwort
        )
