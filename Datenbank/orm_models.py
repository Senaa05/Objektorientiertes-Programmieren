"""
ORM Models - SQLAlchemy Datenbankmodelle
===================================
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import date

Base = declarative_base()

class Buch(Base):
    """Buch-Modell für ORM"""
    __tablename__ = 'buecher'
    
    isbn = Column(String, primary_key=True)
    titel = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    jahr = Column(Integer, nullable=False)
    
    # Beziehung zu Exemplaren
    exemplare = relationship("Exemplar", back_populates="buch")
    
    def __repr__(self):
        return f"<Buch(titel='{self.titel}', autor='{self.autor}')>"

class Exemplar(Base):
    """Exemplar-Modell für ORM"""
    __tablename__ = 'exemplare'
    
    exemplar_id = Column(String, primary_key=True)
    isbn = Column(String, ForeignKey('buecher.isbn'), nullable=False)
    status = Column(String, default='verfuegbar')
    
    # Beziehungen
    buch = relationship("Buch", back_populates="exemplare")
    ausleihen = relationship("Ausleihe", back_populates="exemplar")
    
    def __repr__(self):
        return f"<Exemplar(id='{self.exemplar_id}', status='{self.status}')>"

class Benutzer(Base):
    """Benutzer-Modell für ORM"""
    __tablename__ = 'benutzer'
    
    benutzername = Column(String, primary_key=True)
    passwort = Column(String, nullable=False)
    vorname = Column(String, nullable=False)
    nachname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    rolle = Column(String, default='Benutzer')
    
    # Beziehungen
    ausleihen = relationship("Ausleihe", back_populates="benutzer")
    merkliste = relationship("Merkliste", back_populates="benutzer")
    
    def __repr__(self):
        return f"<Benutzer(benutzername='{self.benutzername}', rolle='{self.rolle}')>"

class Ausleihe(Base):
    """Ausleihe-Modell für ORM"""
    __tablename__ = 'ausleihen'
    
    ausleih_id = Column(String, primary_key=True)
    benutzername = Column(String, ForeignKey('benutzer.benutzername'), nullable=False)
    exemplar_id = Column(String, ForeignKey('exemplare.exemplar_id'), nullable=False)
    ausleihdatum = Column(Date, nullable=False)
    faelligkeit = Column(Date, nullable=False)
    rueckgabedatum = Column(Date, nullable=True)
    verlaengerungsanzahl = Column(Integer, default=0)
    
    # Beziehungen
    benutzer = relationship("Benutzer", back_populates="ausleihen")
    exemplar = relationship("Exemplar", back_populates="ausleihen")
    
    def __repr__(self):
        return f"<Ausleihe(id='{self.ausleih_id}', faelligkeit='{self.faelligkeit}')>"

class Merkliste(Base):
    """Merkliste-Modell für ORM"""
    __tablename__ = 'merkliste'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    benutzername = Column(String, ForeignKey('benutzer.benutzername'), nullable=False)
    isbn = Column(String, ForeignKey('buecher.isbn'), nullable=False)
    hinzugefuegt_am = Column(Date, default=date.today)
    
    # Beziehungen
    benutzer = relationship("Benutzer", back_populates="merkliste")
    buch = relationship("Buch")
    
    def __repr__(self):
        return f"<Merkliste(benutzer='{self.benutzername}', isbn='{self.isbn}')>"

import os

DATABASE_URL = "sqlite:///bibliothek_orm.db"
engine = None
SessionLocal = None


def init_database(db_path: str = "bibliothek_orm.db"):
    """Initialisiert Engine und Session für den angegebenen SQLite-Pfad."""
    global engine, SessionLocal, DATABASE_URL
    abs_path = os.path.abspath(db_path)
    os.makedirs(os.path.dirname(abs_path) or ".", exist_ok=True)
    DATABASE_URL = f"sqlite:///{abs_path}"
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


init_database()


def create_tables():
    """Erstellt alle Tabellen in der Datenbank"""
    if engine is None:
        init_database()
    Base.metadata.create_all(bind=engine)


def get_session():
    """Gibt eine neue Datenbank-Session zurück"""
    if SessionLocal is None:
        init_database()
    return SessionLocal()


def close_database():
    """Schließt Engine und Sessions (wichtig für Tests, damit SQLite-Dateien gelöscht werden können)."""
    global engine, SessionLocal
    if engine is not None:
        engine.dispose()
    engine = None
    SessionLocal = None
