"""
Gemeinsamer Demo-Buchkatalog für Seed (DB) und Cover-Anzeige (UI).

ohne_cover=True → UI zeigt farbigen Platzhalter statt Open-Library-Request.
"""

from typing import NamedTuple


class DemoBuch(NamedTuple):
    titel: str
    autor: str
    isbn: str
    jahr: int
    exemplar_anzahl: int
    ohne_cover: bool = False


DEMO_BUECHER: tuple[DemoBuch, ...] = (
    DemoBuch("1984", "George Orwell", "9783548234106", 1949, 3),
    DemoBuch("Das Parfum", "Patrick Süskind", "9783257228007", 1985, 2),
    DemoBuch("Der kleine Prinz", "Antoine de Saint-Exupéry", "9783257068290", 1943, 3),
    DemoBuch(
        "Harry Potter und der Stein der Weisen",
        "J.K. Rowling",
        "9783551354013",
        1997,
        3,
    ),
    DemoBuch("Der Herr der Ringe", "J.R.R. Tolkien", "9783608938289", 1954, 4),
    DemoBuch("Der Hobbit", "J.R.R. Tolkien", "9780547928227", 1937, 2),
    DemoBuch("BECOMING: Meine Geschichte", "Michelle Obama", "9783442314874", 2018, 2),
    DemoBuch("Der Vorleser", "Bernhard Schlink", "9783257229707", 1995, 2),
    DemoBuch("Die Bücherdiebin", "Markus Zusak", "9780375831003", 2005, 2),
    DemoBuch("Der Name der Rose", "Umberto Eco", "9780151446476", 1980, 2),
    DemoBuch(
        "Die Tribute von Panem - Tödliche Spiele",
        "Suzanne Collins",
        "9780545425117",
        2008,
        3,
    ),
    DemoBuch("Eragon - Das Erbe der Macht", "Christopher Paolini", "9780375826689", 2002, 2),
    DemoBuch("Schöne neue Welt", "Aldous Huxley", "9783596209215", 1932, 3, ohne_cover=True),
    DemoBuch("Der Prozess", "Franz Kafka", "9783518369007", 1925, 3, ohne_cover=True),
    DemoBuch("Also sprach Zarathustra", "Friedrich Nietzsche", "9783150071115", 1884, 2, ohne_cover=True),
    DemoBuch("Der Alchimist", "Paulo Coelho", "9783257230600", 1988, 2, ohne_cover=True),
    DemoBuch("Ich bin Malala", "Malala Yousafzai", "9783596195962", 2013, 2, ohne_cover=True),
)

DEMO_ISBN_OHNE_COVER = frozenset(b.isbn for b in DEMO_BUECHER if b.ohne_cover)
