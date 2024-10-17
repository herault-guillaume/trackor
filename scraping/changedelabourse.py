import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import re

CMN = {
    "Napoléon Or 20 Francs": "or - 20 francs fr",  # Assuming a standard 20 Francs gold coin
    "50 Pesos": "or - 50 pesos mex",
    "Souverain": "or - 1 souverain",  # Assuming a modern Sovereign
    "20 Dollars US": "or - 20 dollars",
    "10 Francs Napoléon": "or - 10 francs fr",
    "20 Francs Suisse": "or - 20 francs sui vreneli croix",
    "10 Dollars US": "or - 10 dollars liberté",
    "5 Dollars US": "or - 5 dollars liberté",
    "Krugerrand": "or - 1 oz krugerrand",
    "10 Florins": "or - 10 florins",  # Assuming Wilhelmina reign
    "20 Reichsmarks": "or - 20 mark",
    "Union Latine": "or - 20 francs union latine",
    "20 Francs Tunisie": "or - 20 francs tunisie",
    "Demi Souverain": "or - 1/2 souverain",  # Assuming a George V half Sovereign
    "American Eagle 1 OZ": "or - 1 oz american eagle",
    "American Buffalo 1 OZ": "or - 1 oz buffalo",
    "Maple Leaf Or 1 OZ": "or - 1 oz maple leaf",
    "Philharmonique 1 OZ": "or - 1 oz philharmonique",
    "Britannia 1 OZ Or": "or - 1 oz britannia",
    "Nugget 1 OZ": "or - 1 oz nugget / kangourou",
    "PANDA OR 30 GRAMMES": "or - 500 yuan panda",
    "EpargnOr 1/10 Oz": "or - 1/10 oz EpargnOr",
    "1 Ducat Francois-Joseph 1915 Or": "or - 1 ducat",

    "5 Francs semeuse": "ar - 5 francs fr semeuse (1959-1969)",
    "10 Francs Hercule": "ar - 10 francs fr hercule (1965-1973)",
    "2 Francs Semeuse": "ar - 2 francs fr semeuse",
    "1 Franc Semeuse": "ar - 1 franc fr semeuse",
    "50 Cts Semeuse": "ar - 50 centimes francs fr semeuse",
    "Ecu 5 Francs": "ar - 5 francs fr ecu (1854-1860)",
    "100 Francs Argent": "ar - 100 francs fr",
    "SILVER EAGLE 1 OZ": "ar - 1 oz silver eagle",
    "Kangourou 1 OZ": "ar - 1 oz nugget / kangourou",
    "Maple Leaf 1 Argent OZ": "ar - 1 oz maple leaf",
    "Philharmonique 1 OZ ARGENT": "ar - 1 oz philharmonique",
    "Britannia 1 Oz Argent": "ar - 1 oz britannia",
    "BOÎTE 500 PIÈCES MAPLE LEAF": ("ar - 1 oz maple leaf",500),
    "Sachet Scellé 1000 pièces 5 francs semeuse": ("ar - 5 francs fr semeuse (1959-1969)",1000),
    "Sachet scellé 100 pièces 5 francs semeuse": ("ar - 5 francs fr semeuse (1959-1969)",100),
    "50 Francs Hercule": "ar - 50 francs fr hercule (1974-1980)",
    "Boite 250 Pièces Kangourou": ("ar - 1 oz nugget / kangourou",250),

}
def get_delivery_price(price):
    if 0 <= price <= 600:
        return 10.0
    elif 600.01 <= price <= 2500:
        return 20.0
    elif 2500.01 <= price <= 5000:
        return 34.0
    elif 5000.01 <= price <= 7500:
        return 50.0
    elif 7500.01 <= price <= 10000:
        return 56.0
    elif 10000.01 <= price <= 15000:
        return 65.0
    else:  # price > 15000.01
        return 0.0  # Free delivery

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Change de la Bourse using requests and BeautifulSoup.
    """
    print('https://www.changedelabourse.com/or')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    urls = ['https://www.changedelabourse.com/or','https://www.changedelabourse.com/argent']

    for url in urls :
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the 'ul' with class 'product_list list row'
        product_list = soup.find('ul', class_='product_list list row')

        # Iterate over each 'li' within the 'ul'
        for product_item in product_list.find_all('li'):
            try:

                # Extract the product name
                product_name_link = product_item.find('a', class_='product-name')
                product_name = product_name_link.text.strip()
                url = product_name_link['href']
                item_data = CMN[product_name]

                # Extract the price
                price_span = product_item.find('span', class_='price product-price')
                price = Price.fromstring(price_span.text.strip())

                minimum=1
                min_p = product_item.find('p', class_='alqty')
                if min_p:
                    minimum = int(re.search(r"\d+", min_p.text).group())

                quantity = 1
                if isinstance(item_data,tuple):
                    name = item_data[0]
                    quantity = item_data[1]
                    bullion_type = item_data[0][:2]
                else :
                    name=item_data
                    bullion_type = item_data[:2]

                if bullion_type == 'or':
                    buy_price = buy_price_gold
                else :
                    buy_price = buy_price_silver

                print(price,CMN[product_name], url)

                if price:

                    # More robust price cleaning: handle variations in formatting
                    #price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))
                    coin = Item(name=name,
                                buy=price.amount_float,
                                source=url,
                                buy_premium=(((price.amount_float + get_delivery_price(
                                    price.amount_float) / minimum) / float(quantity)) - (
                                                     buy_price * poids_pieces[name])) * 100.0 / (
                                                        buy_price * poids_pieces[name]),

                                delivery_fee=get_delivery_price(price.amount_float),
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum)
                    session.add(coin)
                    session.commit()

            except Exception as e:
                print(traceback.format_exc())
                pass
