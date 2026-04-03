# Klasse für Bibliothek Standardbenutzer
class User:
    def __init__(self, benutzername, passwort, vorname, nachname, email):
        self.benutzername = benutzername
        self.passwort = passwort
        self.vorname = vorname
        self.nachname = nachname
        self.email = email
        # Rolle Standardbenutzer zuweisen
        self.rolle = "Benutzer"

# Klasse für Administratoren
class Administrator(User):
    def __init__(self, benutzername, passwort, vorname, nachname, email):
        # Vererbung von User-Klasse
        super().__init__(benutzername, passwort, vorname, nachname, email)
        # Rolle Admin zuweisen
        self.rolle = "Admin"