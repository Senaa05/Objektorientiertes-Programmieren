from datetime import date

class Ausleihe:
    def __init__(
        self,
        ausleih_id: str,
        benutzername: str,
        exemplar_id: str,
        ausleihdatum: str,
        faelligkeit: str,
        verlaengerungsanzahl: int = 0,
        rueckgabedatum: str = None
    ):
        self.ausleih_id = ausleih_id
        self.benutzername = benutzername
        self.exemplar_id = exemplar_id
        self.ausleihdatum = ausleihdatum
        self.faelligkeit = faelligkeit
        self.verlaengerungsanzahl = verlaengerungsanzahl
        self.rueckgabedatum = rueckgabedatum

    def ist_zurueckgegeben(self) -> bool:
        return self.rueckgabedatum is not None

    def ist_verlaengerbar(self) -> bool:
        # Eine Ausleihe darf nur einmal und nur vor Rueckgabe verlaengert werden.
        return not self.ist_zurueckgegeben() and self.verlaengerungsanzahl < 1

    def ist_ueberfaellig(self) -> bool:
        # Rueckgegebene Ausleihen gelten nicht als ueberfaellig.
        if self.ist_zurueckgegeben():
            return False
        return date.today() > date.fromisoformat(self.faelligkeit)

    def resttage(self) -> int:
        return (date.fromisoformat(self.faelligkeit) - date.today()).days

    def als_dict(self) -> dict:
        return {
            "ausleih_id": self.ausleih_id,
            "benutzername": self.benutzername,
            "exemplar_id": self.exemplar_id,
            "ausleihdatum": self.ausleihdatum,
            "faelligkeit": self.faelligkeit,
            "verlaengerungsanzahl": self.verlaengerungsanzahl,
            "rueckgabedatum": self.rueckgabedatum
        }