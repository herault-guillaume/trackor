import requests
from bs4 import BeautifulSoup
from models.model import Item
from price_parser import Price
from models.model import Item, poids_pieces

from price_parser import Price
import traceback

CMN = {
    "20 $ US" :  'or - 20 dollars',
    "10 $ US" : 'or - 10 dollars liberté',
    "5 $ US" :'or - 5 dollars liberté',
    "Napoléon 20 Frs (Louis d'Or)" : 'or - 20 francs fr coq marianne',
    "Croix Suisse 20 Frs": 'or - 10 francs sui vreneli croix',
    "50 Pesos": "or - 50 pesos mex",
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
    delivery_ranges=[[0,100000.0,30.0],(100000,float('inf'),80.0)]
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_="pricesTable coinsCompleteTable bours")

    for table in tables:
        for row in table.find_all('tr'):
            try:
                name_element = row.find('td', class_="name speak")
                source = url[:-1] + name_element.find('a')['href']
                price_element = row.find('td', class_="price speak")

                if name_element and price_element:
                    name = name_element.text.strip()
                    price = Price.fromstring(price_element.text)
                    print(price,CMN[name],url)

                    item_data = CMN[name]
                    minimum = 1
                    quantity = 1
                    if isinstance(item_data, tuple):
                        name = item_data[0]
                        quantity = item_data[1]
                        bullion_type = item_data[0][:2]
                    else:
                        name = item_data
                        bullion_type = item_data[:2]

                    if bullion_type == 'or':
                        buy_price = buy_price_gold
                    else:
                        buy_price = buy_price_silver

                    price_ranges = [(minimum,999999999,price)]

                    def price_between(value, ranges):
                        """
                        Returns the price per unit for a given quantity.
                        """

                        for min_qty, max_qty, price in ranges:
                            if min_qty <= value <= max_qty:
                                if isinstance(price, Price):
                                    return price.amount_float
                                else:
                                    return price

                    coin = Item(name=name,
                                price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in price_ranges]),
                                buy_premiums=';'.join(
        ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(1,minimum)] +
        ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges)*i,delivery_ranges)/(quantity*i)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(minimum,151)]
                                ),
                                delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                                source=source,
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum)

                    session.add(coin)
                    session.commit()


            except Exception as e:
                print(traceback.format_exc())



