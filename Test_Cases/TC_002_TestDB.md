"""
TC_002 – ORMDatenbankManager CRUD-Operationen
==============================================
Testet alle CRUD-Funktionen des ORMDatenbankManagers (SQLAlchemy).

Voraussetzung:
  - SQLAlchemy ist installiert  (pip install sqlalchemy)
  - Diese Datei liegt im Projektordner (neben dem Ordner Datenbank/)
    ODER wird mit: python -m pytest TC_002_Datenbank_Test.py gestartet

Ausführen:
  python TC_002_Datenbank_Test.py
  python -m pytest TC_002_Datenbank_Test.py -v
"""

import unittest
import os
import sys
from datetime import date

# ─── Projektpfade einrichten ─────────────────────────────────────────────────
DIESES_VERZEICHNIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIESES_VERZEICHNIS)
sys.path.insert(0, os.path.join(DIESES_VERZEICHNIS, "Datenbank"))

# ─── orm_models live erzeugen (SQLite in-memory) ─────────────────────────────
# Damit der Test ohne externes orm_models.py läuft, definieren wir die
# SQLAlchemy-Modelle und Hilfsfunktionen direkt hier.
from sqlalchemy import (
    create_engine, Column, String, Integer, Date,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
import types

Base = declarative_base()
_engine = None
_SessionLocal = None

def init_database(db_path: str):
    global _engine, _SessionLocal
    url = f"sqlite:///{db_path}"
    _engine = create_engine(url, connect_args={"check_same_thread": False})
    _SessionLocal = sessionmaker(bind=_engine)

def create_tables():
    Base.metadata.create_all(_engine)

def get_session() -> Session:
    return _SessionLocal()

class Buch(Base):
    __tablename__ = "buecher"
    isbn   = Column(String, primary_key=True)
    titel  = Column(String, nullable=False)
    autor  = Column(String, nullable=False)
    jahr   = Column(Integer, nullable=False)
    exemplare = relationship("Exemplar", back_populates="buch", cascade="all, delete-orphan")
    merkliste = relationship("Merkliste", back_populates="buch", cascade="all, delete-orphan")

class Exemplar(Base):
    __tablename__ = "exemplare"
    exemplar_id = Column(String, primary_key=True)
    isbn        = Column(String, ForeignKey("buecher.isbn"), nullable=False)
    status      = Column(String, default="verfuegbar")
    buch        = relationship("Buch", back_populates="exemplare")
    ausleihen   = relationship("Ausleihe", back_populates="exemplar")

class Benutzer(Base):
    __tablename__ = "benutzer"
    benutzername = Column(String, primary_key=True)
    passwort     = Column(String, nullable=False)
    vorname      = Column(String, nullable=False)
    nachname     = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False)
    rolle        = Column(String, default="Benutzer")
    ausleihen    = relationship("Ausleihe", back_populates="benutzer")
    merkliste    = relationship("Merkliste", back_populates="benutzer")

class Ausleihe(Base):
    __tablename__ = "ausleihen"
    ausleih_id          = Column(String, primary_key=True)
    benutzername        = Column(String, ForeignKey("benutzer.benutzername"), nullable=False)
    exemplar_id         = Column(String, ForeignKey("exemplare.exemplar_id"), nullable=False)
    ausleihdatum        = Column(Date, nullable=False)
    faelligkeit         = Column(Date, nullable=False)
    rueckgabedatum      = Column(Date, nullable=True)
    verlaengerungsanzahl = Column(Integer, default=0)
    benutzer = relationship("Benutzer", back_populates="ausleihen")
    exemplar = relationship("Exemplar", back_populates="ausleihen")

class Merkliste(Base):
    __tablename__ = "merkliste"
    __table_args__ = (UniqueConstraint("benutzername", "isbn"),)
    id           = Column(Integer, primary_key=True, autoincrement=True)
    benutzername = Column(String, ForeignKey("benutzer.benutzername"), nullable=False)
    isbn         = Column(String, ForeignKey("buecher.isbn"), nullable=False)
    hinzugefuegt_am = Column(Date, default=date.today)
    benutzer = relationship("Benutzer", back_populates="merkliste")
    buch     = relationship("Buch",     back_populates="merkliste")

