"""
Test case ID:       TC_001
Title:              Login-Funktionalität (Integration)
Preconditions:      Leere Test-DB; BenutzerService + ORMDatenbankManager
Test steps:         Registrieren → Login → Rollen-/Hash-Prüfung
Test data/input:    lilly2/test123, admin1/admin123, ungültige Logins
Expected result:    User/Admin korrekt; bcrypt-Hash; Duplikat verhindert
Actual result:      (automatisch via unittest)
Status:             automatisierbar – pass/fail in Konsole
Comments:           Siehe Test_Cases/README.md; Vorlage: Pizzeria-Reference-Project

Ausführen: python Test_Cases/TC_001_Login_Integrationstest.py
"""

import unittest
import os
import sys

# ── Projektpfade einrichten ───────────────────────────────────────────────────
PROJEKT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATENBANK_DIR = os.path.join(PROJEKT_ROOT, "Datenbank")
sys.path.insert(0, PROJEKT_ROOT)
sys.path.insert(0, DATENBANK_DIR)

from Datenbank.orm_manager import ORMDatenbankManager
from Datenbank.test_db_util import (
    cleanup_all_test_dbs,
    cleanup_test_db,
    create_temp_db_path,
    remove_legacy_test_db_files,
)
from Backend.modelle.benutzer import User, Administrator
from Backend.services.benutzer_service import BenutzerService


class TC_001_I1_LoginIntegration(unittest.TestCase):
    """
    Integration Test TC_001_I1
    Testet den vollständigen Login-Ablauf mit echter Datenbank:
      Registrierung → Passwort-Hashing → DB-Speicherung → Login → Rollenprüfung
    """

    # ── Setup / Teardown ──────────────────────────────────────────────────────
    @classmethod
    def setUpClass(cls):
        remove_legacy_test_db_files(PROJEKT_ROOT)

    @classmethod
    def tearDownClass(cls):
        cleanup_all_test_dbs()
        remove_legacy_test_db_files(PROJEKT_ROOT)

    def setUp(self):
        """Arrange: Frische Datenbank + Service vor jedem Test."""
        self.db_path = create_temp_db_path("tc001_")
        self.db = ORMDatenbankManager(self.db_path)
        self.service = BenutzerService(self.db)
        self.addCleanup(cleanup_test_db, self.db_path, lambda: self.db)

        # Zwei Testbenutzer registrieren (mit echtem Hashing)
        self.service.benutzer_registrieren(
            benutzername="lilly2",
            passwort="test123",
            vorname="Lilly",
            nachname="Müller",
            email="lilly2@test.de",
            rolle="Benutzer",
        )
        self.service.benutzer_registrieren(
            benutzername="admin1",
            passwort="admin123",
            vorname="Ada",
            nachname="Admin",
            email="admin1@test.de",
            rolle="Admin",
        )

    # ── Testfälle ─────────────────────────────────────────────────────────────

    def test_I1_login_normaler_benutzer_erfolgreich(self):
        """
        Vollständiger Login-Ablauf für einen normalen Benutzer.
        Passwort wurde gehasht gespeichert und wird korrekt geprüft.
        """
        # Act
        benutzer = self.service.login("lilly2", "test123")

        # Assert: Korrekter Typ, Benutzername und Rolle
        self.assertIsInstance(benutzer, User)
        self.assertEqual(benutzer.benutzername, "lilly2")
        self.assertEqual(benutzer.rolle, "Benutzer")
        self.assertFalse(benutzer.ist_admin())

    def test_I1_login_admin_benutzer_erfolgreich(self):
        """
        Vollständiger Login-Ablauf für einen Admin-Benutzer.
        Rückgabe muss ein Administrator-Objekt mit ist_admin() == True sein.
        """
        # Act
        benutzer = self.service.login("admin1", "admin123")

        # Assert: Admin-Objekt mit korrekter Rolle
        self.assertIsInstance(benutzer, Administrator)
        self.assertEqual(benutzer.benutzername, "admin1")
        self.assertEqual(benutzer.rolle, "Admin")
        self.assertTrue(benutzer.ist_admin())

    def test_I1_login_falsches_passwort_schlaegt_fehl(self):
        """
        Login mit falschem Passwort muss ValueError auslösen.
        Benutzer bleibt auf Login-Seite (kein Zugriff auf Dashboard).
        """
        with self.assertRaises(ValueError) as ctx:
            self.service.login("lilly2", "falschespasswort")
        self.assertIn("falsch", str(ctx.exception).lower())

    def test_I1_login_nicht_existierender_benutzer_schlaegt_fehl(self):
        """
        Login mit unbekanntem Benutzernamen muss ValueError auslösen.
        Entspricht dem Testfall 'Ungültige Test-Daten' aus TC_001.
        """
        with self.assertRaises(ValueError):
            self.service.login("nichtvorhanden", "beliebigespasswort")

    def test_I1_passwort_wird_gehasht_gespeichert(self):
        """
        Passwort darf NICHT im Klartext in der Datenbank stehen.
        Prüft, dass der gespeicherte Hash mit bcrypt-Format beginnt.
        """
        # Direkt aus der DB lesen (am Service vorbei)
        daten = self.db.benutzer_laden("lilly2")
        gespeichertes_passwort = daten["passwort"]

        # Assert: Bcrypt-Hash beginnt immer mit $2b$
        self.assertTrue(
            gespeichertes_passwort.startswith(("$2a$", "$2b$", "$2y$")),
            "Passwort sollte als bcrypt-Hash gespeichert sein, nicht als Klartext!"
        )

    def test_I1_rollenverteilung_benutzer_vs_admin(self):
        """
        ist_admin() muss für Benutzer False und für Admin True liefern.
        Prüft die korrekte Rollenverteilung nach dem Login in der echten DB.
        """
        self.assertFalse(self.service.ist_admin("lilly2"))
        self.assertTrue(self.service.ist_admin("admin1"))

    def test_I1_doppelte_registrierung_verhindert(self):
        """
        Eine zweite Registrierung mit demselben Benutzernamen muss fehlschlagen.
        Schützt vor Duplikaten in der Datenbank.
        """
        with self.assertRaises(ValueError) as ctx:
            self.service.benutzer_registrieren(
                benutzername="lilly2",
                passwort="anderes_passwort",
                vorname="Lilly2",
                nachname="Doppelt",
                email="anders@test.de",
            )
        self.assertIn("existiert", str(ctx.exception).lower())


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)