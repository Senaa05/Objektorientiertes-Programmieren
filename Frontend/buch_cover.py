"""
Buchcover für die UI — Open Library (ISBN, optional API-Fallback).

Ein Request pro Cover über /buchcover/{isbn} (Server-Cache, kein Doppel-Laden im Browser).
"""

import json
import re
import threading
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional, Tuple

from nicegui import app, ui

from Backend.demo_katalog import DEMO_ISBN_OHNE_COVER

OPEN_LIBRARY_ISBN = "https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
OPEN_LIBRARY_API = (
    "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
)
OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
OPEN_LIBRARY_COVER_ID = "https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

USER_AGENT = (
    "Bibflow/1.0 (FHNW Bibliotheks-App; "
    "+https://github.com/Senaa05/Objektorientiertes-Programmieren)"
)

PLATZHALTER_FARBEN = ["#fce7f3", "#dbeafe", "#dcfce7", "#fef9c3", "#ede9fe", "#ffedd5"]

# Tailwind-Klassen für Cover-Rahmen und Inhalt
_RAHMEN = "shrink-0 overflow-hidden border border-slate-200 shadow-md box-border"
_KARUSSELL_BOX = f"w-40 h-[140px] {_RAHMEN}"
_LISTE_BOX = f"w-24 h-36 min-w-24 max-w-24 min-h-36 rounded-lg {_RAHMEN} self-stretch"
_PLATZHALTER_SCHICHT = (
    "absolute inset-0 z-0 flex items-center justify-center p-2 "
    "text-center font-semibold text-slate-700 break-words box-border"
)
_LABEL_KARUSSELL = "text-xs leading-tight line-clamp-4 m-0 w-full"
_LABEL_LISTE = "text-[0.7rem] leading-snug line-clamp-5 m-0 w-full px-1.5"
_BILD = "absolute inset-0 z-[1] w-full h-full object-cover"

_bytes_cache: dict[str, Tuple[bytes, str]] = {}
_route_registriert = False
_ol_semaphore = threading.Semaphore(4)

_GOOGLE_PLATZHALTER_GROESSE = 1269
_MIN_COVER_BYTES = 800


def normalisiere_isbn(isbn: str) -> str:
    return re.sub(r"\D", "", isbn or "")


def _cache_key(isbn: str) -> str:
    return normalisiere_isbn(isbn)


def _platzhalter_farbe(titel: str) -> str:
    return PLATZHALTER_FARBEN[sum(ord(c) for c in (titel or "")) % len(PLATZHALTER_FARBEN)]


def _ist_gueltiges_cover(data: bytes, content_type: Optional[str]) -> bool:
    if len(data) < _MIN_COVER_BYTES:
        return False
    if content_type and not content_type.startswith("image/"):
        return False
    if len(data) == _GOOGLE_PLATZHALTER_GROESSE and data[:8] == b"\x89PNG\r\n\x1a\n":
        return False
    if data[:6] == b"GIF89a" and len(data) < 200:
        return False
    return True


def _http_get(url: str) -> Tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with _ol_semaphore:
        with urllib.request.urlopen(req, timeout=10) as antwort:
            data = antwort.read()
            mime = antwort.headers.get("Content-Type") or "image/jpeg"
            return data, mime.split(";")[0].strip()


def _versuche_cover_url(url: str) -> Optional[Tuple[bytes, str]]:
    try:
        data, mime = _http_get(url)
    except (OSError, urllib.error.HTTPError):
        return None
    if _ist_gueltiges_cover(data, mime):
        return data, mime
    return None


