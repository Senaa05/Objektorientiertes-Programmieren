"""
Test case ID:       TC_002
Title:              ORMDatenbankManager – CRUD (DB-Tests)
Preconditions:      Frische Test-DB pro Test; SQLAlchemy-Tabellen
Test steps:         Anlegen, Lesen, Ändern, Löschen für alle Entitäten
Test data/input:    Feste ISBNs, testuser1, Ausleih-IDs (siehe Datei)
Expected result:    CRUD korrekt; Lösch-Sperre bei Ausleihe; keine Doppel-E-Mail
Actual result:      (automatisch via unittest)
Status:             automatisierbar – pass/fail in Konsole
Comments:           Siehe Test_Cases/README.md; Vorlage: Pizzeria-Reference-Project

Ausführen im Terminal (Windows): python Datenbank/TC_002_Datenbank_Test.py
Ausführen im Terminal (Mac): python3 Datenbank/TC_002_Datenbank_Test.py
"""
import os
import sys
import unittest

PROJEKT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJEKT_ROOT not in sys.path:
    sys.path.insert(0, PROJEKT_ROOT)

from sqlalchemy import inspect

from Datenbank.orm_manager import ORMDatenbankManager
from Datenbank.orm_models import engine
from Datenbank.test_db_util import (
    cleanup_all_test_dbs,
    cleanup_test_db,
    create_temp_db_path,
    remove_legacy_test_db_files,
)

# ─── Testdaten ────────────────────────────────────────────────────────────────
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


class TestORMDatenbankManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        remove_legacy_test_db_files(PROJEKT_ROOT)

    @classmethod
    def tearDownClass(cls):
        cleanup_all_test_dbs()
        remove_legacy_test_db_files(PROJEKT_ROOT)

    def setUp(self):
        """Frische Datenbank vor jedem Test (im System-Temp, nicht im Projekt)."""
        self.db_path = create_temp_db_path("tc002_")
        self.db = ORMDatenbankManager(self.db_path)
        self.addCleanup(cleanup_test_db, self.db_path, lambda: self.db)

    def _buch_und_exemplar(self):
        """Legt Buch + Exemplar an (Vorbedingung für viele Tests)."""
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)
        self.db.exemplar_speichern(EXEMPLAR_ID, ISBN_1)

    def _benutzer(self):
        """Legt Testbenutzer an."""
        self.db.benutzer_speichern(BENUTZERNAME, PASSWORT, VORNAME, NACHNAME, EMAIL, ROLLE)

    def test_4_1_verbindung_und_tabellen(self):
        """ORMDatenbankManager initialisiert und legt alle 5 Tabellen an."""
        session = self.db.get_session()
        self.assertIsNotNone(session, "get_session() sollte eine Session zurückgeben.")
        session.close()

        inspektor = inspect(engine)
        vorhandene = set(inspektor.get_table_names())
        for tabelle in ("buecher", "exemplare", "benutzer", "ausleihen", "merkliste"):
            self.assertIn(tabelle, vorhandene, f"Tabelle '{tabelle}' fehlt.")

    def test_4_2_buch_speichern_und_laden(self):
        result = self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)
        self.assertTrue(result, "buch_speichern() sollte True zurückgeben.")

        buch = self.db.buch_laden(ISBN_1)
        self.assertIsNotNone(buch, "buch_laden() sollte einen Datensatz liefern.")
        self.assertEqual(buch["titel"], TITEL_1)
        self.assertEqual(buch["autor"], AUTOR_1)
        self.assertEqual(buch["isbn"],  ISBN_1)
        self.assertEqual(buch["jahr"],  JAHR_1)

    def test_4_3_alle_buecher_und_suche(self):
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)
        self.db.buch_speichern(TITEL_2, AUTOR_2, ISBN_2, JAHR_2)

        alle = self.db.alle_buecher_laden()
        self.assertEqual(len(alle), 2, "Es sollten genau 2 Bücher vorhanden sein.")

        treffer_titel = self.db.bucher_suchen("Python")
        self.assertEqual(len(treffer_titel), 1, "Suche nach 'Python' sollte 1 Treffer liefern.")

        treffer_autor = self.db.bucher_suchen("Mustermann")
        self.assertEqual(len(treffer_autor), 1, "Suche nach 'Mustermann' sollte 1 Treffer liefern.")

    def test_4_4_buch_bearbeiten(self):
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)

        result = self.db.buch_bearbeiten(ISBN_1, titel="Python Fortgeschritten")
        self.assertTrue(result, "buch_bearbeiten() sollte True zurückgeben.")

        buch = self.db.buch_laden(ISBN_1)
        self.assertEqual(buch["titel"], "Python Fortgeschritten",
                         "Titel sollte nach buch_bearbeiten() aktualisiert sein.")

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

        duplikat = self.db.benutzer_speichern(
            "anderer_user", PASSWORT, "Max", "Muster", EMAIL, ROLLE
        )
        self.assertFalse(duplikat, "Doppelte E-Mail sollte False zurückgeben.")

    def test_4_7_ausleihe_lebenszyklus(self):
        self._buch_und_exemplar()
        self._benutzer()

        result = self.db.ausleih_speichern(
            AUSLEIH_ID_1, BENUTZERNAME, EXEMPLAR_ID, AUSLEIHDATUM_1, FAELLIGKEIT_1
        )
        self.assertTrue(result, "ausleih_speichern() sollte True zurückgeben.")

        aktive = self.db.ausleihen_benutzer(BENUTZERNAME)
        self.assertEqual(len(aktive), 1, "Es sollte genau 1 aktive Ausleihe geben.")
        self.assertTrue(
            any(TITEL_1 in str(a.get("titel", "")) for a in aktive),
            "Buchtitel sollte in der Ausleihe enthalten sein."
        )

        self.assertEqual(self.db.anzahl_ausleihen_benutzer(BENUTZERNAME), 1)

        verlaengert = self.db.ausleih_verlaengern(AUSLEIH_ID_1, "2026-06-17")
        self.assertTrue(verlaengert, "ausleih_verlaengern() sollte True zurückgeben.")

        ausleihe = self.db.ausleih_laden(AUSLEIH_ID_1)
        self.assertEqual(ausleihe["faelligkeit"],         "2026-06-17")
        self.assertEqual(ausleihe["verlaengerungsanzahl"], 1)

        rueckgabe = self.db.ausleih_rueckgabe(AUSLEIH_ID_1)
        self.assertTrue(rueckgabe, "ausleih_rueckgabe() sollte True zurückgeben.")

        aktive_danach = self.db.ausleihen_benutzer(BENUTZERNAME)
        self.assertEqual(len(aktive_danach), 0,
                         "Nach Rückgabe sollten 0 aktive Ausleihen übrig sein.")

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

    def test_4_9_merkliste(self):
        self.db.buch_speichern(TITEL_1, AUTOR_1, ISBN_1, JAHR_1)
        self._benutzer()

        result = self.db.merkliste_hinzufuegen(BENUTZERNAME, ISBN_1)
        self.assertTrue(result, "merkliste_hinzufuegen() sollte True zurückgeben.")

        duplikat = self.db.merkliste_hinzufuegen(BENUTZERNAME, ISBN_1)
        self.assertFalse(duplikat, "Duplikat in der Merkliste sollte False zurückgeben.")

        merkliste = self.db.merkliste_laden(BENUTZERNAME)
        self.assertEqual(len(merkliste), 1, "Merkliste sollte genau 1 Eintrag haben.")
        self.assertIn("titel", merkliste[0], "Merkliste-Eintrag sollte Buchdetails enthalten.")

        entfernt = self.db.merkliste_entfernen(BENUTZERNAME, ISBN_1)
        self.assertTrue(entfernt, "merkliste_entfernen() sollte True zurückgeben.")

        leer = self.db.merkliste_laden(BENUTZERNAME)
        self.assertEqual(len(leer), 0, "Merkliste sollte nach dem Entfernen leer sein.")

    def test_4_10_buch_loeschen(self):
        self._buch_und_exemplar()

        self.db.exemplar_status_aktualisieren(EXEMPLAR_ID, "ausgeliehen")
        result_fehl = self.db.buch_loeschen(ISBN_1)
        self.assertFalse(result_fehl,
                         "Löschen sollte fehlschlagen, solange Exemplare ausgeliehen sind.")

        self.db.exemplar_status_aktualisieren(EXEMPLAR_ID, "verfuegbar")
        result_ok = self.db.buch_loeschen(ISBN_1)
        self.assertTrue(result_ok, "Löschen sollte nach Freigabe True zurückgeben.")

        self.assertIsNone(self.db.buch_laden(ISBN_1),
                          "Buch sollte nach dem Löschen nicht mehr auffindbar sein.")

        exemplare = self.db.exemplare_laden(ISBN_1)
        self.assertEqual(len(exemplare), 0,
                         "Exemplare sollten beim Kaskadenlöschen mitentfernt worden sein.")

    def test_4_11_verbindung_schliessen(self):
        try:
            self.db.schliessen()
        except Exception as e:
            self.fail(f"schliessen() hat eine unerwartete Exception ausgelöst: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
