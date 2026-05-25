"""
Test case ID:       TC_003 (TC_003_I1, TC_003_I2)
Title:              Überfällige Ausleihen / popup_ueberfaellige_fuer_benutzer
Preconditions:      Seed-Bücher + Demo-Ausleihen (überfällig); Benutzer demo/admin1
Test steps:         Seed laden → Service-Methode aufrufen → Liste prüfen
Test data/input:    demo (überfällig), admin1 (ohne eigene überfällige Ausleihe)
Expected result:    I1: ≥1 Eintrag für demo; I2: [] für admin1
Actual result:      (automatisch via unittest)
Status:             automatisierbar – pass/fail in Konsole
Comments:           UI: Login demo/demo123 → Popup in dashboard.py; siehe Test_Cases/README.md

Ausführen: python Test_Cases/TC_003_Popup_Ueberfaellig_Test.py
"""

import os
import sys
import unittest

PROJEKT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, PROJEKT_ROOT)

from Datenbank.orm_manager import ORMDatenbankManager
from Datenbank.seed_demo_daten import seed_demo_ausleihen, seed_demo_buecher
from Datenbank.test_db_util import cleanup_test_db, create_temp_db_path
from Backend.services.benutzer_service import BenutzerService
from Backend.services.buch_service import BuchService
from Backend.services.ausleihe_service import AusleiheService

DEMO_BENUTZER = {
    "benutzername": "demo",
    "passwort": "demo123",
    "vorname": "Demo",
    "nachname": "Benutzer",
    "email": "demo@bibflow.local",
    "rolle": "Benutzer",
}


class TC_003_PopupUeberfaellig(unittest.TestCase):

    def setUp(self):
        self.db_path = create_temp_db_path("tc003_")
        self.db = ORMDatenbankManager(self.db_path)
        self.buch_service = BuchService(self.db)
        self.benutzer_service = BenutzerService(self.db)
        self.ausleihe_service = AusleiheService(self.db)
        self.addCleanup(cleanup_test_db, self.db_path, lambda: self.db)

        seed_demo_buecher(self.buch_service)
        self.benutzer_service.benutzer_registrieren(**DEMO_BENUTZER)
        seed_demo_ausleihen(self.db)

    def test_popup_ueberfaellig_fuer_demo_benutzer(self):
        popups = self.ausleihe_service.popup_ueberfaellige_fuer_benutzer("demo")
        self.assertGreaterEqual(
            len(popups), 1, "Demo-Benutzer soll mindestens eine überfällige Ausleihe haben."
        )
        self.assertEqual(popups[0]["benutzername"], "demo")
        self.assertIn("titel", popups[0])

    def test_popup_nicht_fuer_admin_ohne_eigene_ueberfaellige(self):
        self.benutzer_service.benutzer_registrieren(
            benutzername="admin1",
            passwort="admin123",
            vorname="Test",
            nachname="Admin",
            email="admin1@test.local",
            rolle="Admin",
        )
        popups = self.ausleihe_service.popup_ueberfaellige_fuer_benutzer("admin1")
        self.assertEqual(len(popups), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