# orm_models als Modul ins sys.modules eintragen, damit orm_manager.py es findet
_orm_models = types.ModuleType("orm_models")
_orm_models.Buch       = Buch
_orm_models.Exemplar   = Exemplar
_orm_models.Benutzer   = Benutzer
_orm_models.Ausleihe   = Ausleihe
_orm_models.Merkliste  = Merkliste
_orm_models.get_session    = get_session
_orm_models.create_tables  = create_tables
_orm_models.init_database  = init_database
sys.modules["orm_models"] = _orm_models

from orm_manager import ORMDatenbankManager  # noqa: E402 – muss nach dem Stub stehen

# ─── Testdaten ────────────────────────────────────────────────────────────────
TEST_DB      = "test_bibliothek.db"

ISBN_1       = "978-3-000-00001-1"
TITEL_1      = "Python Grundlagen"
AUTOR_1      = "Max Mustermann"
JAHR_1       = 2022

ISBN_2       = "978-3-000-00002-2"
TITEL_2      = "OOP Prinzipien"
AUTOR_2      = "Erika Musterfrau"
JAHR_2       = 2020

EXEMPLAR_ID  = "EX-001"

BENUTZERNAME = "testuser1"
PASSWORT     = "passwort123"
VORNAME      = "Anna"
NACHNAME     = "Schmidt"
EMAIL        = "anna@test.de"
ROLLE        = "Benutzer"

AUSLEIH_ID_1   = "AUS-001"
AUSLEIHDATUM_1 = "2026-05-20"
FAELLIGKEIT_1  = "2026-06-03"

AUSLEIH_ID_2   = "AUS-002"
AUSLEIHDATUM_2 = "2026-01-01"
FAELLIGKEIT_2  = "2026-01-15"


