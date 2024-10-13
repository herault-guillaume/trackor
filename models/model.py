from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, index=True)
    buy = Column(Float, nullable=True)
    sell = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    minimum = Column(Integer, nullable=True)
    buy_premium = Column(Float, nullable=True)
    sell_premium = Column(Float, nullable=True)
    delivery_fee = Column(Float, nullable=True)
    source = Column(String,nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(pytz.timezone('CET')))
    session_id = Column(UUID(as_uuid=True))
    bullion_type = Column(String,nullable=True)

class MetalPrice(Base):
    __tablename__ = 'metal_price'
    id = Column(Integer, primary_key=True)
    buy_price = Column(Float,nullable=True)
    sell_price = Column(Float,nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(pytz.timezone('CET')))
    session_id = Column(UUID(as_uuid=True))
    bullion_type = Column(String,nullable=True)

poids_pieces  = {
                        'or - 1 ducat': 3.44,
                        'or - 1 oz' : 31.103,
                        'or - 1 oz buffalo': 31.103,
                        'or - 1 oz krugerrand': 31.103,# -> CPor
                        'or - 1 oz nugget / kangourou': 31.103,
                        'or - 1 oz philharmonique': 31.103,
                        'or - 1 oz britannia' : 31.103,
                        'or - 1 oz dragon chinois 2024' : 31.103,
                        'or - 1 oz kangourou 2024' : 31.103,
                        'or - 1 oz cygne 2024' : 31.103,
                        'or - 1 oz dragon et koï 2024' : 31.103,
                        'or - 1 oz 125e anniv perth mint 2024' : 31.103,
                        'or - 1 oz koala 2024 RAM' : 31.103,
                        'or - 1 oz dragon 2024 lunar III' : 31.103,
                        'or - 1 oz dragon chinois 2018' : 31.103,
                        'or - 1 oz dragon chinois 2022' : 31.103,
                        'or - 1 oz dragon chinois 2023' : 31.103,
                        'or - 1 oz dragon tudor beasts 2024' : 31.103,
                        'or - 1 oz st george et le dragon 2024' : 31.103,
                        'or - 1 oz britannia 2022' : 31.103,
                        'or - 1 oz buffalo 2024' : 31.103,
                        'or - 1 oz american eagle' : 31.103,
                        'or - 1 oz britannia 2024' : 31.103,
                        'or - 1 oz maple leaf 2024' : 31.103,
                        'or - 1 oz maple leaf' : 31.103,
                        'or - 1 oz philharmonique 2024' : 31.103,
                        "or - 1 oz lion d'angleterre tudor beasts 2022" : 31.103,
                        'or - 1 oz beowulf et grendel mythes et légendes 2024' : 31.103,
                        'or - 1 oz britannia et liberty 2024' : 31.103,
                        'or - 1 oz lion et aigle 2024' : 31.103,
                        'or - 1 oz bond of the 1970s 2024' : 31.103,
                        'or - 1 oz bond of the 1960s 2024' : 31.103,
                        'or - 1 oz licorne de seymour tudor beasts 2024' : 31.103,
                        'or - 1 oz morgan le fay mythes et légendes 2024' : 31.103,
                        'or - 1 oz the royal arms 2023' : 31.103,
                        'or - 1 oz cygne 2017' : 31.103,
                        'or - 1 oz britannia elizabeth II 2023' : 31.103,
                        'or - 1 oz taureau de clarence tudor beasts 2023' : 31.103,
                        'or - 1 oz serpent 2025 lunar III' : 31.103,
                        'or - 1 rand sud-africains': 3.648,
                        'or - 1/10 oz': 3.11,
                        'or - 1/10 oz philharmonique': 3.11,
                        'or - 1/10 oz american eagle': 3.11,
                        'or - 1/10 oz krugerrand': 3.11,
                        'or - 1/10 oz maple leaf': 3.11,
                        'or - 1/10 oz nugget / kangourou': 3.11,
                        'or - 1/10 oz kangourou 2024': 3.11,
                        'or - 1/10 oz kookaburra 2024': 3.11,
                        'or - 1/10 oz dragon 2024 lunar III': 3.11,
                        'or - 1/10 oz chien 2018 Lunar II': 3.11,
                        'or - 1/10 oz lapin 2023 lunar III': 3.11,
                        'or - 1/10 oz britannia 2024': 3.11,
                        'or - 1/10 oz britannia': 3.11,
                        'or - 1/10 oz britannia charles III 2023': 3.11,
                        'or - 1/10 oz american eagle 2024': 3.11,
                        'or - 1/10 oz couronnement charles III 2023': 3.11,
                        'or - 1/2 oz': 15.552,
                        'or - 1/2 oz american eagle': 15.552,
                        'or - 1/2 oz krugerrand': 15.55,
                        'or - 1/2 oz maple leaf': 15.552,
                        'or - 1/2 oz nugget / kangourou': 15.552,
                        'or - 1/2 oz kangourou 2024': 15.552,
                        'or - 1/2 oz dragon 2024 lunar III': 15.552,
                        'or - 1/2 oz lapin 2023 lunar III': 15.552,
                        'or - 1/2 oz american eagle 2024': 15.552,  # -> CPor
                        'or - 1/2 oz britannia 2024': 15.552,
                        'or - 1/2 oz britannia': 15.552,
                        'or - 1/2 oz philharmonique 2024': 15.552,
                        'or - 1/2 oz philharmonique': 15.552,
                        'or - 1/2 souverain': 3.661, # -> CPor
                        'or - 1/2 souverain georges V': 3.661, # -> CPor
                        'or - 1/2 souverain victoria': 3.661, # -> CPor
                        'or - 1/10 oz koala 2023': 3.11, # -> CPor
                        'or - 1/20 oz': 1.55,
                        'or - 1/20 oz nugget / kangourou': 1.55,
                        'or - 1/20 oz dragon 2024 lunar III': 1.55,
                        'or - 1/20 oz lapin 2023 lunar III': 1.55,
                        'or - 1/20 oz boeuf 2021 Lunar III': 1.55,
                        'or - 1/4 oz': 7.776,
                        'or - 1/4 oz american eagle': 7.776,
                        'or - 1/4 oz krugerrand': 7.776,
                        'or - 1/4 oz maple leaf': 7.776,
                        'or - 1/4 oz nugget / kangourou': 7.776,
                        'or - 1/4 oz kangourou 2024': 7.776,
                        'or - 1/4 oz dragon 2024 lunar III': 7.776,
                        'or - 1/4 oz lapin 2023 lunar III': 7.776,
                        'or - 1/4 oz tigre 2022 lunar III': 7.776,
                        'or - 1/4 oz dragon tudor beasts 2024': 7.776,
                        'or - 1/4 oz st george et le dragon 2024': 7.776,
                        'or - 1/4 oz britannia 2024': 7.776,
                        'or - 1/4 oz britannia': 7.776,
                        'or - 1/4 oz american eagle 2024': 7.776,
                        'or - 1/4 oz souris 2020 Lunar III': 7.776,
                        'or - 1/4 oz britannia charles III 2023': 7.776,
                        'or - 1/4 oz couronnement charles III 2023': 7.776,
                        'or - 1/4 oz philharmonique': 7.776,
                        'or - 1/4 oz éale de beaufort tudor beasts 2023': 7.776,
                        "or - 1/4 oz lion d'angleterre tudor beasts 2022": 7.776,
                        'or - 10 couronnes françois joseph I': 3.096,
                        'or - 10 dollars liberté': 15.047,
                        'or - 10 dollars tête indien': 15.047,
                        'or - 10 florins': 6.056, # -> CPor
                        'or - 10 florins wilhelmina': 6.056, # -> CPor
                        'or - 10 florins willem III': 6.056, # -> CPor
                        'or - 10 francs fr': 2.903, # -> CPor
                        'or - 10 francs fr coq marianne': 2.903, # -> CPor
                        'or - 10 francs fr cérès 1850-1851': 2.903,
                        'or - 10 francs fr napoléon III': 2.903,
                        'or - 10 francs fr napoléon III laurée': 2.903,
                        'or - 10 francs sui vreneli croix': 2.903,
                        'or - 10 pesos': 7.5,
                        'or - 10 lire vittorio emanuele II': 2.898,
                        'or - 100 couronnes françois joseph I': 30.483,
                        'or - 100 francs fr': 29.02,
                        'or - 100 francs fr napoléon III tête nue': 29.02,
                        'or - 100 francs fr napoléon III tête laurée': 29.02,
                        'or - 100 francs fr génie DPF': 29.02,
                        'or - 100 francs fr génie LEF': 29.02,
                        'or - 100 piastres turc': 6.61,
                        'or - 2.5 pesos': 1.872,
                        'or - 2 pesos': 1.494,
                        'or - 20 couronnes': 6.093,
                        'or - 20 dollars': 30.096, # -> CPor
                        'or - 20 dollars tete indien': 30.096, # -> CPor
                        'or - 20 dollars liberté longacre': 30.096, # -> CPor
                        'or - 20 dollars liberté st gaudens': 30.096, # -> CPor
                        'or - 20 francs fr': 5.805, # -> CPor
                        'or - 20 francs fr coq marianne': 5.805, # -> CPor
                        'or - 20 francs fr coq marianne refrappe pinay': 5.805, # -> CPor
                        'or - 20 francs fr cérès': 5.805, # -> CPor
                        'or - 20 francs fr génie debout': 5.805,
                        'or - 20 francs sui confederatio': 5.805, # -> CPor
                        'or - 20 francs bel leopold I': 5.805, # -> CPor
                        'or - 20 francs bel leopold II': 5.805, # -> CPor
                        'or - 20 francs bel albert I': 5.805, # -> CPor
                        'or - 20 francs bel albert I': 5.805, # -> CPor
                        'or - 20 francs fr louis XVIII buste nu': 5.805, # -> CPor
                        'or - 20 francs fr charles X': 5.805, # -> CPor
                        'or - 20 francs fr louis XVIII buste habillé': 5.805, # -> CPor
                        'or - 20 francs fr louis philippe laurée': 5.805, # -> CPor
                        'or - 20 francs fr napoléon empereur': 5.805, # -> CPor
                        'or - 20 francs fr napoléon empereur nue': 5.805, # -> CPor
                        'or - 20 francs fr napoléon empereur laurée': 5.805, # -> CPor
                        'or - 20 francs fr louis-napoléon bonaparte': 5.805, # -> CPor
                        'or - 20 francs fr napoléon III': 5.805, # -> CPor
                        'or - 20 francs tunisie': 5.805, # -> CPor
                        'or - 20 francs union latine': 5.805, # -> CPor
                        'or - 20 francs sui': 5.805, # -> CPor
                        'or - 20 francs sui vreneli croix': 5.805, # -> CPor
                        'or - 20 francs sui vreneli croix 1935L': 5.805, # -> CPor
                        'or - 20 francs fr louis philippe I nu': 5.805, # -> CPor
                        'or - 20 lire umberto I': 5.805,
                        'or - 20 lire vittorio emanuele II': 5.805,
                        'or - 20 mark': 7.168, # -> CPor
                        'or - 20 mark wilhelm II': 7.168, # -> CPor
                        'or - 20 pesos': 15.0,
                        'or - 4 ducats': 13.78,
                        'or - 4 florins 10 francs 1892 refrappe': 2.9,
                        'or - 40 francs fr': 11.61,
                        'or - 40 francs fr napoléon empereur laurée': 11.61,
                        'or - 40 francs fr napoléon empereur non laurée': 11.61,
                        'or - 40 francs fr napoléon premier consul': 11.61,
                        'or - 40 francs fr louis XVIII': 11.61,
                        'or - 40 francs fr louis philippe': 11.61,
                        'or - 40 francs fr charles X': 11.61,
                        'or - 40 francs fr louis philippe': 11.61,
                        'or - 5 dollars liberté': 7.523, # -> CPor
                        'or - 5 dollars tête indien': 7.523, # -> CPor
                        'or - 2.5 dollars liberté': 3.762, # -> CPor
                        'or - 2.5 dollars tête indien': 3.762, # -> CPor
                        'or - 5 dollars liberté': 7.523, # -> CPor
                        'or - 5 francs fr napoléon III': 1.452,
                        'or - 5 francs fr napoléon III nue': 1.452,
                        'or - 5 pesos': 3.75,
                        'or - 5 roubles': 3.87,
                        'or - 50 francs fr napoléon III tête nue': 14.51,
                        'or - 50 francs fr napoléon III tête laurée': 14.51,
                        'or - 50 pesos': 37.5, # -> CPor
                        'or - 50 écus charles quint': 15.552,
                        'or - 8 florins 20 francs franz joseph I': 5.805,
                        'or - 500 yuan panda 2010 1 oz': 31.103,
                        'or - 500 yuan panda 2024 30g': 30.0,
                        'or - 200 yuan panda 2024 15g': 15.0,
                        'or - 200 yuan panda 2010 1/2 oz': 15.552,
                        'or - 100 yuan panda 2024 8g': 8.0,
                        'or - 100 yuan panda 2010 1/4 oz': 7.776,
                        'or - 50 yuan panda 2024 3g': 3.0,
                        'or - 50 yuan panda 2010 1/10 oz': 3.11,
                        'or - 50 yuan panda 2012 1/10 oz': 3.11,
                        'or - 20 yuan panda 2010 1/20 oz': 1.55,
                        'or - 10 yuan panda 2024 1g': 1.0,
                        'or - lingot 1 g': 1.0,
                        'or - lingot 1 kg LBMA': 1000.0,
                        'or - lingot 1 once LBMA': 31.103,
                        'or - lingot 10 g LBMA': 10.0,
                        'or - lingot 100 g LBMA': 100.0,
                        'or - lingot 20 g LBMA': 20.0,
                        'or - lingot 250 g LBMA': 250.0,
                        'or - lingot 5 g LBMA': 5.0,
                        'or - lingot 50 g LBMA': 50.0,
                        'or - lingot 500 g LBMA': 500.0,
                        'or - 1 souverain': 7.318, # -> CPor
                        'or - 1 souverain edouart VII': 7.318, # -> CPor
                        'or - 1 souverain elizabeth II': 7.318, # -> CPor
                        'or - 1 souverain georges V': 7.318, # -> CPor
                        'or - 1 souverain victoria jubilee': 7.318, # -> CPor
                        'or - 1 souverain 2024 charles III': 7.318, # -> CPor
                        'or - 1 souverain 2023 charles III': 7.318, # -> CPor
                        'or - 1 souverain 2022 charles III': 7.318, # -> CPor
                        'or - 1/2 souverain 2024 charles III': 3.6612, # -> CPor
                        'or - 1/2 souverain 2023 charles III': 3.6612, # -> CPor
                        'or - 1/2 souverain 2022 charles III': 3.6612, # -> CPor
                        'or - 1/2 souverain edouard VII': 3.6612, # -> CPor
                        'or - 1/4 souverain 2024 charles III': 1.83, # -> CPor
                        'or - 2 souverain 2024 charles III': 14.64, # -> CPor
                        'or - 2 souverain 2022 charles III': 14.64, # -> CPor

                        # Argent
                        'ar - lingot 5 kg' : 1000.0,
                        'ar - 50 francs fr hercule (1974-1980)': 30.0 * 0.900,
                        'ar - 10 francs fr hercule (1965-1973)': 10.0 * 0.900,
                        'ar - 5 francs fr semeuse (1959-1969)': 12.0 * 0.835,
                        'ar - 2 francs fr semeuse': 10.0 * 0.835,
                        'ar - 1 franc fr semeuse': 5 * 0.835,
                        'ar - 50 centimes francs fr semeuse': 2.5 * 0.835,
                        'ar - 100 francs fr génie (1878-1914)': 32.258 * 0.900,
                        'ar - 100 francs fr panthéon': 15.0 * 0.900,
                        'ar - 100 francs fr': 15.0 * 0.900,
                        'ar - 20 francs fr turin (1860-1928)': 20.0 * 0.680,
                        'ar - 20 francs fr turin (1929-1939)': 20.0 * 0.680,
                        'ar - 10 francs fr turin (1860-1928)': 10.0 * 0.680,
                        'ar - 5 francs fr ecu (1854-1860)' : 25.0 * 0.900,
                        'ar - 1 oz  fr ecu (1854-1860)': 25.0 * 0.900,
                        'ar - 1 oz' : 31.103,
                        'ar - 1 oz buffalo': 31.103,
                        'ar - 1 oz krugerrand': 31.103,
                        'ar - 1 oz nugget / kangourou': 31.103,
                        'ar - 1 oz philharmonique': 31.103,
                        'ar - 1 oz britannia' : 31.103,
                        'ar - 1 oz dragon chinois 2024' : 31.103,
                        'ar - 1 oz kangourou 2024' : 31.103,
                        'ar - 1 oz cygne 2024' : 31.103,
                        'ar - 1 oz dragon et koï 2024' : 31.103,
                        'ar - 1 oz 125e anniv perth mint 2024' : 31.103,
                        'ar - 1 oz koala 2024 RAM' : 31.103,
                        'ar - 1 oz dragon 2024 lunar III' : 31.103,
                        'ar - 1 oz dragon chinois 2018' : 31.103,
                        'ar - 1 oz dragon chinois 2022' : 31.103,
                        'ar - 1 oz dragon chinois 2023' : 31.103,
                        'ar - 1 oz dragon tudor beasts 2024' : 31.103,
                        'ar - 1 oz st george et le dragon 2024' : 31.103,
                        'ar - 1 oz britannia 2022' : 31.103,
                        'ar - 1 oz buffalo 2024' : 31.103,
                        'ar - 1 oz american eagle' : 31.103,
                        'ar - 1 oz britannia 2024' : 31.103,
                        'ar - 1 oz maple leaf 2024' : 31.103,
                        'ar - 1 oz maple leaf' : 31.103,
                        'ar - 1 oz silver eagle' : 31.103,
                    }

# Configuration de la base de données
engine = create_engine(r'sqlite:///C:\Users\Guillaume Hérault\PycharmProjects\trackor\models\pieces_or.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)