def _open_library_api_cover_urls(isbn: str) -> list[str]:
    """Eine Books-API-Anfrage; bevorzugt medium/small URLs aus der Antwort."""
    raw = normalisiere_isbn(isbn)
    if len(raw) < 10:
        return []

    url = OPEN_LIBRARY_API.format(isbn=urllib.parse.quote(raw))
    try:
        roh, _ = _http_get(url)
        data = json.loads(roh.decode("utf-8", errors="replace"))
    except (OSError, urllib.error.HTTPError, json.JSONDecodeError, UnicodeDecodeError):
        return []

    eintrag = data.get(f"ISBN:{raw}") or {}
    cover = eintrag.get("cover") or {}
    urls = []
    for schluessel in ("medium", "small", "large"):
        if schluessel in cover:
            urls.append(cover[schluessel])
    return urls


def _open_library_cover_id_aus_isbn(isbn: str) -> str:
    """Höchstens eine Search-Anfrage (nur ISBN)."""
    raw = normalisiere_isbn(isbn)
    if len(raw) < 10:
        return ""

    url = f"{OPEN_LIBRARY_SEARCH}?{urllib.parse.urlencode({'isbn': raw, 'limit': '1'})}"
    try:
        roh, _ = _http_get(url)
        treffer = json.loads(roh.decode("utf-8", errors="replace"))
    except (OSError, urllib.error.HTTPError, json.JSONDecodeError, UnicodeDecodeError):
        return ""

    docs = treffer.get("docs") or []
    if not docs:
        return ""

    cover_id = docs[0].get("cover_i")
    if cover_id:
        return OPEN_LIBRARY_COVER_ID.format(cover_id=cover_id)
    return ""


def lade_cover_bytes(
    isbn: str, titel: str = "", autor: str = ""
) -> Tuple[Optional[bytes], str]:
    del titel, autor  # Cover hängt an der ISBN; keine Titelsuche mehr (Rate-Limits)

    schluessel = _cache_key(isbn)
    if schluessel in _bytes_cache:
        data, mime = _bytes_cache[schluessel]
        return (data, mime) if data else (None, "")

    raw = normalisiere_isbn(isbn)
    if len(raw) >= 10:
        treffer = _versuche_cover_url(OPEN_LIBRARY_ISBN.format(isbn=raw))
        if treffer:
            _bytes_cache[schluessel] = treffer
            return treffer

        for api_url in _open_library_api_cover_urls(isbn):
            treffer = _versuche_cover_url(api_url)
            if treffer:
                _bytes_cache[schluessel] = treffer
                return treffer

        suche_url = _open_library_cover_id_aus_isbn(isbn)
        if suche_url:
            treffer = _versuche_cover_url(suche_url)
            if treffer:
                _bytes_cache[schluessel] = treffer
                return treffer

    _bytes_cache[schluessel] = (b"", "")
    return None, ""


def cover_bild_pfad(isbn: str, titel: str = "", autor: str = "") -> str:
    del titel, autor
    raw = normalisiere_isbn(isbn)
    if len(raw) < 10:
        return ""
    return f"/buchcover/{raw}"


def registriere_cover_route() -> None:
    global _route_registriert
    if _route_registriert:
        return

    from nicegui import run
    from starlette.responses import Response

    @app.get("/buchcover/{isbn}")
    async def buchcover_endpoint(isbn: str):
        data, mime = await run.io_bound(lade_cover_bytes, isbn)
        if not data:
            return Response(status_code=404)
        return Response(
            content=data,
            media_type=mime,
            headers={"Cache-Control": "public, max-age=86400"},
        )

    _route_registriert = True


def _box_klassen(karussell: bool, breite: str, hoehe: str, rund: str, *, mit_bild: bool = False) -> str:
    if karussell:
        klassen = _KARUSSELL_BOX
    elif breite == "96px" and hoehe == "144px" and rund == "8px":
        klassen = _LISTE_BOX
    else:
        klassen = (
            f"w-[{breite}] min-w-[{breite}] max-w-[{breite}] "
            f"h-[{hoehe}] min-h-[{hoehe}] rounded-[{rund}] {_RAHMEN} self-stretch"
        )
    if mit_bild:
        klassen += " relative"
    return klassen


