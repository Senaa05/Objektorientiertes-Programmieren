"""
Demo-Bestand für Bibflow (wird ins Repo committed, nicht die .db-Datei).
Beim App-Start werden Bücher und Demo-Ausleihen angelegt, sofern sie noch fehlen.

Cover-Hinweis: Bücher mit ✓ haben bei Open Library ein Cover zur ISBN.
Bücher mit ○ zeigen in der UI den farbigen Platzhalter mit Buchtitel.
"""

from datetime import date, timedelta

# titel, autor, isbn (13-stellig), jahr, exemplar_anzahl
DEMO_BUECHER = [
    # ── Mit Cover (Open Library) ──
    ("1984", "George Orwell", "9783548234106", 1949, 3),  # ✓
    ("Das Parfum", "Patrick Süskind", "9783257228007", 1985, 2),  # ✓
    ("Der kleine Prinz", "Antoine de Saint-Exupéry", "9783257068290", 1943, 3),  # ✓
    (
        "Harry Potter und der Stein der Weisen",
        "J.K. Rowling",
        "9783551354013",
        1997,
        3,
    ),  # ✓
    ("Der Herr der Ringe", "J.R.R. Tolkien", "9783608938289", 1954, 4),  # ✓
    ("Der Hobbit", "J.R.R. Tolkien", "9780547928227", 1937, 2),  # ✓
    ("BECOMING: Meine Geschichte", "Michelle Obama", "9783442314874", 2018, 2),  # ✓
    ("Der Vorleser", "Bernhard Schlink", "9783257229707", 1995, 2),  # ✓
    ("Die Bücherdiebin", "Markus Zusak", "9780375831003", 2005, 2),  # ✓
    ("Der Name der Rose", "Umberto Eco", "9780151446476", 1980, 2),  # ✓
    (
        "Die Tribute von Panem - Tödliche Spiele",
        "Suzanne Collins",
        "9780545425117",
        2008,
        3,
    ),  # ✓
    ("Eragon - Das Erbe der Macht", "Christopher Paolini", "9780375826689", 2002, 2),  # ✓
    # ── Ohne Cover (Platzhalter mit Titel) ──
    ("Schöne neue Welt", "Aldous Huxley", "9783596209215", 1932, 3),  # ○
    ("Der Prozess", "Franz Kafka", "9783518369007", 1925, 3),  # ○
    ("Also sprach Zarathustra", "Friedrich Nietzsche", "9783150071115", 1884, 2),  # ○
    ("Der Alchimist", "Paulo Coelho", "9783257230600", 1988, 2),  # ○
    ("Ich bin Malala", "Malala Yousafzai", "9783596195962", 2013, 2),  # ○
]

# Nur Ziffern — für UI-Platzhalter (kein Cover-Bild laden)
DEMO_ISBN_OHNE_COVER = {
    "9783596209215",
    "9783518369007",
    "9783150071115",
    "9783257230600",
    "9783596195962",
}

# Alte Demo-ISBNs → korrigierte ISBN (für bestehende bibliothek_orm.db beim App-Start)
ISBN_KORREKTUR = {
    "9783548234105": "9783548234106",
    "9783150197066": "9783150190494",
    "9781524763145": "9783442314874",
    "9783123456789": "9783257230600",
    "9783608938315": "9783608938289",
    "9783987654321": "9783518181241",
    "9783551551678": "9783551354013",
    "9783314103407": "9783257241804",
    "9783789142185": "9780545425117",
    "9783789132186": "9780545425117",
}

# Demo-Ausleihen: benutzername, isbn-Kandidaten, ausleih_id, tage_seit_ausleihe, tage_bis_faelligkeit
# tage_bis_faelligkeit < 0  → überfällig (Popup popup_ueberfaellige_fuer_benutzer)
# 0 .. 7 → bald fällig (Reminder-Popup)
DEMO_AUSLEIHEN = [
    ("demo", ["9783548234106", "9783548234105", "978-3-548-23410-6"], "DEMO-AUS-UEBERFAELLIG", 50, -14),
    ("demo", ["9783551354013", "9783551551678", "978-3-551-35401-3"], "DEMO-AUS-REMINDER", 23, 5),
]


