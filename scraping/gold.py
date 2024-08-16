import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice
from price_parser import Price
from models.model import CoinPrice

from price_parser import Price
import traceback

coin_name_to_map = {
    "20 $ US" :  '20 dollars or liberté',
    "10 $ US" : '10 dollars or liberté',
    "5 $ US" :'5 dollars or liberté',
    "Napoléon 20 Frs (Louis d'Or)" : '20 francs or coq marianne',
    "Croix Suisse 20 Frs": '10 francs or vreneli croix suisse',
    "50 Pesos": "50 pesos or",
    "Krugerrand": '1 oz krugerrand',
    "Souverain George V": 'souverain or georges V',
    "Elisabeth II": 'souverain or elizabeth II',
    "Demi Napoléon / 10 Frs Napoléon": '10 francs or coq marianne',
    "Demi Souverain": '1/2 souverain victoria',
    "10 Florins":'10 florins or wilhelmina', # ou '10 florins or willem III'
    "20 Frs Tunisie": '20 francs or tunisie',
    "Union Latine": '20 francs or union latine léopold II',
    "Reichsmark": '20 mark or wilhelm II',
    # non côté
}

def get_delivery_price(price):
    pass
#https://www.gold.fr/informations-sur-l-or/nous-connaitre/conditions-generales-dutilisation#frais-et-commissions

def get_price_for(session, session_id):
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
                    print(price,name)
                    coin = CoinPrice(nom=name,
                                     j_achete=price.amount_float,
                                     source=url,
                                     frais_port=30.0,
                                     session_id=session_id)
                    session.add(coin)
                    session.commit()

            except Exception as e:
                print(traceback.format_exc())



