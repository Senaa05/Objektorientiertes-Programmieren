"""
ORM Manager - SQLAlchemy Datenbank-Manager
========================================
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import date, timedelta
from typing import List, Optional, Dict
import uuid

import sys, os as _os
_datenbank_pfad = _os.path.dirname(_os.path.abspath(__file__))
if _datenbank_pfad not in sys.path:
    sys.path.insert(0, _datenbank_pfad)

from orm_models import (
    Buch, Exemplar, Benutzer, Ausleihe, Merkliste,
    get_session, create_tables, init_engine
)

class ORMDatenbankManager:
    """ORM-basierter Datenbank-Manager mit SQLAlchemy"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path
        init_engine(db_path)
        create_tables()
        print(f"ORM-Datenbank verbunden: {db_path}")
    
    def get_session(self) -> Session:
        """Gibt eine neue Session zurück"""
        return get_session()
    
    # ==================== BÜCHER-CRUD ====================
    
    def buch_speichern(self, titel: str, autor: str, isbn: str, jahr: int) -> bool:
        """Speichert ein neues Buch über ORM"""
        try:
            with self.get_session() as session:
                buch = Buch(titel=titel, autor=autor, isbn=isbn, jahr=jahr)
                session.add(buch)
                session.commit()
                return True
        except Exception as e:
            print(f"Fehler beim Speichern des Buches: {e}")
            return False
    
    def buch_laden(self, isbn: str) -> Optional[Dict]:
        """Lädt ein Buch über ORM"""
        with self.get_session() as session:
            buch = session.query(Buch).filter(Buch.isbn == isbn).first()
            if buch:
                return {
                    'isbn': buch.isbn,
                    'titel': buch.titel,
                    'autor': buch.autor,
                    'jahr': buch.jahr
                }
        return None
    
    def alle_buecher_laden(self) -> List[Dict]:
        """Lädt alle Bücher über ORM"""
        with self.get_session() as session:
            buecher = session.query(Buch).order_by(Buch.titel).all()
            return [
                {
                    'isbn': buch.isbn,
                    'titel': buch.titel,
                    'autor': buch.autor,
                    'jahr': buch.jahr
                }
                for buch in buecher
            ]
    
    def bucher_suchen(self, suchbegriff: str) -> List[Dict]:
        """Sucht Bücher über ORM"""
        with self.get_session() as session:
            suchbegriff = f"%{suchbegriff}%"
            buecher = session.query(Buch).filter(
                or_(
                    Buch.titel.like(suchbegriff),
                    Buch.autor.like(suchbegriff),
                    Buch.isbn.like(suchbegriff)
                )
            ).order_by(Buch.titel).all()
            
            return [
                {
                    'isbn': buch.isbn,
                    'titel': buch.titel,
                    'autor': buch.autor,
                    'jahr': buch.jahr
                }
                for buch in buecher
            ]
    
    # ==================== EXEMPLARE-CRUD ====================
    
    def exemplar_speichern(self, exemplar_id: str, isbn: str) -> bool:
        """Speichert ein neues Exemplar über ORM"""
        try:
            with self.get_session() as session:
                exemplar = Exemplar(exemplar_id=exemplar_id, isbn=isbn)
                session.add(exemplar)
                session.commit()
                return True
        except Exception as e:
            print(f"Fehler beim Speichern des Exemplars: {e}")
            return False
    
    def verfuegbare_exemplare(self, isbn: str) -> List[Dict]:
        """Gibt verfügbare Exemplare über ORM zurück"""
        with self.get_session() as session:
            exemplare = session.query(Exemplar).filter(
                and_(
                    Exemplar.isbn == isbn,
                    Exemplar.status == 'verfuegbar'
                )
            ).order_by(Exemplar.exemplar_id).all()
            
            return [
                {
                    'exemplar_id': exemplar.exemplar_id,
                    'isbn': exemplar.isbn,
                    'status': exemplar.status
                }
                for exemplar in exemplare
            ]
    
    def exemplar_status_aktualisieren(self, exemplar_id: str, status: str) -> bool:
        """Aktualisiert den Exemplar-Status über ORM"""
        try:
            with self.get_session() as session:
                exemplar = session.query(Exemplar).filter(
                    Exemplar.exemplar_id == exemplar_id
                ).first()
                if exemplar:
                    exemplar.status = status
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Exemplar-Status: {e}")
            return False
    
    # ==================== BENUTZER-CRUD ====================
    
    def benutzer_speichern(self, benutzername: str, passwort: str, vorname: str, 
                         nachname: str, email: str, rolle: str = "Benutzer") -> bool:
        """Speichert einen neuen Benutzer über ORM"""
        try:
            with self.get_session() as session:
                benutzer = Benutzer(
                    benutzername=benutzername,
                    passwort=passwort,
                    vorname=vorname,
                    nachname=nachname,
                    email=email,
                    rolle=rolle
                )
                session.add(benutzer)
                session.commit()
                return True
        except Exception as e:
            print(f"Fehler beim Speichern des Benutzers: {e}")
            return False
    
    def benutzer_laden(self, benutzername: str) -> Optional[Dict]:
        """Lädt einen Benutzer über ORM"""
        with self.get_session() as session:
            benutzer = session.query(Benutzer).filter(
                Benutzer.benutzername == benutzername
            ).first()
            if benutzer:
                return {
                    'benutzername': benutzer.benutzername,
                    'passwort': benutzer.passwort,
                    'vorname': benutzer.vorname,
                    'nachname': benutzer.nachname,
                    'email': benutzer.email,
                    'rolle': benutzer.rolle
                }
        return None
    
    def alle_benutzer_laden(self) -> List[Dict]:
        """Lädt alle Benutzer über ORM"""
        with self.get_session() as session:
            benutzer_liste = session.query(Benutzer).order_by(
                Benutzer.nachname, Benutzer.vorname
            ).all()
            
            return [
                {
                    'benutzername': benutzer.benutzername,
                    'passwort': benutzer.passwort,
                    'vorname': benutzer.vorname,
                    'nachname': benutzer.nachname,
                    'email': benutzer.email,
                    'rolle': benutzer.rolle
                }
                for benutzer in benutzer_liste
            ]
    
    # ==================== AUSLEIHEN-CRUD ====================
    
    def ausleih_speichern(self, ausleih_id: str, benutzername: str, exemplar_id: str, 
                         ausleihdatum: str, faelligkeit: str) -> bool:
        """Speichert eine neue Ausleihe über ORM"""
        try:
            with self.get_session() as session:
                ausleihe = Ausleihe(
                    ausleih_id=ausleih_id,
                    benutzername=benutzername,
                    exemplar_id=exemplar_id,
                    ausleihdatum=date.fromisoformat(ausleihdatum),
                    faelligkeit=date.fromisoformat(faelligkeit)
                )
                session.add(ausleihe)
                session.commit()
                return True
        except Exception as e:
            print(f"Fehler beim Speichern der Ausleihe: {e}")
            return False
    
    def ausleihen_benutzer(self, benutzername: str) -> List[Dict]:
        """Lädt alle Ausleihen eines Benutzers über ORM"""
        with self.get_session() as session:
            ausleihen = session.query(Ausleihe).filter(
                and_(
                    Ausleihe.benutzername == benutzername,
                    Ausleihe.rueckgabedatum.is_(None)
                )
            ).join(Ausleihe.exemplar).join(Exemplar.buch).order_by(
                Ausleihe.faelligkeit
            ).all()
            
            return [
                {
                    'ausleih_id': ausleihe.ausleih_id,
                    'benutzername': ausleihe.benutzername,
                    'exemplar_id': ausleihe.exemplar_id,
                    'ausleihdatum': ausleihe.ausleihdatum.strftime('%Y-%m-%d'),
                    'faelligkeit': ausleihe.faelligkeit.strftime('%Y-%m-%d'),
                    'rueckgabedatum': ausleihe.rueckgabedatum.strftime('%Y-%m-%d') if ausleihe.rueckgabedatum else None,
                    'verlaengerungsanzahl': ausleihe.verlaengerungsanzahl,
                    'titel': ausleihe.exemplar.buch.titel,
                    'autor': ausleihe.exemplar.buch.autor
                }
                for ausleihe in ausleihen
            ]
    
    def anzahl_ausleihen_benutzer(self, benutzername: str) -> int:
        """Gibt die Anzahl der aktiven Ausleihen zurück über ORM"""
        with self.get_session() as session:
            return session.query(Ausleihe).filter(
                and_(
                    Ausleihe.benutzername == benutzername,
                    Ausleihe.rueckgabedatum.is_(None)
                )
            ).count()
    
    def ausleihe_verlaengern(self, ausleih_id: str, neue_faelligkeit: str) -> bool:
        """Alias – Service ruft diesen Namen auf"""
        return self.ausleihe_verlaengern(ausleih_id, neue_faelligkeit)

    def ausleihe_verlaengern(self, ausleih_id: str, neue_faelligkeit: str) -> bool:
        """Verlängert eine Ausleihe über ORM"""
        try:
            with self.get_session() as session:
                ausleihe = session.query(Ausleihe).filter(
                    Ausleihe.ausleih_id == ausleih_id
                ).first()
                if ausleihe:
                    ausleihe.faelligkeit = date.fromisoformat(neue_faelligkeit)
                    ausleihe.verlaengerungsanzahl += 1
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Fehler beim Verlängern der Ausleihe: {e}")
            return False
    
    # ==================== MERKLISTE-CRUD ====================
    
    def merkliste_hinzufuegen(self, benutzername: str, isbn: str) -> bool:
        """Fügt ein Buch zur Merkliste über ORM hinzu"""
        try:
            with self.get_session() as session:
                # Prüfen ob bereits vorhanden
                existiert = session.query(Merkliste).filter(
                    and_(
                        Merkliste.benutzername == benutzername,
                        Merkliste.isbn == isbn
                    )
                ).first()
                
                if not existiert:
                    merkliste = Merkliste(benutzername=benutzername, isbn=isbn)
                    session.add(merkliste)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Fehler beim Hinzufügen zur Merkliste: {e}")
            return False
    
    def merkliste_laden(self, benutzername: str) -> List[Dict]:
        """Lädt die Merkliste über ORM"""
        with self.get_session() as session:
            merkliste = session.query(Merkliste).filter(
                Merkliste.benutzername == benutzername
            ).join(Merkliste.buch).order_by(
                desc(Merkliste.hinzugefuegt_am)
            ).all()
            
            return [
                {
                    'id': eintrag.id,
                    'benutzername': eintrag.benutzername,
                    'isbn': eintrag.isbn,
                    'titel': eintrag.buch.titel,
                    'autor': eintrag.buch.autor,
                    'jahr': eintrag.buch.jahr,
                    'hinzugefuegt_am': eintrag.hinzugefuegt_am.strftime('%Y-%m-%d')
                }
                for eintrag in merkliste
            ]
    
    def merkliste_entfernen(self, benutzername: str, isbn: str) -> bool:
        """Entfernt ein Buch aus der Merkliste über ORM"""
        try:
            with self.get_session() as session:
                eintrag = session.query(Merkliste).filter(
                    and_(
                        Merkliste.benutzername == benutzername,
                        Merkliste.isbn == isbn
                    )
                ).first()
                if eintrag:
                    session.delete(eintrag)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Fehler beim Entfernen aus der Merkliste: {e}")
            return False
    
    def ausleih_laden(self, ausleih_id: str) -> Optional[Dict]:
        """Lädt eine einzelne Ausleihe per ID"""
        with self.get_session() as session:
            a = session.query(Ausleihe).filter(Ausleihe.ausleih_id == ausleih_id).first()
            if a:
                return {
                    'ausleih_id': a.ausleih_id,
                    'benutzername': a.benutzername,
                    'exemplar_id': a.exemplar_id,
                    'ausleihdatum': a.ausleihdatum.strftime('%Y-%m-%d'),
                    'faelligkeit': a.faelligkeit.strftime('%Y-%m-%d'),
                    'rueckgabedatum': a.rueckgabedatum.strftime('%Y-%m-%d') if a.rueckgabedatum else None,
                    'verlaengerungsanzahl': a.verlaengerungsanzahl,
                }
        return None

    def ausleih_rueckgabe(self, ausleih_id: str) -> bool:
        """Setzt rueckgabedatum (Service setzt Exemplar-Status separat)"""
        try:
            with self.get_session() as session:
                a = session.query(Ausleihe).filter(
                    Ausleihe.ausleih_id == ausleih_id,
                    Ausleihe.rueckgabedatum.is_(None)
                ).first()
                if a:
                    a.rueckgabedatum = date.today()
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Fehler bei Rückgabe: {e}")
            return False

    def ueberfaellige_ausleihen(self) -> List[Dict]:
        """Gibt alle überfälligen aktiven Ausleihen zurück"""
        with self.get_session() as session:
            heute = date.today()
            ausleihen = session.query(Ausleihe).filter(
                Ausleihe.faelligkeit < heute,
                Ausleihe.rueckgabedatum.is_(None)
            ).join(Ausleihe.benutzer).join(Ausleihe.exemplar).join(Exemplar.buch).order_by(Ausleihe.faelligkeit).all()
            return [
                {
                    'ausleih_id': a.ausleih_id,
                    'benutzername': a.benutzername,
                    'exemplar_id': a.exemplar_id,
                    'faelligkeit': a.faelligkeit.strftime('%Y-%m-%d'),
                    'vorname': a.benutzer.vorname,
                    'nachname': a.benutzer.nachname,
                    'email': a.benutzer.email,
                    'titel': a.exemplar.buch.titel,
                }
                for a in ausleihen
            ]

    def benutzer_mit_email_laden(self, email: str) -> Optional[Dict]:
        """Lädt einen Benutzer anhand der E-Mail"""
        with self.get_session() as session:
            b = session.query(Benutzer).filter(Benutzer.email == email).first()
            if b:
                return {'benutzername': b.benutzername, 'email': b.email, 'rolle': b.rolle}
        return None

    def beliebteste_buecher_laden(self, limit: int = 5) -> List[Dict]:
        """Gibt die am häufigsten ausgeliehenen Bücher zurück"""
        from sqlalchemy import func
        with self.get_session() as session:
            ergebnisse = session.query(
                Buch.isbn, Buch.titel, Buch.autor, Buch.jahr,
                func.count(Ausleihe.ausleih_id).label('anzahl_ausleihen')
            ).outerjoin(Exemplar, Buch.isbn == Exemplar.isbn
            ).outerjoin(Ausleihe, Exemplar.exemplar_id == Ausleihe.exemplar_id
            ).group_by(Buch.isbn).order_by(func.count(Ausleihe.ausleih_id).desc()
            ).limit(limit).all()
            return [
                {'isbn': r.isbn, 'titel': r.titel, 'autor': r.autor,
                 'jahr': r.jahr, 'anzahl_ausleihen': r.anzahl_ausleihen}
                for r in ergebnisse
            ]

    def exemplare_laden(self, isbn: str) -> List[Dict]:
        """Lädt alle Exemplare eines Buches"""
        with self.get_session() as session:
            exemplare = session.query(Exemplar).filter(Exemplar.isbn == isbn).order_by(Exemplar.exemplar_id).all()
            return [{'exemplar_id': e.exemplar_id, 'isbn': e.isbn, 'status': e.status} for e in exemplare]

    def exemplare_fuer_buch_anlegen(self, isbn: str, anzahl: int) -> bool:
        """Legt mehrere Exemplare für ein Buch an"""
        try:
            with self.get_session() as session:
                for _ in range(anzahl):
                    neue_id = "EX-" + str(uuid.uuid4())[:6].upper()
                    session.add(Exemplar(exemplar_id=neue_id, isbn=isbn))
                session.commit()
                return True
        except Exception as e:
            print(f"Fehler beim Anlegen von Exemplaren: {e}")
            return False

    def buch_loeschen(self, isbn: str) -> bool:
        """Löscht ein Buch wenn keine aktiven Ausleihen bestehen"""
        try:
            with self.get_session() as session:
                aktiv = session.query(Exemplar).join(Ausleihe, Exemplar.exemplar_id == Ausleihe.exemplar_id).filter(
                    Exemplar.isbn == isbn, Ausleihe.rueckgabedatum.is_(None)
                ).count()
                if aktiv > 0:
                    return False
                session.query(Exemplar).filter(Exemplar.isbn == isbn).delete()
                session.query(Buch).filter(Buch.isbn == isbn).delete()
                session.commit()
                return True
        except Exception as e:
            print(f"Fehler beim Löschen: {e}")
            return False

    def buch_bearbeiten(self, isbn: str, titel: str = None, autor: str = None, jahr: int = None) -> bool:
        """Aktualisiert Buchfelder"""
        try:
            with self.get_session() as session:
                buch = session.query(Buch).filter(Buch.isbn == isbn).first()
                if not buch:
                    return False
                if titel: buch.titel = titel
                if autor: buch.autor = autor
                if jahr:  buch.jahr = jahr
                session.commit()
                return True
        except Exception as e:
            print(f"Fehler beim Bearbeiten: {e}")
            return False

    def exemplar_loeschen(self, exemplar_id: str) -> bool:
        """Löscht ein einzelnes Exemplar"""
        try:
            with self.get_session() as session:
                exemplar = session.query(Exemplar).filter(
                    Exemplar.exemplar_id == exemplar_id
                ).first()
                if exemplar:
                    session.delete(exemplar)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Fehler beim Löschen des Exemplars: {e}")
            return False

    def schliessen(self):
        """Schließt die Datenbankverbindung (ORM benötigt explizites Schließen nicht)"""
        print("ORM-Datenbankverbindung geschlossen")