def _finde_verfuegbares_exemplar(db, isbn_kandidaten: list[str], bereits_belegt: set[str]):
    """Sucht ein freies Exemplar (Seed-ISBN oder erstes freies Buch in der DB)."""
    for isbn in isbn_kandidaten:
        for exemplar in db.verfuegbare_exemplare(isbn):
            eid = exemplar["exemplar_id"]
            if eid not in bereits_belegt:
                return isbn, eid

    for buch in db.alle_buecher_laden():
        for exemplar in db.verfuegbare_exemplare(buch["isbn"]):
            eid = exemplar["exemplar_id"]
            if eid not in bereits_belegt:
                return buch["isbn"], eid
    return None, None


def korrigiere_demo_isbns(db) -> int:
    """Passt falsche Demo-ISBNs in einer bestehenden DB an (Primary Key buecher.isbn)."""
    from Datenbank.orm_models import Buch, Exemplar, Merkliste

    geaendert = 0
    with db.get_session() as session:
        for alt, neu in ISBN_KORREKTUR.items():
            if session.query(Buch).filter(Buch.isbn == neu).first():
                continue
            buch = session.query(Buch).filter(Buch.isbn == alt).first()
            if not buch:
                continue
            session.query(Exemplar).filter(Exemplar.isbn == alt).update(
                {Exemplar.isbn: neu}, synchronize_session=False
            )
            session.query(Merkliste).filter(Merkliste.isbn == alt).update(
                {Merkliste.isbn: neu}, synchronize_session=False
            )
            buch.isbn = neu
            geaendert += 1
        if geaendert:
            session.commit()
    return geaendert


def seed_demo_buecher(buch_service) -> int:
    """Legt Demo-Bücher an, wenn die Datenbank noch leer ist. Gibt Anzahl angelegter Bücher zurück."""
    if buch_service.alle_buecher():
        return 0

    angelegt = 0
    for titel, autor, isbn, jahr, exemplar_anzahl in DEMO_BUECHER:
        try:
            buch_service.buch_erstellen(
                titel=titel,
                autor=autor,
                isbn=isbn,
                jahr=jahr,
                exemplar_anzahl=exemplar_anzahl,
            )
            angelegt += 1
        except ValueError:
            pass
    return angelegt


def seed_demo_ausleihen(db) -> int:
    """
    Legt Demo-Ausleihen an (überfällig + bald fällig für Benutzer demo).
    Idempotent über feste ausleih_id. Für popup_ueberfaellige_fuer_benutzer / Reminder.
    """
    if db.ausleih_laden("DEMO-AUS-UEBERFAELLIG"):
        return 0

    heute = date.today()
    angelegt = 0
    bereits_belegt: set[str] = set()

    for (
        benutzername,
        isbn_kandidaten,
        ausleih_id,
        tage_seit_ausleihe,
        tage_bis_faelligkeit,
    ) in DEMO_AUSLEIHEN:
        if not db.benutzer_laden(benutzername):
            continue

        _isbn, exemplar_id = _finde_verfuegbares_exemplar(db, isbn_kandidaten, bereits_belegt)
        if not exemplar_id:
            continue
        bereits_belegt.add(exemplar_id)
        ausleihdatum = heute - timedelta(days=tage_seit_ausleihe)
        faelligkeit = heute + timedelta(days=tage_bis_faelligkeit)

        if not db.ausleih_speichern(
            ausleih_id=ausleih_id,
            benutzername=benutzername,
            exemplar_id=exemplar_id,
            ausleihdatum=ausleihdatum.strftime("%Y-%m-%d"),
            faelligkeit=faelligkeit.strftime("%Y-%m-%d"),
        ):
            continue

        if db.exemplar_status_aktualisieren(exemplar_id, "ausgeliehen"):
            angelegt += 1

    return angelegt
