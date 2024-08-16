from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class CoinPrice(Base):
    __tablename__ = 'coin_price'

    id = Column(Integer, primary_key=True)
    nom = Column(String,nullable=True,index=True)
    j_achete = Column(Float,nullable=True)
    je_vend = Column(Float,nullable=True)
    cotation_francaise = Column(Float,nullable=True)
    prime_achat_vendeur = Column(Float,nullable=True)
    prime_vente_vendeur = Column(Float,nullable=True)
    prime_achat_perso = Column(Float,nullable=True)
    prime_vente_perso = Column(Float,nullable=True)
    frais_port = Column(Float,nullable=True)
    source = Column(String,nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(UUID(as_uuid=True))

class GoldPrice(Base):
    __tablename__ = 'gold_price'
    id = Column(Integer, primary_key=True)
    buy_price = Column(Float,nullable=True)
    sell_price = Column(Float,nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

poids_pieces_or  = {
                        '1 ducat or': 3.44,
                        '1 oz american eagle': 31.103,
                        '1 oz buffalo': 31.103,
                        '1 oz krugerrand': 31.103,
                        '1 oz maple leaf': 31.103,
                        '1 oz nugget / kangourou': 31.103,
                        '1 oz philharmonique': 31.103,
                        '1 oz britannia' : 31.103,
                        '1/10 oz american eagle': 3.11,
                        '1/10 oz krugerrand': 3.054,
                        '1/10 oz maple leaf': 3.11,
                        '1/10 oz nugget / kangourou': 3.11,
                        '1/2 oz american eagle': 15.552,
                        '1/2 oz krugerrand': 15.269,
                        '1/2 oz maple leaf': 15.552,
                        '1/2 oz nugget / kangourou': 15.552,
                        '1/2 souverain georges V': 3.661,
                        '1/2 souverain victoria': 3.661,
                        '1/20 oz nugget / kangourou': 1.55,
                        '1/4 oz american eagle': 7.776,
                        '1/4 oz krugerrand': 7.634,
                        '1/4 oz maple leaf': 7.776,
                        '1/4 oz nugget / kangourou': 7.776,
                        '10 couronnes or françois joseph I': 3.096,
                        '10 dollars or liberté': 15.047,
                        '10 dollars or tête indien': 15.047,
                        '10 florins or wilhelmina': 6.056,
                        '10 florins or willem III': 6.056,
                        '10 francs or coq marianne': 2.903,
                        '10 francs or cérès 1850-1851': 2.903,
                        '10 francs or napoléon III': 2.903,
                        '10 francs or vreneli croix suisse': 2.903,
                        '10 pesos or': 7.5,
                        '100 couronnes or françois joseph I': 30.483,
                        '100 francs or napoléon III tête nue': 29.02,
                        '2 1/2 pesos or': 1.872,
                        '20 couronnes or françois joseph I': 6.093,
                        '20 dollars or liberté': 30.093,
                        '20 francs or coq marianne': 5.805,
                        '20 francs or cérès': 5.805,
                        '20 francs or génie debout': 5.805,
                        '20 francs or helvetia suisse': 5.805,
                        '20 francs or leopold I': 5.805,
                        '20 francs or napoléon III': 5.805,
                        '20 francs or tunisie': 5.805,
                        '20 francs or union latine léopold II': 5.805,
                        '20 francs or vreneli croix suisse': 5.805,
                        '20 lire or umberto I': 5.805,
                        '20 lire or vittorio emanuele II': 5.805,
                        '20 mark or wilhelm II': 7.168,
                        '20 pesos or': 15.0,
                        '4 ducats or': 13.78,
                        '4 florins 10 francs 1892 refrappe': 2.9,
                        '40 francs or napoléon empereur lauré': 11.61,
                        '5 dollars or liberté': 7.523,
                        '5 dollars or tête indien': 7.523,
                        '5 francs or napoléon III': 1.452,
                        '5 pesos or': 3.75,
                        '50 francs or napoléon III tête nue': 14.51,
                        '50 pesos or': 37.5,
                        '50 écus or charles quint': 15.552,
                        '8 florins 20 francs or franz joseph I': 5.805,
                        'Lingot or 1 g': 1.0,
                        'Lingot or 1 kg LBMA': 1000.0,
                        'Lingot or 1 once LBMA': 31.103,
                        'Lingot or 10 g LBMA': 10.0,
                        'Lingot or 100 g LBMA': 100.0,
                        'Lingot or 20 g LBMA': 20.0,
                        'Lingot or 250 g LBMA': 250.0,
                        'Lingot or 5 g LBMA': 5.0,
                        'Lingot or 50 g LBMA': 50.0,
                        'Lingot or 500 g LBMA': 500.0,
                        'souverain or edouart VII': 7.318,
                        'souverain or elizabeth II': 7.318,
                        'souverain or georges V': 7.318,
                        'souverain or victoria jubilee': 7.318
                    }


# Configuration de la base de données
engine = create_engine('sqlite:///pieces_or.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)