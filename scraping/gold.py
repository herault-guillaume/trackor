import requests
from bs4 import BeautifulSoup
from models.model import Item
from price_parser import Price
from models.model import Item, poids_pieces

from price_parser import Price
import traceback

coin_name_to_map = {
    "20 $ US" :  'or - 20 dollars',
    "10 $ US" : 'or - 10 dollars liberté',
    "5 $ US" :'or - 5 dollars liberté',
    "Napoléon 20 Frs (Louis d'Or)" : 'or - 20 francs fr coq marianne',
    "Croix Suisse 20 Frs": 'or - 10 francs sui vreneli croix',
    "50 Pesos": "or - 50 pesos",
    "Krugerrand": 'or - 1 oz krugerrand',
    "Souverain George V": 'or - 1 souverain georges V',
    'Souverain (toutes effigies)': 'or - 1 souverain georges V',
    "Elisabeth II": 'or - 1 souverain elizabeth II',
    "Demi Napoléon / 10 Frs Napoléon": 'or - 10 francs fr coq marianne',
    "Demi Souverain": 'or - 1/2 souverain victoria',
    '20 francs Or (toutes effigies)': 'or - 20 francs fr',
    'Britannia 1 OZ Or': 'or - 1 oz britannia',
    "10 Florins":'or - 10 florins wilhelmina', # ou 'or - 10 florins willem III'
    "20 Frs Tunisie": 'or - 20 francs tunisie',
    "20 francs Tunisie": 'or - 20 francs tunisie',
    "Union Latine": 'or - 20 francs union latine',
    "Reichsmark": 'or - 20 mark wilhelm II',
    # non côté
}

def get_delivery_price(price):
    pass
#https://www.gold.fr/informations-sur-l-or/nous-connaitre/conditions-generales-dutilisation#frais-et-commissions

def get_price_for(session, session_id,buy_price_gold,buy_price_silver):
    url = "https://www.gold.fr/achat-piece-or/"
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_="pricesTable coinsCompleteTable bours")

    for table in tables:
        for row in table.find_all('tr'):
            try:
                name_element = row.find('td', class_="name speak")
                price_element = row.find('td', class_="price speak")

                if name_element and price_element:
                    name = name_element.text.strip()
                    price = Price.fromstring(price_element.text)
                    print(price,coin_name_to_map[name],url)
                    if coin_name_to_map[name][:2] == 'or':
                        coin = Item(name=coin_name_to_map[name],
                                    buy=price.amount_float,
                                    source=url,
                                    buy_premium=((price.amount_float + 30.0) - (buy_price * poids_pieces[
                                             coin_name_to_map[name]])) * 100.0 / (buy_price * poids_pieces[coin_name_to_map[name]]),

                                    delivery_fee=30.0,
                                    session_id=session_id, bullion_type='g')
                    session.add(coin)
                    session.commit()

            except Exception as e:
                print(traceback.format_exc())



