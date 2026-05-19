"""
Einmalige Migration von bibliothek.db nach bibliothek_orm.db.
Kopiert alle Tabellen inkl. der 4 Benutzer und bestehender Ausleihen.
"""

import os
import sqlite3
from datetime import date

from orm_models import init_database, create_tables, get_session
from orm_models import Buch, Exemplar, Benutzer, Ausleihe, Merkliste


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def migrate(legacy_path: str, orm_path: str) -> None:
    if not os.path.isfile(legacy_path):
        raise FileNotFoundError(f"Legacy-Datenbank nicht gefunden: {legacy_path}")

    if os.path.isfile(orm_path):
        os.remove(orm_path)

    init_database(orm_path)
    create_tables()

    legacy = sqlite3.connect(legacy_path)
    legacy.row_factory = sqlite3.Row

    with get_session() as session:
        for row in legacy.execute("SELECT * FROM buecher"):
            session.add(Buch(
                isbn=row["isbn"],
                titel=row["titel"],
                autor=row["autor"],
                jahr=row["jahr"],
            ))

        for row in legacy.execute("SELECT * FROM benutzer"):
            session.add(Benutzer(
                benutzername=row["benutzername"],
                passwort=row["passwort"],
                vorname=row["vorname"],
                nachname=row["nachname"],
                email=row["email"],
                rolle=row["rolle"],
            ))

        for row in legacy.execute("SELECT * FROM exemplare"):
            session.add(Exemplar(
                exemplar_id=row["exemplar_id"],
                isbn=row["isbn"],
                status=row["status"],
            ))

        for row in legacy.execute("SELECT * FROM ausleihen"):
            session.add(Ausleihe(
                ausleih_id=row["ausleih_id"],
                benutzername=row["benutzername"],
                exemplar_id=row["exemplar_id"],
                ausleihdatum=_parse_date(row["ausleihdatum"]),
                faelligkeit=_parse_date(row["faelligkeit"]),
                rueckgabedatum=_parse_date(row["rueckgabedatum"]),
                verlaengerungsanzahl=row["verlaengerungsanzahl"] or 0,
            ))

        for row in legacy.execute("SELECT * FROM merkliste"):
            session.add(Merkliste(
                benutzername=row["benutzername"],
                isbn=row["isbn"],
                hinzugefuegt_am=_parse_date(row["hinzugefuegt_am"]) or date.today(),
            ))

        session.commit()

    legacy.close()

    verify = sqlite3.connect(orm_path)
    benutzer = verify.execute("SELECT COUNT(*) FROM benutzer").fetchone()[0]
    buecher = verify.execute("SELECT COUNT(*) FROM buecher").fetchone()[0]
    verify.close()

    print(f"Migration abgeschlossen: {orm_path}")
    print(f"  Benutzer: {benutzer}, Bücher: {buecher}")


if __name__ == "__main__":
    basis = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    legacy = os.path.join(basis, "Backend", "bibliothek.db")
    ziel = os.path.join(basis, "bibliothek_orm.db")
    migrate(legacy, ziel)
