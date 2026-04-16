from modelle.ausleihe import Ausleihe

class AusleiheService:
    def ausleihen(self, user, buch):
        # 1. Prüfen: maximal 5 aktive Ausleihen
        aktive_ausleihen = [a for a in user.ausleihen if a.rueckgabedatum is None]
        if len(aktive_ausleihen) >= 5:
            raise ValueError("Benutzer darf maximal 5 Bücher gleichzeitig ausleihen.")

        # 2. Prüfen: gleiches Buch nicht doppelt ausleihen
        for ausleihe in aktive_ausleihen:
            if ausleihe.exemplar.buch == buch:
                raise ValueError("Dieses Buch wurde bereits ausgeliehen.")

        # 3. Verfügbares Exemplar suchen
        verfuegbare = [e for e in buch.exemplare if e.status == "verfuegbar"]
        if not verfuegbare:
            raise ValueError("Kein verfügbares Exemplar vorhanden.")

        exemplar = verfuegbare[0]

        # 4. Exemplar ausleihen
        exemplar.ausleihen()

        # 5. Ausleihe erstellen
        ausleihe = Ausleihe(user, exemplar)

        # 6. Beim User speichern
        user.ausleihen.append(ausleihe)

        return ausleihe
    
