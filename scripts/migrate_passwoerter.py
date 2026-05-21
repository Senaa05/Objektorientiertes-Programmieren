#!/usr/bin/env python3
"""
Einmalige Migration: Klartext-Passwörter in der DB zu bcrypt-Hashes.
Bestehende Logins funktionieren danach unverändert (gleiches Passwort, nur gehasht gespeichert).

Aufruf vom Projektroot:
  python3 scripts/migrate_passwoerter.py
"""

import os
import sys

projekt_pfad = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for pfad in [projekt_pfad, os.path.join(projekt_pfad, "Backend"), os.path.join(projekt_pfad, "Datenbank")]:
    if pfad not in sys.path:
        sys.path.insert(0, pfad)

from Datenbank.orm_manager import ORMDatenbankManager
from Backend.services.benutzer_service import BenutzerService


def main():
    db_pfad = os.path.join(projekt_pfad, "bibliothek_orm.db")
    if not os.path.isfile(db_pfad):
        print(f"Datenbank nicht gefunden: {db_pfad}")
        sys.exit(1)

    db = ORMDatenbankManager(db_pfad)
    service = BenutzerService(db)
    anzahl = service.passwoerter_migrieren()
    print(f"Migration abgeschlossen: {anzahl} Benutzer-Passwörter gehasht.")


if __name__ == "__main__":
    main()
