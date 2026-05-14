"""
ORM Manager - SQLAlchemy Datenbank-Manager
========================================
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import date, timedelta
from typing import List, Optional, Dict
import uuid

from orm_models import (
    Buch, Exemplar, Benutzer, Ausleihe, Merkliste,
    get_session, create_tables
)

class ORMDatenbankManager:
    """ORM-basierter Datenbank-Manager mit SQLAlchemy"""
    
    def __init__(self, db_path: str = "bibliothek_orm.db"):
        self.db_path = db_path
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
    
    def ausleihe_rueckgabe(self, ausleih_id: str) -> bool:
        """Verarbeitet die Rückgabe über ORM"""
        try:
            with self.get_session() as session:
                ausleihe = session.query(Ausleihe).filter(
                    Ausleihe.ausleih_id == ausleih_id
                ).first()
                if ausleihe:
                    # Exemplar-Status aktualisieren
                    exemplar = session.query(Exemplar).filter(
                        Exemplar.exemplar_id == ausleihe.exemplar_id
                    ).first()
                    if exemplar:
                        exemplar.status = 'verfuegbar'
                    
                    # Ausleihe als zurückgegeben markieren
                    ausleihe.rueckgabedatum = date.today()
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Fehler bei der Ausleih-Rückgabe: {e}")
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
    
    def schliessen(self):
        """Schließt die Datenbankverbindung (ORM benötigt explizites Schließen nicht)"""
        print("ORM-Datenbankverbindung geschlossen")
