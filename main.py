"""
Bibflow - Haupteinstiegspunkt
=============================
Start der Anwendung aus dem Projektroot:

    python main.py

"""
import os
import sys

PROJEKT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJEKT_ROOT not in sys.path:
    sys.path.insert(0, PROJEKT_ROOT)

from Frontend.main_ui import start


if __name__ in {"__main__", "__mp_main__"}:
    start()
