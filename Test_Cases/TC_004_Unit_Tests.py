"""
Test case ID:       TC_004 (TC_004_U1 … TC_004_U6)
Title:              Unit-Tests BuchService / AusleiheService / BenutzerService
Preconditions:      Frische Test-DB pro Test; ORMDatenbankManager + Service-Instanzen
Test steps:         Service-Methoden mit gültigen/ungültigen Daten aufrufen; Ergebnis prüfen
Test data/input:    ISBNs 9783000000001–6; Benutzer maxausleihen, verlanger; Jahre/ISBN-Validierung
Expected result:    U1/U2: ValueError; U3: Duplikat verhindert; U4: Titel/ISBN aktualisiert;
                    U5: max. 5 Ausleihen; U6: nur eine Verlängerung
Actual result:      (automatisch via unittest)
Status:             automatisierbar – pass/fail in Konsole
Comments:           Siehe Test_Cases/README.md; Ausführen: python Test_Cases/TC_004_Unit_Tests.py
"""

import os
import sys
import unittest

PROJEKT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..").replace("\\", "/")
if PROJEKT_ROOT not in sys.path:
    sys.path.insert(0, PROJEKT_ROOT)

from Datenbank.orm_manager import ORMDatenbankManager
from Datenbank.test_db_util import (
    cleanup_all_test_dbs,
    cleanup_test_db,
    create_temp_db_path,
    remove_legacy_test_db_files,
)
from Backend.services.ausleihe_service import AusleiheService
from Backend.services.buch_service import BuchService
from Backend.services.benutzer_service import BenutzerService


class TC_004_UnitTests(unittest.TestCase):
    """
    Unit-Tests TC_004_U1–U6
    Testet zentrale Service-Methoden (BuchService, AusleiheService, BenutzerService)
    in einem frischen Test-Setup ohne UI.
    """

    @classmethod
    def setUpClass(cls):
        remove_legacy_test_db_files(PROJEKT_ROOT)

    @classmethod
    def tearDownClass(cls):
        cleanup_all_test_dbs()
        remove_legacy_test_db_files(PROJEKT_ROOT)

    def setUp(self):
        self.db_path = create_temp_db_path("tc004_")
        self.db = ORMDatenbankManager(self.db_path)
        self.buch_service = BuchService(self.db)
        self.benutzer_service = BenutzerService(self.db)
        self.ausleihe_service = AusleiheService(self.db)
        self.addCleanup(cleanup_test_db, self.db_path, lambda: self.db)

    def test_U1_buch_erstellen_verwirft_ungueltiges_jahr(self):
        """Ein ungültiges Jahr muss vom BuchService abgefangen werden."""
        with self.assertRaises(ValueError) as ctx:
            self.buch_service.buch_erstellen(
                titel="Ungültiges Jahr",
                autor="Testautor",
                isbn="9783000000001",
                jahr=99,
                exemplar_anzahl=1,
            )
        self.assertIn("jahr", str(ctx.exception).lower())

    def test_U2_buch_erstellen_verwirft_zu_kurze_isbn(self):
        """Eine ISBN mit zu wenigen Ziffern muss scheitern."""
        with self.assertRaises(ValueError) as ctx:
            self.buch_service.buch_erstellen(
                titel="Kurze ISBN",
                autor="Testautor",
                isbn="123456789012",
                jahr=2024,
                exemplar_anzahl=1,
            )
        self.assertIn("isbn", str(ctx.exception).lower())

    def test_U3_buch_erstellen_verhindert_duplikat(self):
        """Doppelte ISBNs dürfen nicht erneut gespeichert werden."""
        self.buch_service.buch_erstellen(
            titel="Originaltitel",
            autor="Testautor",
            isbn="9783000000002",
            jahr=2024,
            exemplar_anzahl=1,
        )

        with self.assertRaises(ValueError) as ctx:
            self.buch_service.buch_erstellen(
                titel="Duplikat",
                autor="Testautor",
                isbn="9783000000002",
                jahr=2024,
                exemplar_anzahl=1,
            )

        self.assertIn("existiert", str(ctx.exception).lower())

    def test_U4_buch_bearbeiten_aendert_isbn_und_titel(self):
        """Buchdaten dürfen über den Service aktualisiert werden."""
        self.buch_service.buch_erstellen(
            titel="Alter Titel",
            autor="Testautor",
            isbn="9783000000003",
            jahr=2024,
            exemplar_anzahl=1,
        )

        result = self.buch_service.buch_bearbeiten(
            isbn="9783000000003",
            titel="Neuer Titel",
            isbn_neu="9783000000004",
        )

        self.assertTrue(result)
        self.assertIsNone(self.db.buch_laden("9783000000003"))
        aktualisiertes_buch = self.db.buch_laden("9783000000004")
        self.assertIsNotNone(aktualisiertes_buch)
        self.assertEqual(aktualisiertes_buch["titel"], "Neuer Titel")

    def test_U5_buch_ausleihen_schlaegt_fehl_bei_5_aktiven_ausleihen(self):
        """Der Service muss den Maximalwert von 5 aktiven Ausleihen erzwingen."""
        self.benutzer_service.benutzer_registrieren(
            benutzername="maxausleihen",
            passwort="geheim123",
            vorname="Max",
            nachname="Ausleiher",
            email="maxausleihen@test.de",
            rolle="Benutzer",
        )
        self.buch_service.buch_erstellen(
            titel="Fünf Exemplare",
            autor="Testautor",
            isbn="9783000000005",
            jahr=2024,
            exemplar_anzahl=6,
        )

        for _ in range(5):
            self.ausleihe_service.buch_ausleihen("maxausleihen", "9783000000005")

        with self.assertRaises(ValueError) as ctx:
            self.ausleihe_service.buch_ausleihen("maxausleihen", "9783000000005")

        self.assertIn("maximal 5", str(ctx.exception).lower())

    def test_U6_ausleihe_verlaengern_schlaegt_fehl_wenn_bereits_verlaengert(self):
        """Eine Ausleihe darf nur einmal verlängert werden."""
        self.benutzer_service.benutzer_registrieren(
            benutzername="verlanger",
            passwort="geheim123",
            vorname="Verl",
            nachname="Anger",
            email="verlanger@test.de",
            rolle="Benutzer",
        )
        self.buch_service.buch_erstellen(
            titel="Verlängerbar",
            autor="Testautor",
            isbn="9783000000006",
            jahr=2024,
            exemplar_anzahl=1,
        )

        ausleih_id = self.ausleihe_service.buch_ausleihen("verlanger", "9783000000006")

        self.assertTrue(self.ausleihe_service.ausleihe_verlaengern(ausleih_id))

        with self.assertRaises(ValueError) as ctx:
            self.ausleihe_service.ausleihe_verlaengern(ausleih_id)

        self.assertIn("verlängert", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
