from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class GoldData(Base):
    __tablename__ = 'gold_data'

    id = Column(Integer, primary_key=True)
    nom = Column(String,nullable=True,index=True)
    j_achete = Column(Float,nullable=True)
    je_vend = Column(Float,nullable=True)
    cotation_francaise = Column(Float,nullable=True)
    prime_achat_vendeur = Column(Float,nullable=True)
    prime_vente_vendeur = Column(Float,nullable=True)
    prime_achat_perso = Column(Float,nullable=True)
    prime_vente_perso = Column(Float,nullable=True)
    source = Column(String,nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Configuration de la base de données
engine = create_engine('sqlite:///pieces_or.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)