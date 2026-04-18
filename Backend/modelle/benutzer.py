class User:
    def __init__(
        self,
        benutzername: str,
        passwort: str,
        vorname: str,
        nachname: str,
        email: str,
        rolle: str = "Benutzer"
    ):
        self.benutzername = benutzername
        self.passwort = passwort
        self.vorname = vorname
        self.nachname = nachname
        self.email = email
        self.rolle = rolle

    def ist_admin(self) -> bool:
        # Erlaubt die Rollenbezeichnung "Admin" und "Administrator".
        return self.rolle in ["Admin", "Administrator"]

    def als_dict(self) -> dict:
        return {
            "benutzername": self.benutzername,
            "passwort": self.passwort,
            "vorname": self.vorname,
            "nachname": self.nachname,
            "email": self.email,
            "rolle": self.rolle
        }


class Administrator(User):
    def __init__(self, benutzername, passwort, vorname, nachname, email):
        # Admin ist eine Spezialisierung von User mit fixer Rolle.
        super().__init__(benutzername, passwort, vorname, nachname, email, rolle="Admin")