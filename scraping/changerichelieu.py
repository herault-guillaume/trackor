import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import re
import logging

# Get the logger
logger = logging.getLogger(__name__)

CMN = {
    "20 Francs Napoléon": "or - 20 francs fr",
    "20 Francs Suisse": "or - 20 francs sui vreneli croix",
    "Union Latine": "or - 20 francs union latine",
    "Souverain": "or - 1 souverain",
    "Demi Souverain": "or - 1/2 souverain",
    "50 Pesos": "or - 50 pesos mex",
    "10 Francs Napoléon": "or - 10 francs fr napoléon III",
    "Krugerrand": "or - 1 oz krugerrand",
    "10 Dollars US": "or - 10 dollars liberté",
    "5 Dollars US": "or - 5 dollars liberté",
    "20 Reichsmarks": "or - 20 mark",
    "10 Florins": "or - 10 florins",
    "Maple Leaf Or 1 OZ": "or - 1 oz maple leaf",
    "American Eagle 1 OZ": "or - 1 oz american eagle",
    "Philharmonique 1 OZ": "or - 1 oz philharmonique",
    "American Buffalo 1 OZ": "or - 1 oz buffalo",
    "Nugget 1 OZ": "or - 1 oz nugget / kangourou",
    "Britannia 1 OZ Or": "or - 1 oz britannia",
    "PANDA OR 30 GRAMMES": "or - 500 yuan panda",
    "EpargnOr OZ": "or - 1 oz EpargnOr",

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
    "Kangourou 1 OZ": "ar - 1 oz nugget / kangourou",
    "Koala 1 OZ": "ar - 1 oz koala",
    "Maple Leaf 1 OZ Ar...": "ar - 1 oz maple leaf",
    "Philharmonique 1 O...": "ar - 1 oz philharmonique",
    "Britannia 1 Oz Argent": "ar - 1 oz britannia",
    "BOÎTE 500 PIÈCES MAPLE LEAF": ("ar - 1 oz maple leaf",500),
    "Sachet Scellé 1000 pièces 5 francs semeuse": ("ar - 5 francs fr semeuse (1959-1969)",1000),
    "Sachet scellé 100 pièces 5 francs semeuse": ("ar - 5 francs fr semeuse (1959-1969)",100),
    "50 Francs Hercule": "ar - 50 francs fr hercule (1974-1980)",
    "Boite 250 Pièces Kangourou": ("ar - 1 oz nugget / kangourou",250),
}

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    urls = ["https://www.changerichelieu.fr/or","https://www.changerichelieu.fr/argent"]
    logger.debug("Scraping started for https://www.changerichelieu.fr/")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    delivery_ranges = [
    (0, 600, 10.0),      # Price 0-600, delivery cost 10.0
    (600.01, 2500, 20.0),  # Price 600.01-2500, delivery cost 20.0
    (2500.01, 5000, 34.0), # Price 2500.01-5000, delivery cost 34.0
    (5000.01, 7500, 50.0), # Price 5000.01-7500, delivery cost 50.0
    (7500.01, 10000, 56.0),# Price 7500.01-10000, delivery cost 56.0
    (10000.01, 15000, 65.0),# Price 10000.01-15000, delivery cost 65.0
    (15000.01, float('inf'), 0.0)  # Price 15000.01+, free delivery
]

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

                minimum = 1
                min_p = div.find('p', class_='alqty hidden')
                if min_p:
                    minimum = int(re.search(r"\d+", min_p.text).group())

                qty = div.find_all('li',class_='left')
                prices = div.find_all('li',class_='right')
                price_ranges = []
                if len(qty) > 1 and len(prices) > 1:
                    for q,p in zip(qty[1:],prices[1:]):
                        match = re.search(r"(\d+)\s*\D+\s*(\d+)", q.text)
                        if match :
                            min = int(match.group(1))
                            max = int(match.group(2))
                        else:
                            min = int(re.search(r"\d+", q.text).group())
                            max = 9999999999.0
                        price_ranges.append((min,max,Price.fromstring(p.text)))

                else :                    # Extract price
                    price_element = div.find('p', class_='price product-price')
                    price = Price.fromstring(price_element.text.strip())
                    price_ranges.append((minimum,999999999,price))

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
                            price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                            buy_premiums=';'.join(
    ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(1,minimum)] +
    ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(minimum,151)]
                            ),
                            delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                            source=url,
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=quantity,
                            minimum=minimum)

                session.add(coin)
                session.commit()


            except KeyError as e:
                logger.error(f"KeyError: {name}")

            except requests.exceptions.RequestException as e:
                logger.error(f"An error occurred while making the request: {e}")

            except Exception as e:
                logger.error(f"An error occurred while processing: {e}")
