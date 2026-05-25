"""
Buchcover für die UI — Open Library (ISBN + Titelsuche).

Anzeige per nativem <img> und Route /buchcover/{isbn} (zuverlässig in NiceGUI).
"""

import html
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
    schrift = (
        "font-weight:600; font-size:0.75rem; line-height:1.2; color:#334155; "
        "text-align:center; padding:0.5rem; box-sizing:border-box; width:100%; "
        "display:-webkit-box; -webkit-line-clamp:4; -webkit-box-orient:vertical; "
        "overflow:hidden; word-break:break-word; margin:0;"
    )
    if not karussell:
        schrift = (
            "font-weight:600; font-size:0.7rem; line-height:1.15; color:#334155; "
            "text-align:center; padding:0.35rem; box-sizing:border-box; width:100%; "
            "display:-webkit-box; -webkit-line-clamp:5; -webkit-box-orient:vertical; "
            "overflow:hidden; word-break:break-word; margin:0;"
        )

    rahmen = (
        f"width:{breite}; min-width:{breite}; max-width:{breite}; "
        f"height:{hoehe}; min-height:{hoehe}; flex-shrink:0; align-self:stretch; "
        f"border-radius:{rund}; overflow:hidden; background:{farbe}; "
        "display:flex; align-items:center; justify-content:center; box-sizing:border-box; "
        "box-shadow:0 2px 8px rgba(15,23,42,0.12); border:1px solid #e2e8f0;"
    )
    if karussell:
        with ui.element("div").style(
            "width:160px; height:140px; flex-shrink:0; display:flex; "
            f"align-items:center; justify-content:center; border-radius:{rund}; "
            f"overflow:hidden; background:{farbe}; box-sizing:border-box; "
            "box-shadow:0 2px 8px rgba(15,23,42,0.12); border:1px solid #e2e8f0;"
        ):
            ui.label(titel_anzeige).style(schrift)
    else:
        with ui.element("div").style(rahmen):
            ui.label(titel_anzeige).style(schrift)


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

    # Karussell-Karten sind 160px breit — feste Maße, sonst lädt ui.html kein Bild
    if karussell:
        breite = "160px"
        hoehe = "140px"
        rund = "0"

    raw = normalisiere_isbn(isbn)
    if raw in DEMO_ISBN_OHNE_COVER:
        _zeige_nur_platzhalter(titel, breite=breite, hoehe=hoehe, rund=rund, karussell=karussell)
        return

    titel_anzeige = html.escape((titel or "Unbekannt").strip())
    src = cover_bild_pfad(isbn, titel, autor)
    if not src:
        _zeige_nur_platzhalter(titel, breite=breite, hoehe=hoehe, rund=rund, karussell=karussell)
        return

    farbe = _platzhalter_farbe(titel)
    ol_direkt = OPEN_LIBRARY_ISBN.format(isbn=raw)
    api_src = html.escape(src)

    if karussell:
        schrift = "font-size:0.75rem; -webkit-line-clamp:4;"
    else:
        schrift = "font-size:0.7rem; -webkit-line-clamp:5;"

    rahmen = (
        f"width:{breite}; min-width:{breite}; max-width:{breite}; "
        f"height:{hoehe}; min-height:{hoehe}; flex-shrink:0; align-self:stretch; "
        f"border-radius:{rund}; overflow:hidden; position:relative; "
        f"box-sizing:border-box; box-shadow:0 2px 8px rgba(15,23,42,0.12); "
        "border:1px solid #e2e8f0;"
    )
    platzhalter = (
        f"position:absolute; inset:0; z-index:0; background:{farbe}; "
        "display:flex; align-items:center; justify-content:center; "
        "padding:0.35rem; box-sizing:border-box; text-align:center; "
        f"font-weight:600; color:#334155; line-height:1.15; word-break:break-word; {schrift}"
    )
    bild = (
        "position:absolute; inset:0; z-index:1; width:100%; height:100%; "
        "object-fit:cover; display:block;"
    )
    cover_html = f"""
        <div style="{rahmen}">
            <div class="bibflow-cover-ph" style="{platzhalter}">{titel_anzeige}</div>
            <img class="bibflow-cover-img" src="{html.escape(ol_direkt)}" alt="{titel_anzeige}"
                 style="{bild}"
                 onload="if(this.naturalWidth>50&&this.naturalHeight>50){{this.previousElementSibling.style.display='none'}}else{{this.style.display='none'}}"
                 onerror="if(!this.dataset.retry){{this.dataset.retry='1';this.src='{api_src}';}}
                          else{{this.style.display='none'}}">
        </div>
    """
    if karussell:
        with ui.element("div").style(
            "width:160px; height:140px; flex-shrink:0; display:block;"
        ):
            ui.html(cover_html, sanitize=False)
    else:
        ui.html(cover_html, sanitize=False)
