"""
Backend.bootstrap
=================
Bootstrap-/Seed-Logik, die beim App-Start ausgeführt wird.

Hält `Backend/services/__init__.py` schlank: dort werden nur DB + Services gebaut.
"""

from __future__ import annotations

from typing import Any

from Datenbank.seed_demo_daten import korrigiere_demo_isbns, seed_demo_ausleihen, seed_demo_buecher


# Dokumentierter lokaler Admin (README Abschnitt „Lokaler Admin-Zugang“)
LOKALER_ADMIN: dict[str, str] = {
    "benutzername": "admin1",
    "passwort": "admin123",
    "vorname": "Lokal",
    "nachname": "Admin",
    "email": "admin1@bibflow.local",
    "rolle": "Admin",
}

# Optionaler Demo-Benutzer zum Testen der Benutzer-Ansicht
LOKALER_DEMO_BENUTZER: dict[str, str] = {
    "benutzername": "demo",
    "passwort": "demo123",
    "vorname": "Demo",
    "nachname": "Benutzer",
    "email": "demo@bibflow.local",
    "rolle": "Benutzer",
}


def _konto_anlegen_wenn_fehlt(benutzer_service: Any, konto: dict) -> None:
    if benutzer_service.db.benutzer_laden(konto["benutzername"]):
        return
    try:
        benutzer_service.benutzer_registrieren(**konto)
    except ValueError as exc:
        # Nur warnen, nicht hard-fail: Bootstrap soll App nicht blockieren.
        if hasattr(benutzer_service, "logger") and benutzer_service.logger:
            benutzer_service.logger.warning(
                "Lokales Konto '%s' konnte nicht angelegt werden: %s",
                konto["benutzername"],
                exc,
            )


def _ensure_lokaler_admin(benutzer_service: Any, logger) -> None:
    """Stellt den dokumentierten Admin admin1 immer bereit (anlegen oder README-Passwort sicherstellen)."""
    from Backend.services.benutzer_service import _passwort_hashen

    bn = LOKALER_ADMIN["benutzername"]
    pw = LOKALER_ADMIN["passwort"]

    try:
        benutzer_service.login(bn, pw)
        return
    except ValueError:
        pass

    if benutzer_service.db.benutzer_laden(bn):
        benutzer_service.db.benutzer_passwort_aktualisieren(bn, _passwort_hashen(pw))
        return

    try:
        benutzer_service.benutzer_registrieren(**LOKALER_ADMIN)
    except ValueError as exc:
        logger.warning("Lokaler Admin '%s' konnte nicht angelegt werden: %s", bn, exc)


def ensure_lokale_zugaenge(benutzer_service: Any, logger) -> None:
    """Lokaler Admin ist immer vorhanden; Demo-Benutzer nur bei Bedarf."""
    _ensure_lokaler_admin(benutzer_service, logger)
    _konto_anlegen_wenn_fehlt(benutzer_service, LOKALER_DEMO_BENUTZER)


def ensure_demo_bibliotheksbestand(db: Any, buch_service: Any) -> None:
    """Legt den Demo-Buchkatalog an, wenn die DB noch keine Bücher enthält."""
    korrigiere_demo_isbns(db)
    seed_demo_buecher(buch_service)


def ensure_demo_ausleihen(db: Any) -> None:
    """Legt überfällige und bald fällige Demo-Ausleihen für Benutzer demo an."""
    seed_demo_ausleihen(db)