# ─── Testklasse ──────────────────────────────────────────────────────────────
class TestORMDatenbankManager(unittest.TestCase):

    # ── Setup / Teardown ─────────────────────────────────────────────────────

    def setUp(self):
        """Frische Datenbank vor jedem Test."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        self.db = ORMDatenbankManager(TEST_DB)

    def tearDown(self):
        """Verbindung schließen und Datei aufräumen."""
        try:
            self.db.schliessen()
        except Exception:
            pass
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    # ── Hilfsmethoden ────────────────────────────────────────────────────────

    def _buch_und_exemplar(self):
        """Legt Buch + Exemplar an (Vorbedingung für viele Tests)."""
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)
        self.db.exemplar_speichern(EXEMPLAR_ID, ISBN_1)

    def _benutzer(self):
        """Legt Testbenutzer an."""
        self.db.benutzer_speichern(BENUTZERNAME, PASSWORT, VORNAME, NACHNAME, EMAIL, ROLLE)

    # ── 4.1  Verbindung & Tabellenerstellung ─────────────────────────────────

    def test_4_1_verbindung_und_tabellen(self):
        """ORMDatenbankManager initialisiert und legt alle 5 Tabellen an."""
        # ORMDatenbankManager nutzt Sessions statt einer rohen connection.
        # Wir prüfen, dass get_session() ohne Exception eine Session liefert.
        session = self.db.get_session()
        self.assertIsNotNone(session, "get_session() sollte eine Session zurückgeben.")
        session.close()

        # Alle 5 Tabellen prüfen
        from sqlalchemy import inspect
        inspektor = inspect(_engine)
        vorhandene = set(inspektor.get_table_names())
        for tabelle in ("buecher", "exemplare", "benutzer", "ausleihen", "merkliste"):
            self.assertIn(tabelle, vorhandene, f"Tabelle '{tabelle}' fehlt.")

    # ── 4.2  Buch speichern und laden ────────────────────────────────────────

    def test_4_2_buch_speichern_und_laden(self):
        result = self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)
        self.assertTrue(result, "buch_speichern() sollte True zurückgeben.")

        buch = self.db.buch_laden(ISBN_1)
        self.assertIsNotNone(buch, "buch_laden() sollte einen Datensatz liefern.")
        self.assertEqual(buch["titel"], TITEL_1)
        self.assertEqual(buch["autor"], AUTOR_1)
        self.assertEqual(buch["isbn"],  ISBN_1)
        self.assertEqual(buch["jahr"],  JAHR_1)

    # ── 4.3  Alle Bücher laden & Suche ───────────────────────────────────────

    def test_4_3_alle_buecher_und_suche(self):
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)
        self.db.buch_speichern(TITEL_2, AUTOR_2, ISBN_2, JAHR_2)

        alle = self.db.alle_buecher_laden()
        self.assertEqual(len(alle), 2, "Es sollten genau 2 Bücher vorhanden sein.")

        treffer_titel = self.db.bucher_suchen("Python")
        self.assertEqual(len(treffer_titel), 1, "Suche nach 'Python' sollte 1 Treffer liefern.")

        treffer_autor = self.db.bucher_suchen("Mustermann")
        self.assertEqual(len(treffer_autor), 1, "Suche nach 'Mustermann' sollte 1 Treffer liefern.")

    # ── 4.4  Buch bearbeiten ─────────────────────────────────────────────────

    def test_4_4_buch_bearbeiten(self):
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)

        result = self.db.buch_bearbeiten(ISBN_1, titel="Python Fortgeschritten")
        self.assertTrue(result, "buch_bearbeiten() sollte True zurückgeben.")

        buch = self.db.buch_laden(ISBN_1)
        self.assertEqual(buch["titel"], "Python Fortgeschritten",
                         "Titel sollte nach buch_bearbeiten() aktualisiert sein.")

    # ── 4.5  Exemplar speichern und Status aktualisieren ─────────────────────

    def test_4_5_exemplar_speichern_und_status(self):
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)

        result = self.db.exemplar_speichern(EXEMPLAR_ID, ISBN_1)
        self.assertTrue(result, "exemplar_speichern() sollte True zurückgeben.")

        verfuegbar = self.db.verfuegbare_exemplare(ISBN_1)
        self.assertEqual(len(verfuegbar), 1,
                         "Nach dem Speichern sollte 1 Exemplar verfügbar sein.")

        self.db.exemplar_status_aktualisieren(EXEMPLAR_ID, "ausgeliehen")
        verfuegbar_danach = self.db.verfuegbare_exemplare(ISBN_1)
        self.assertEqual(len(verfuegbar_danach), 0,
                         "Nach Statuswechsel auf 'ausgeliehen' sollten 0 Exemplare verfügbar sein.")

    # ── 4.6  Benutzer speichern und laden ────────────────────────────────────

    def test_4_6_benutzer_speichern_und_laden(self):
        result = self.db.benutzer_speichern(
            BENUTZERNAME, PASSWORT, VORNAME, NACHNAME, EMAIL, ROLLE
        )
        self.assertTrue(result, "benutzer_speichern() sollte True zurückgeben.")

        benutzer = self.db.benutzer_laden(BENUTZERNAME)
        self.assertIsNotNone(benutzer)
        self.assertEqual(benutzer["vorname"],  VORNAME)
        self.assertEqual(benutzer["nachname"], NACHNAME)
        self.assertEqual(benutzer["email"],    EMAIL)
        self.assertEqual(benutzer["rolle"],    ROLLE)

        per_email = self.db.benutzer_mit_email_laden(EMAIL)
        self.assertIsNotNone(per_email, "benutzer_mit_email_laden() sollte einen Datensatz liefern.")
        self.assertEqual(per_email["benutzername"], BENUTZERNAME)

        # Duplikat-E-Mail muss abgelehnt werden
        duplikat = self.db.benutzer_speichern(
            "anderer_user", PASSWORT, "Max", "Muster", EMAIL, ROLLE
        )
        self.assertFalse(duplikat, "Doppelte E-Mail sollte False zurückgeben.")

    # ── 4.7  Ausleihe: erstellen, verlängern, zurückgeben ────────────────────

    def test_4_7_ausleihe_lebenszyklus(self):
        self._buch_und_exemplar()
        self._benutzer()

        # Ausleihe speichern
        result = self.db.ausleih_speichern(
            AUSLEIH_ID_1, BENUTZERNAME, EXEMPLAR_ID, AUSLEIHDATUM_1, FAELLIGKEIT_1
        )
        self.assertTrue(result, "ausleih_speichern() sollte True zurückgeben.")

        # Aktive Ausleihen des Benutzers
        aktive = self.db.ausleihen_benutzer(BENUTZERNAME)
        self.assertEqual(len(aktive), 1, "Es sollte genau 1 aktive Ausleihe geben.")
        self.assertTrue(
            any(TITEL_1 in str(a.get("titel", "")) for a in aktive),
            "Buchtitel sollte in der Ausleihe enthalten sein."
        )

        # Anzahl aktiver Ausleihen
        self.assertEqual(self.db.anzahl_ausleihen_benutzer(BENUTZERNAME), 1)

        # Verlängern
        verlaengert = self.db.ausleih_verlaengern(AUSLEIH_ID_1, "2026-06-17")
        self.assertTrue(verlaengert, "ausleih_verlaengern() sollte True zurückgeben.")

        ausleihe = self.db.ausleih_laden(AUSLEIH_ID_1)
        self.assertEqual(ausleihe["faelligkeit"],         "2026-06-17")
        self.assertEqual(ausleihe["verlaengerungsanzahl"], 1)

        # Rückgabe
        rueckgabe = self.db.ausleih_rueckgabe(AUSLEIH_ID_1)
        self.assertTrue(rueckgabe, "ausleih_rueckgabe() sollte True zurückgeben.")

        aktive_danach = self.db.ausleihen_benutzer(BENUTZERNAME)
        self.assertEqual(len(aktive_danach), 0,
                         "Nach Rückgabe sollten 0 aktive Ausleihen übrig sein.")

    # ── 4.8  Überfällige Ausleihen ───────────────────────────────────────────

    def test_4_8_ueberfaellige_ausleihen(self):
        self._buch_und_exemplar()
        self._benutzer()

        self.db.ausleih_speichern(
            AUSLEIH_ID_2, BENUTZERNAME, EXEMPLAR_ID, AUSLEIHDATUM_2, FAELLIGKEIT_2
        )

        ueberfaellig = self.db.ueberfaellige_ausleihen()
        self.assertGreaterEqual(len(ueberfaellig), 1,
                                "Mindestens 1 überfällige Ausleihe erwartet.")
        eintrag = ueberfaellig[0]
        self.assertIn("vorname", eintrag, "'vorname' sollte im Ergebnis enthalten sein.")
        self.assertIn("titel",   eintrag, "'titel' sollte im Ergebnis enthalten sein.")

    # ── 4.9  Merkliste ───────────────────────────────────────────────────────

    def test_4_9_merkliste(self):
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)
        self._benutzer()

        # Hinzufügen
        result = self.db.merkliste_hinzufuegen(BENUTZERNAME, ISBN_1)
        self.assertTrue(result, "merkliste_hinzufuegen() sollte True zurückgeben.")

        # Duplikat abweisen
        duplikat = self.db.merkliste_hinzufuegen(BENUTZERNAME, ISBN_1)
        self.assertFalse(duplikat, "Duplikat in der Merkliste sollte False zurückgeben.")

        # Laden
        merkliste = self.db.merkliste_laden(BENUTZERNAME)
        self.assertEqual(len(merkliste), 1, "Merkliste sollte genau 1 Eintrag haben.")
        self.assertIn("titel", merkliste[0], "Merkliste-Eintrag sollte Buchdetails enthalten.")

        # Entfernen
        entfernt = self.db.merkliste_entfernen(BENUTZERNAME, ISBN_1)
        self.assertTrue(entfernt, "merkliste_entfernen() sollte True zurückgeben.")

        leer = self.db.merkliste_laden(BENUTZERNAME)
        self.assertEqual(len(leer), 0, "Merkliste sollte nach dem Entfernen leer sein.")

    # ── 4.10  Buch löschen (mit Einschränkung) ───────────────────────────────

    def test_4_10_buch_loeschen(self):
        self._buch_und_exemplar()

        # Löschen bei ausgeliehenen Exemplaren verweigern
        self.db.exemplar_status_aktualisieren(EXEMPLAR_ID, "ausgeliehen")
        result_fehl = self.db.buch_loeschen(ISBN_1)
        self.assertFalse(result_fehl,
                         "Löschen sollte fehlschlagen, solange Exemplare ausgeliehen sind.")

        # Nach Freigabe erlaubt
        self.db.exemplar_status_aktualisieren(EXEMPLAR_ID, "verfuegbar")
        result_ok = self.db.buch_loeschen(ISBN_1)
        self.assertTrue(result_ok, "Löschen sollte nach Freigabe True zurückgeben.")

        self.assertIsNone(self.db.buch_laden(ISBN_1),
                          "Buch sollte nach dem Löschen nicht mehr auffindbar sein.")

        exemplare = self.db.exemplare_laden(ISBN_1)
        self.assertEqual(len(exemplare), 0,
                         "Exemplare sollten beim Kaskadenlöschen mitentfernt worden sein.")

    # ── 4.11  Verbindung schließen ───────────────────────────────────────────

    def test_4_11_verbindung_schliessen(self):
        try:
            self.db.schliessen()
        except Exception as e:
            self.fail(f"schliessen() hat eine unerwartete Exception ausgelöst: {e}")


# ─── Einstiegspunkt ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)