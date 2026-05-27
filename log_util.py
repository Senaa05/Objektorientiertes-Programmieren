"""Minimales Logging für Bibflow → logs/bibflow.log (nur Fehler/Warnungen)."""

import logging
import os

_konfiguriert = False


def get_logger(name: str = "services") -> logging.Logger:
    global _konfiguriert
    if not _konfiguriert:
        log_datei = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "bibflow.log")
        os.makedirs(os.path.dirname(log_datei), exist_ok=True)
        handler = logging.FileHandler(log_datei, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        root = logging.getLogger("bibflow")
        root.setLevel(logging.WARNING)
        if not root.handlers:
            root.addHandler(handler)
        root.propagate = False
        _konfiguriert = True
    return logging.getLogger(f"bibflow.{name}")
