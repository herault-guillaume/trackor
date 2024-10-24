import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import re

CMN = {
    "20 Francs Napoléon": "or - 20 francs fr",
    "20 Francs Suisse": "or - 20 francs sui vreneli croix",
    "Union Latine": "or - 20 francs union latine",
    "Souverain": "or - 1 souverain elizabeth II",
    "Demi Souverain": "or - 1/2 souverain georges V",
    "50 Pesos": "or - 50 pesos mex",
    "10 Francs Napoléon": "or - 10 francs fr napoléon III",
    "Krugerrand": "or - 1 oz krugerrand",
    "10 Dollars US": "or - 10 dollars liberté",
    "5 Dollars US": "or - 5 dollars liberté",
    "20 Reichsmarks": "or - 20 mark wilhelm II",
    "10 Florins": "or - 10 florins wilhelmina",
    "Maple Leaf Or 1 OZ": "or - 1 oz maple leaf",
    "American Eagle 1 OZ": "or - 1 oz american eagle",
    "Philharmonique 1 OZ": "or - 1 oz philharmonique",
    "American Buffalo 1 OZ": "or - 1 oz buffalo",
    "Nugget 1 OZ": "or - 1 oz nugget / kangourou",
    '20 Dollars US' : 'or - 20 dollars',
    '20 Francs Marianne...' : 'or - 20 francs fr coq marianne',
    '10 Francs Napoléon...' : 'or - 10 francs fr napoléon III',
    'Britannia 1 OZ Or' : 'or - 1 oz britannia',
    'PANDA OR 30 GRAMMES' : 'or - 500 yuan panda',
    'EpargnOr OZ' : 'or - 1 oz EpargnOr',

    "5 Francs semeuse": "ar - 5 francs fr semeuse (1959-1969)",
    "10 Francs Hercule": "ar - 10 francs fr hercule (1965-1973)",
    "2 Francs Semeuse": "ar - 2 francs fr semeuse",
    "1 Franc Semeuse": "ar - 1 franc fr semeuse",
    "50 Cts Semeuse": "ar - 50 centimes francs fr semeuse",
    "Ecu 5 Francs": "ar - 5 francs fr ecu (1854-1860)",
    "100 Francs Argent": "ar - 100 francs fr",
    "20 Francs Turin": "ar - 20 francs fr turin (1929-1939)",
    "10 Francs Turin": "ar - 10 francs fr turin (1860-1928)",
    "SILVER EAGLE 1 OZ": "ar - 1 oz silver eagle",
    "Kangourou 1 OZ Argent": "ar - 1 oz nugget / kangourou",
    "Maple Leaf 1 OZ Ar...": "ar - 1 oz maple leaf",
    "Philharmonique 1 O...": "ar - 1 oz philharmonique",
    "Britannia 1 Oz Argent": "ar - 1 oz britannia",
    "Boite 500 Pièces B...": ("ar - 1 oz britannia", 500),
    "50 Francs Hercule": "ar - 50 francs fr hercule (1974-1980)",
    "PANDA ARGENT 30 GR...": "ar - 10 yuan panda 30g",
}
def get_delivery_price(price):
    #https://www.changerichelieu.fr/livraison
    if price <= 600.0:
        return 10.0
    elif 600.0 < price <= 2500.0 :
        return 20.0
    elif 2500.0 < price <= 5000.0 :
        return 34.0
    elif 5000.0 < price <= 7500.0 :
        return 50.0
    elif 7500.0 < price <= 10000.0 :
        return 56.0
    elif 10000.0 < price <= 15000.0 :
        return 65.0
    else :
        return 0.0

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    urls = ["https://www.changevivienne.com/or","https://www.changevivienne.com/argent"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for url in urls:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        target_divs = soup.find_all('div', class_='cv-table-block cv-table-block-item')

        for div in target_divs:
            try :
                # Extract product name
                product_name_element = div.find('a', class_='product-name product_name_grand')
                product_name = product_name_element.text.strip()
                source = product_name_element['href']
                item_data = CMN[product_name]

                # Extract price
                price_element = div.find('p', class_='price product-price')
                price = Price.fromstring(price_element.text.strip())

                minimum = 1
                min_p = div.find('p', class_='alqty hidden')
                if min_p:
                    minimum = int(re.search(r"\d+", min_p.text).group())

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

                print(price,CMN[product_name], source)

                qty = div.find_all('li',class_='left')
                prices = div.find_all('li',class_='right')

                if len(qty) > 1 and len(prices) > 1:
                    for q,p in zip(qty[1:],prices[1:]):

                        min = int(re.search(r"\d+", q.text).group())
                        if min > minimum:
                            minimum = min

                        coin = Item(name=name,
                                    prices=price.amount_float,
                                    source=source,
                                    buy_premiums=(((price.amount_float + get_delivery_price(
                                        price.amount_float) / minimum) / float(quantity)) - (
                                                         buy_price * poids_pieces[name])) * 100.0 / (
                                                            buy_price * poids_pieces[name]),

                                    delivery_fee=get_delivery_price(price.amount_float*minimum),
                                    session_id=session_id,
                                    bullion_type=bullion_type,
                                    quantity=quantity,
                                    minimum=minimum)

                        session.add(coin)
                        session.commit()

                else :
                    # Extract price
                    price_element = div.find('p', class_='price product-price')
                    price = Price.fromstring(price_element.text.strip())

                    coin = Item(name=name,
                                prices=price.amount_float,
                                source=source,
                                buy_premiums=(((price.amount_float + get_delivery_price(
                                    price.amount_float) / minimum) / float(quantity)) - (
                                                     buy_price * poids_pieces[name])) * 100.0 / (
                                                    buy_price * poids_pieces[name]),

                                delivery_fee=get_delivery_price(price.amount_float*minimum),
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum)

                    session.add(coin)
                    session.commit()



            except Exception as e:
                print(traceback.format_exc())
