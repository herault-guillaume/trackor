from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

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
    timestamp = Column(DateTime, default=lambda: datetime.now(pytz.timezone('CET')))
    session_id = Column(UUID(as_uuid=True))
    metal = Column(String,nullable=True)

class MetalPrice(Base):
    __tablename__ = 'metal_price'
    id = Column(Integer, primary_key=True)
    buy_price = Column(Float,nullable=True)
    sell_price = Column(Float,nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(pytz.timezone('CET')))
    session_id = Column(UUID(as_uuid=True))
    metal = Column(String,nullable=True)

poids_pieces_or  = {
                        '1 ducat or': 3.44,
                        '1 oz' : 31.103,
                        '1 oz buffalo': 31.103,
                        '1 oz krugerrand': 31.103,# -> CPor
                        '1 oz nugget / kangourou': 31.103,
                        '1 oz philharmonique': 31.103,
                        '1 oz philharmonique': 31.103,
                        '1 oz britannia' : 31.103,
                        '1 oz dragon chinois 2024' : 31.103,
                        '1 oz kangourou 2024' : 31.103,
                        '1 oz cygne 2024' : 31.103,
                        '1 oz dragon et koï 2024' : 31.103,
                        '1 oz 125e anniv perth mint 2024' : 31.103,
                        '1 oz koala 2024 RAM' : 31.103,
                        '1 oz dragon 2024 lunar III' : 31.103,
                        '1 oz dragon chinois 2018' : 31.103,
                        '1 oz dragon chinois 2022' : 31.103,
                        '1 oz dragon chinois 2023' : 31.103,
                        '1 oz dragon tudor beasts 2024' : 31.103,
                        '1 oz st george et le dragon 2024' : 31.103,
                        '1 oz britannia 2022' : 31.103,
                        '1 oz buffalo 2024' : 31.103,
                        '1 oz american eagle' : 31.103,
                        '1 oz britannia 2024' : 31.103,
                        '1 oz maple leaf 2024' : 31.103,
                        '1 oz maple leaf' : 31.103,
                        '1 oz philharmonique 2024' : 31.103,
                        "1 oz lion d'angleterre tudor beasts 2022" : 31.103,
                        '1 oz beowulf et grendel mythes et légendes 2024' : 31.103,
                        '1 oz britannia et liberty 2024' : 31.103,
                        '1 oz lion et aigle 2024' : 31.103,
                        '1 oz bond of the 1970s 2024' : 31.103,
                        '1 oz bond of the 1960s 2024' : 31.103,
                        '1 oz licorne de seymour tudor beasts 2024' : 31.103,
                        '1 oz morgan le fay mythes et légendes 2024' : 31.103,
                        '1 oz the royal arms 2023' : 31.103,
                        '1 oz cygne 2017' : 31.103,
                        '1 oz britannia elizabeth II 2023' : 31.103,
                        '1 oz taureau de clarence tudor beasts 2023' : 31.103,
                        '1 oz serpent 2025 lunar III' : 31.103,
                        '1 rand sud-africains or': 3.648,
                        '1/10 oz': 3.11,
                        '1/10 oz philharmonique': 3.11,
                        '1/10 oz american eagle': 3.11,
                        '1/10 oz krugerrand': 3.11,
                        '1/10 oz maple leaf': 3.11,
                        '1/10 oz nugget / kangourou': 3.11,
                        '1/10 oz kangourou 2024': 3.11,
                        '1/10 oz kookaburra 2024': 3.11,
                        '1/10 oz dragon 2024 lunar III': 3.11,
                        '1/10 oz chien 2018 Lunar II': 3.11,
                        '1/10 oz lapin 2023 lunar III': 3.11,
                        '1/10 oz britannia 2024': 3.11,
                        '1/10 oz britannia charles III 2023': 3.11,
                        '1/10 oz american eagle 2024': 3.11,
                        '1/10 oz couronnement charles III 2023': 3.11,
                        '1/2 oz': 15.552,
                        '1/2 oz american eagle': 15.552,
                        '1/2 oz krugerrand': 15.55,
                        '1/2 oz maple leaf': 15.552,
                        '1/2 oz nugget / kangourou': 15.552,
                        '1/2 oz kangourou 2024': 15.552,
                        '1/2 oz dragon 2024 lunar III': 15.552,
                        '1/2 oz lapin 2023 lunar III': 15.552,
                        '1/2 oz american eagle 2024': 15.552,  # -> CPor
                        '1/2 oz britannia 2024': 15.552,
                        '1/2 oz philharmonique 2024': 15.552,
                        '1/2 souverain or': 3.661, # -> CPor
                        '1/2 souverain or georges V': 3.661, # -> CPor
                        '1/2 souverain or victoria': 3.661, # -> CPor
                        '1/10 oz koala 2023': 3.11, # -> CPor
                        '1/20 oz': 1.55,
                        '1/20 oz nugget / kangourou': 1.55,
                        '1/20 oz dragon 2024 lunar III': 1.55,
                        '1/20 oz lapin 2023 lunar III': 1.55,
                        '1/20 oz boeuf 2021 Lunar III': 1.55,
                        '1/4 oz': 7.776,
                        '1/4 oz american eagle': 7.776,
                        '1/4 oz krugerrand': 7.776,
                        '1/4 oz maple leaf': 7.776,
                        '1/4 oz nugget / kangourou': 7.776,
                        '1/4 oz kangourou 2024': 7.776,
                        '1/4 oz dragon 2024 lunar III': 7.776,
                        '1/4 oz lapin 2023 lunar III': 7.776,
                        '1/4 oz tigre 2022 lunar III': 7.776,
                        '1/4 oz dragon tudor beasts 2024': 7.776,
                        '1/4 oz st george et le dragon 2024': 7.776,
                        '1/4 oz britannia 2024': 7.776,
                        '1/4 oz american eagle 2024': 7.776,
                        '1/4 oz souris 2020 Lunar III': 7.776,
                        '1/4 oz britannia charles III 2023': 7.776,
                        '1/4 oz couronnement charles III 2023': 7.776,
                        '1/4 oz philharmonique': 7.776,
                        '1/4 oz éale de beaufort tudor beasts 2023': 7.776,
                        "1/4 oz lion d'angleterre tudor beasts 2022": 7.776,
                        '10 couronnes or françois joseph I': 3.096,
                        '10 dollars or liberté': 15.047,
                        '10 dollars or tête indien': 15.047,
                        '10 florins or': 6.056, # -> CPor
                        '10 florins or wilhelmina': 6.056, # -> CPor
                        '10 florins or willem III': 6.056, # -> CPor
                        '10 francs or fr': 2.903, # -> CPor
                        '10 francs or fr coq marianne': 2.903, # -> CPor
                        '10 francs or fr cérès 1850-1851': 2.903,
                        '10 francs or fr napoléon III': 2.903,
                        '10 francs or fr napoléon III laurée': 2.903,
                        '10 francs or sui vreneli croix suisse': 2.903,
                        '10 pesos or': 7.5,
                        '10 lire or vittorio emanuele II': 2.898,
                        '100 couronnes or françois joseph I': 30.483,
                        '100 francs or fr': 29.02,
                        '100 francs or fr napoléon III tête nue': 29.02,
                        '100 francs or fr napoléon III tête laurée': 29.02,
                        '100 francs or fr génie DPF': 29.02,
                        '100 francs or fr génie LEF': 29.02,
                        '100 piastres or': 6.61,
                        '2 1/2 pesos or': 1.872,
                        '2 pesos or': 1.494,
                        '20 couronnes or françois joseph I': 6.093,
                        '20 dollars or': 30.096, # -> CPor
                        '20 dollars or tete indien': 30.096, # -> CPor
                        '20 dollars or liberté longacre': 30.096, # -> CPor
                        '20 dollars or liberté st gaudens': 30.096, # -> CPor
                        '20 francs or fr': 5.805, # -> CPor
                        '20 francs or fr coq marianne': 5.805, # -> CPor
                        '20 francs or fr coq marianne refrappe pinay': 5.805, # -> CPor
                        '20 francs or fr cérès': 5.805, # -> CPor
                        '20 francs or fr génie debout': 5.805,
                        '20 francs or sui confederatio suisse': 5.805, # -> CPor
                        '20 francs or bel leopold I': 5.805, # -> CPor
                        '20 francs or bel leopold II': 5.805, # -> CPor
                        '20 francs or bel albert I': 5.805, # -> CPor
                        '20 francs or fr louis XVIII buste nu': 5.805, # -> CPor
                        '20 francs or fr charles X': 5.805, # -> CPor
                        '20 francs or fr louis XVIII buste habillé': 5.805, # -> CPor
                        '20 francs or fr louis philippe laurée': 5.805, # -> CPor
                        '20 francs or fr napoléon empereur': 5.805, # -> CPor
                        '20 francs or fr napoléon empereur nue': 5.805, # -> CPor
                        '20 francs or fr napoléon empereur laurée': 5.805, # -> CPor
                        '20 francs or fr louis-napoléon bonaparte': 5.805, # -> CPor
                        '20 francs or fr napoléon III': 5.805, # -> CPor
                        '20 francs or tunisie': 5.805, # -> CPor
                        '20 francs or union latine': 5.805, # -> CPor
                        '20 francs or sui': 5.805, # -> CPor
                        '20 francs or sui vreneli croix': 5.805, # -> CPor
                        '20 francs or sui vreneli croix 1935L': 5.805, # -> CPor
                        '20 francs or fr louis philippe I nu': 5.805, # -> CPor
                        '20 lire or umberto I': 5.805,
                        '20 lire or vittorio emanuele II': 5.805,
                        '20 mark or': 7.168, # -> CPor
                        '20 mark or wilhelm II': 7.168, # -> CPor
                        '20 pesos or': 15.0,
                        '4 ducats or': 13.78,
                        '4 florins 10 francs 1892 refrappe': 2.9,
                        '40 francs or fr': 11.61,
                        '40 francs or fr napoléon empereur laurée': 11.61,
                        '40 francs or fr napoléon empereur non laurée': 11.61,
                        '40 francs or fr napoléon premier consul': 11.61,
                        '40 francs or fr louis XVIII': 11.61,
                        '40 francs or fr ouis philippe': 11.61,
                        '40 francs or fr charles X': 11.61,
                        '40 francs or fr louis philippe': 11.61,
                        '5 dollars or liberté': 7.523, # -> CPor
                        '5 dollars or tête indien': 7.523, # -> CPor
                        '2.5 dollars or tête liberté': 3.762, # -> CPor
                        '2.5 dollars or tête indien': 3.762, # -> CPor
                        '5 dollars or liberté': 7.523, # -> CPor
                        '5 francs or fr napoléon III': 1.452,
                        '5 francs or fr napoléon III nue': 1.452,
                        '5 pesos or': 3.75,
                        '5 roubles or': 3.87,
                        '50 francs or fr napoléon III tête nue': 14.51,
                        '50 francs or fr napoléon III tête laurée': 14.51,
                        '50 pesos or': 37.5, # -> CPor
                        '50 écus or charles quint': 15.552,
                        '8 florins 20 francs or franz joseph I': 5.805,
                        '500 yuan panda 2010 1 oz': 31.103,
                        '500 yuan panda 2024 30g': 30.0,
                        '200 yuan panda 2024 15g': 15.0,
                        '200 yuan panda 2010 1/2 oz': 15.552,
                        '100 yuan panda 2024 8g': 8.0,
                        '100 yuan panda 2010 1/4 oz': 7.776,
                        '50 yuan panda 2024 3g': 3.0,
                        '50 yuan panda 2010 1/10 oz': 3.11,
                        '50 yuan panda 2012 1/10 oz': 3.11,
                        '20 yuan panda 2010 1/20 oz': 1.55,
                        '10 yuan panda 2024 1g': 1.0,
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
                        'souverain or': 7.318, # -> CPor
                        'souverain or edouart VII': 7.318, # -> CPor
                        'souverain or elizabeth II': 7.318, # -> CPor
                        'souverain or georges V': 7.318, # -> CPor
                        'souverain or victoria jubilee': 7.318, # -> CPor
                        'souverain or 2024 charles III': 7.318, # -> CPor
                        'souverain or 2023 charles III': 7.318, # -> CPor
                        'souverain or 2022 charles III': 7.318, # -> CPor
                        'demi souverain or 2024 charles III': 3.6612, # -> CPor
                        'demi souverain or 2023 charles III': 3.6612, # -> CPor
                        'demi souverain or 2022 charles III': 3.6612, # -> CPor
                        '1/4 souverain or 2024 charles III': 1.83, # -> CPor
                        'double souverain or 2024 charles III': 14.64, # -> CPor
                        'double souverain or 2022 charles III': 14.64, # -> CPor
                    }

poids_pieces_argent = {
                        # France
                        '50 Francs Argent Hercule (1974-1980)': 30.0 * 0.900,  
                        '10 Francs Argent Hercule (1965-1973)': 10.0 * 0.900,
                        '5 Francs Argent Semeuse (différentes années)': 12.0 * 0.835,
                        '2 Francs Argent Semeuse (différentes années)': 10.0 * 0.835,
                        '1 Franc Argent Semeuse (différentes années)': 5 * 0.835,
                        '50 Centimes Argent Semeuse (différentes années)': 2.5 * 0.835,
                        '100 Francs Argent Génie (1878-1914)': 32.258 * 0.900,  
                        '100 Francs Argent Panthéon': 15.0 * 0.900,
                        '20 Francs Argent Turin (1860-1928)': 20.0 * 0.680,
                        '10 Francs Argent Turin (1860-1928)': 10.0 * 0.680,
                        '5 Francs Argent Ecu (1854-1860)': 25.0 * 0.900,

                    }

# Configuration de la base de données
engine = create_engine(r'sqlite:///C:\Users\guillaume.herault\PycharmProjects\trackor\models\pieces_or.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)