def _label_klassen(karussell: bool) -> str:
    return _LABEL_KARUSSELL if karussell else _LABEL_LISTE


def _nach_bild_geladen(bild: ui.image, platzhalter: ui.element) -> None:
    """Platzhalter ausblenden, sobald das Cover-Bild geladen ist."""
    ui.run_javascript(
        f"""
        (() => {{
            const root = getElement({bild.id});
            const ph = getElement({platzhalter.id});
            if (!root || !ph) return;
            const img = root.querySelector('img');
            if (!img) {{
                root.style.display = 'none';
                ph.style.display = '';
                return;
            }}
            const pruefen = () => {{
                const ok = img.naturalWidth > 50 && img.naturalHeight > 50;
                if (ok) {{
                    ph.style.display = 'none';
                    root.style.display = '';
                }} else {{
                    root.style.display = 'none';
                    ph.style.display = '';
                }}
            }};
            if (img.complete) pruefen();
            else img.addEventListener('load', pruefen, {{ once: true }});
        }})()
        """
    )


def _zeige_nur_platzhalter(
    titel: str,
    *,
    breite: str,
    hoehe: str,
    rund: str,
    karussell: bool,
):
    """Farbkasten mit Buchtitel — volle Cover-Fläche."""
    farbe = _platzhalter_farbe(titel)
    titel_anzeige = (titel or "Unbekannt").strip()
    box = _box_klassen(karussell, breite, hoehe, rund)
    with ui.element("div").classes(f"{box} flex items-center justify-center").style(
        f"background-color:{farbe}"
    ):
        ui.label(titel_anzeige).classes(_label_klassen(karussell))


def _zeige_cover_mit_bild(
    titel: str,
    farbe: str,
    src: str,
    *,
    breite: str,
    hoehe: str,
    rund: str,
    karussell: bool,
) -> None:
    """Cover nur über /buchcover/ (ein Request, Server-Cache)."""
    titel_anzeige = (titel or "Unbekannt").strip()
    box = _box_klassen(karussell, breite, hoehe, rund, mit_bild=True)

    with ui.element("div").classes(box):
        platzhalter = ui.element("div").classes(_PLATZHALTER_SCHICHT).style(
            f"background-color:{farbe}"
        )
        with platzhalter:
            ui.label(titel_anzeige).classes(_label_klassen(karussell))

        bild = ui.image(src).classes(_BILD)

        def bei_laden(_event=None) -> None:
            _nach_bild_geladen(bild, platzhalter)

        def bei_fehler(_event=None) -> None:
            bild.visible = False
            platzhalter.visible = True

        bild.on("load", bei_laden)
        bild.on("error", bei_fehler)


def zeige_buch_cover(
    isbn: str,
    titel: str,
    autor: str = "",
    *,
    breite: str = "96px",
    hoehe: str = "144px",
    rund: str = "8px",
    karussell: bool = False,
):
    """Echtes Cover oder farbiger Platzhalter mit Titel."""
    registriere_cover_route()

    if karussell:
        breite = "160px"
        hoehe = "140px"
        rund = "0"

    raw = normalisiere_isbn(isbn)
    if raw in DEMO_ISBN_OHNE_COVER:
        _zeige_nur_platzhalter(titel, breite=breite, hoehe=hoehe, rund=rund, karussell=karussell)
        return

    src = cover_bild_pfad(isbn)
    if not src:
        _zeige_nur_platzhalter(titel, breite=breite, hoehe=hoehe, rund=rund, karussell=karussell)
        return

    cache_key = _cache_key(isbn)
    if cache_key in _bytes_cache and not _bytes_cache[cache_key][0]:
        _zeige_nur_platzhalter(titel, breite=breite, hoehe=hoehe, rund=rund, karussell=karussell)
        return

    _zeige_cover_mit_bild(
        titel,
        _platzhalter_farbe(titel),
        src,
        breite=breite,
        hoehe=hoehe,
        rund=rund,
        karussell=karussell,
    )
