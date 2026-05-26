"""
Buchcover für die UI — Open Library (ISBN + Titelsuche).

Anzeige per nativem <img> und Route /buchcover/{isbn} (zuverlässig in NiceGUI).
"""

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional, Tuple

from nicegui import app, ui

from Datenbank.seed_demo_daten import DEMO_ISBN_OHNE_COVER

OPEN_LIBRARY_ISBN = "https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
OPEN_LIBRARY_API = (
    "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
)
OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
OPEN_LIBRARY_COVER_ID = "https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

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

_GOOGLE_PLATZHALTER_GROESSE = 1269


def normalisiere_isbn(isbn: str) -> str:
    return re.sub(r"\D", "", isbn or "")


def _cache_key(isbn: str, titel: str, autor: str) -> str:
    raw = normalisiere_isbn(isbn)
    return f"{raw}|{(titel or '').strip()}|{(autor or '').strip()}"


def _platzhalter_farbe(titel: str) -> str:
    return PLATZHALTER_FARBEN[sum(ord(c) for c in (titel or "")) % len(PLATZHALTER_FARBEN)]


def _ist_gueltiges_cover(data: bytes, content_type: Optional[str]) -> bool:
    if len(data) < 1500:
        return False
    if content_type and not content_type.startswith("image/"):
        return False
    if len(data) == _GOOGLE_PLATZHALTER_GROESSE and data[:8] == b"\x89PNG\r\n\x1a\n":
        return False
    if data[:6] == b"GIF89a" and len(data) < 200:
        return False
    return True


def _http_get(url: str) -> Tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Bibflow/1.0"})
    with urllib.request.urlopen(req, timeout=12) as antwort:
        data = antwort.read()
        mime = antwort.headers.get("Content-Type") or "image/jpeg"
        return data, mime.split(";")[0].strip()


def _open_library_api_covers(isbn: str) -> list:
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
    for schluessel in ("large", "medium", "small"):
        if schluessel in cover:
            urls.append(cover[schluessel])
    return urls


def _open_library_suche_cover(titel: str, autor: str, isbn: str = "") -> str:
    raw = normalisiere_isbn(isbn)
    suchvarianten = []

    if titel and autor:
        suchvarianten.append({"title": titel, "author": autor, "limit": "1"})
    if titel:
        suchvarianten.append({"q": titel, "limit": "1"})
    if len(raw) >= 10:
        suchvarianten.append({"isbn": raw, "limit": "1"})

    for params in suchvarianten:
        url = f"{OPEN_LIBRARY_SEARCH}?{urllib.parse.urlencode(params)}"
        try:
            roh, _ = _http_get(url)
            treffer = json.loads(roh.decode("utf-8", errors="replace"))
        except (OSError, urllib.error.HTTPError, json.JSONDecodeError, UnicodeDecodeError):
            continue

        docs = treffer.get("docs") or []
        if not docs:
            continue

        cover_id = docs[0].get("cover_i")
        if cover_id:
            return OPEN_LIBRARY_COVER_ID.format(cover_id=cover_id)

    return ""


def _cover_kandidaten(isbn: str, titel: str, autor: str) -> list:
    raw = normalisiere_isbn(isbn)
    kandidaten = []
    kandidaten.extend(_open_library_api_covers(isbn))
    if len(raw) >= 10:
        kandidaten.append(OPEN_LIBRARY_ISBN.format(isbn=raw))

    suche_url = _open_library_suche_cover(titel, autor, isbn)
    if suche_url:
        kandidaten.append(suche_url)

    gesehen = set()
    eindeutig = []
    for url in kandidaten:
        if url not in gesehen:
            gesehen.add(url)
            eindeutig.append(url)
    return eindeutig


def lade_cover_bytes(
    isbn: str, titel: str = "", autor: str = ""
) -> Tuple[Optional[bytes], str]:
    schluessel = _cache_key(isbn, titel, autor)
    if schluessel in _bytes_cache:
        data, mime = _bytes_cache[schluessel]
        return (data, mime) if data else (None, "")

    for url in _cover_kandidaten(isbn, titel, autor):
        try:
            data, mime = _http_get(url)
        except (OSError, urllib.error.HTTPError):
            continue
        if _ist_gueltiges_cover(data, mime):
            _bytes_cache[schluessel] = (data, mime)
            return data, mime

    _bytes_cache[schluessel] = (b"", "")
    return None, ""


def cover_bild_pfad(isbn: str, titel: str = "", autor: str = "") -> str:
    raw = normalisiere_isbn(isbn)
    if len(raw) < 10:
        return ""
    query = urllib.parse.urlencode({"titel": titel or "", "autor": autor or ""})
    return f"/buchcover/{raw}?{query}"


def registriere_cover_route() -> None:
    global _route_registriert
    if _route_registriert:
        return

    from nicegui import run
    from starlette.responses import Response

    @app.get("/buchcover/{isbn}")
    async def buchcover_endpoint(isbn: str, titel: str = "", autor: str = ""):
        data, mime = await run.io_bound(lade_cover_bytes, isbn, titel, autor)
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
    """Platzhalter nur ausblenden, wenn das Bild wirklich gross genug ist (wie früher onload)."""
    bild.run_javascript(
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
    ol_url: str,
    api_url: str,
    *,
    breite: str,
    hoehe: str,
    rund: str,
    karussell: bool,
) -> None:
    """Cover-Bild mit farbigem Platzhalter-Fallback (Open Library → API-Route)."""
    titel_anzeige = (titel or "Unbekannt").strip()
    box = _box_klassen(karussell, breite, hoehe, rund, mit_bild=True)

    with ui.element("div").classes(box):
        platzhalter = ui.element("div").classes(_PLATZHALTER_SCHICHT).style(
            f"background-color:{farbe}"
        )
        with platzhalter:
            ui.label(titel_anzeige).classes(_label_klassen(karussell))

        bild = ui.image(ol_url).classes(_BILD)
        retry = {"done": False}

        def bei_laden(_event=None) -> None:
            _nach_bild_geladen(bild, platzhalter)

        def bei_fehler(_event=None) -> None:
            if not retry["done"]:
                retry["done"] = True
                bild.set_source(api_url)
            else:
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

    # Karussell-Karten sind 160×140 px (Tailwind w-40 h-[140px])
    if karussell:
        breite = "160px"
        hoehe = "140px"
        rund = "0"

    raw = normalisiere_isbn(isbn)
    if raw in DEMO_ISBN_OHNE_COVER:
        _zeige_nur_platzhalter(titel, breite=breite, hoehe=hoehe, rund=rund, karussell=karussell)
        return

    src = cover_bild_pfad(isbn, titel, autor)
    if not src:
        _zeige_nur_platzhalter(titel, breite=breite, hoehe=hoehe, rund=rund, karussell=karussell)
        return

    # Bereits bekannt: kein Cover in der API → nur farbiger Platzhalter
    cache_key = _cache_key(isbn, titel, autor)
    if cache_key in _bytes_cache and not _bytes_cache[cache_key][0]:
        _zeige_nur_platzhalter(titel, breite=breite, hoehe=hoehe, rund=rund, karussell=karussell)
        return

    _zeige_cover_mit_bild(
        titel,
        _platzhalter_farbe(titel),
        OPEN_LIBRARY_ISBN.format(isbn=raw),
        src,
        breite=breite,
        hoehe=hoehe,
        rund=rund,
        karussell=karussell,
    )
