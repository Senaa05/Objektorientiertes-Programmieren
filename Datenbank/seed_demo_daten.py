"""
Demo-Bestand für Bibflow (wird ins Repo committed, nicht die .db-Datei).
Beim ersten Start wird dieser Katalog angelegt, wenn die DB noch keine Bücher hat.
"""

# titel, autor, isbn (mind. 13 Ziffern), jahr, exemplar_anzahl
DEMO_BUECHER = [
    ("1984", "George Orwell", "9783548234105", 1949, 3),
    ("Also sprach Zarathustra", "Friedrich Nietzsche", "9783150071115", 1884, 2),
    ("Angst", "Stefan Zweig", "9783150197066", 1925, 1),
    ("BECOMING: Meine Geschichte", "Michelle Obama", "9781524763145", 2021, 2),
    ("Das Parfum", "Patrick Süskind", "9783257228007", 1985, 2),
    ("Der Alchimist", "Paulo Coelho", "9783123456789", 1988, 2),
    ("Der Herr der Ringe", "J.R.R. Tolkien", "9783608938315", 1954, 4),
    ("Der Prozess", "Franz Kafka", "9783518369007", 1925, 3),
    ("Der Sandmann", "E.T.A Hoffmann", "9783150002308", 1986, 2),
    ("Der kleine Prinz", "Antoine de Saint-Exupéry", "9783257068290", 1943, 3),
    ("Die Verwandlung", "Franz Kafka", "9783987654321", 1915, 1),
    ("Eine kurze Geschichte der Zeit", "Stephen Hawking", "9783499621567", 1988, 2),
    ("Harry Potter und der Stein der Weisen", "J.K. Rowling", "9783551551678", 1997, 3),
    ("Heidi", "Johanna Spyri", "9783314103407", 2015, 2),
    ("Ich bin Malala", "Malala Yousafzai", "9783596195962", 2013, 3),
    ("Schöne neue Welt", "Aldous Huxley", "9783596209215", 1932, 3),
    ("Tribute von Panem - Tödliche Spiele", "Suzanne Collins", "9783789142185", 2008, 3),
    ("Twilight – Biss zum Morgengrauen", "Stephenie Meyer", "9783551580016", 2005, 2),
]


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
