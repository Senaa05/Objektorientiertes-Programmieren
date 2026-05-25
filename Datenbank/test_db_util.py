"""
Hilfsfunktionen für Test-Datenbanken
====================================
Erzeugt SQLite-Dateien im System-Temp (nicht im Projektordner) und räumt
sie inkl. WAL/SHM/Journal-Dateien zuverlässig auf.
"""

from __future__ import annotations

import atexit
import glob
import os
import tempfile

_TEMP_DIR = os.path.join(tempfile.gettempdir(), "bibflow_tests")
_created_paths: list[str] = []

LEGACY_TEST_DB_NAMES = (
    "test_login_integration.db",
    "test_bibliothek.db",
    "bibliothek_2.db",
)


def create_temp_db_path(prefix: str = "test_") -> str:
    """Legt eine leere SQLite-Testdatei im System-Temp an."""
    os.makedirs(_TEMP_DIR, exist_ok=True)
    fd, path = tempfile.mkstemp(prefix=prefix, suffix=".db", dir=_TEMP_DIR)
    os.close(fd)
    _created_paths.append(path)
    return path


def _remove_sqlite_files(db_path: str) -> None:
    for path in (
        db_path,
        f"{db_path}-wal",
        f"{db_path}-shm",
        f"{db_path}-journal",
    ):
        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass


def cleanup_test_db(db_path: str | None, db_manager=None) -> None:
    """Schließt Verbindungen und löscht die Test-Datenbank inkl. Neben-Dateien."""
    if db_manager is not None:
        try:
            db_manager.schliessen()
        except Exception:
            pass
    else:
        try:
            from Datenbank.orm_models import close_database

            close_database()
        except Exception:
            pass

    if db_path:
        _remove_sqlite_files(db_path)
        if db_path in _created_paths:
            _created_paths.remove(db_path)


def cleanup_all_test_dbs() -> None:
    """Entfernt alle bekannten Test-DBs aus dem Temp-Ordner."""
    for path in list(_created_paths):
        cleanup_test_db(path, None)

    if os.path.isdir(_TEMP_DIR):
        for leftover in glob.glob(os.path.join(_TEMP_DIR, "*.db*")):
            try:
                os.remove(leftover)
            except OSError:
                pass


def remove_legacy_test_db_files(project_root: str) -> None:
    """Entfernt alte Test-DBs, die früher im Projektordner angelegt wurden."""
    try:
        from Datenbank.orm_models import close_database

        close_database()
    except Exception:
        pass

    for name in LEGACY_TEST_DB_NAMES:
        _remove_sqlite_files(os.path.join(project_root, name))


atexit.register(cleanup_all_test_dbs)
