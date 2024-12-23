import requests
from bs4 import BeautifulSoup
from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights
from price_parser import Price
import traceback
import logging
from datetime import datetime
import pytz
# Get the logger
logger = logging.getLogger(__name__)

CMN = {
    "Pièce Or 20 Francs Marianne Coq": 'or - 20 francs fr coq marianne',
    "Pièce Or 20 Francs Napoléon III": 'or - 20 francs fr napoléon III',
    "Pièce Or 20 Francs Suisse": 'or - 20 francs sui vreneli croix',  # Assuming "Suisse" refers to the Vreneli coin
    "Pièce Or 10 Dollars US": 'or - 10 dollars liberté',  # Assuming "Liberté" is the most common 10 dollar US gold coin
    "Pièce Or 20 Dollars US": 'or - 20 dollars',  # Similar assumption as above
    "Pièce Or Union Latine": 'or - 20 francs union latine',  # Assuming the most common Union Latine coin
    "Pièce Or 50 Pesos": 'or - 50 pesos mex',
    "Pièce Or Souverain": 'or - 1 souverain elizabeth II',  # Assuming the most recent monarch
    "Pièce Or Krugerrand": 'or - 1 oz krugerrand',
    "Pièce Or 100 Francs Napoléon III": 'or - 100 francs fr napoléon III tête nue',
    "Pièce Or 50 Francs Napoléon III": 'or - 50 francs fr napoléon III tête nue',
    "Pièce Or 5 Dollars US": 'or - 5 dollars liberté',  # Same assumption as for 10 dollars
    "Pièce Or 20 Francs Génie": 'or - 20 francs fr génie debout',
    "Pièce Or 20 Mark Allemande": 'or - 20 mark wilhelm II',

    "Pièces Argent 10 Francs Hercule - Lot de 10 pièces": ('ar - 10 francs fr hercule (1965-1973)',10),
    "Pièces Argent 50 Francs Hercule - Lot de 10 pièces": ('ar - 50 francs fr hercule (1974-1980)',10),
    "Pièces Argent 5 Francs Semeuse - Lot de 10": ('ar - 5 francs fr semeuse (1959-1969)',10),
    "Pièce Koala Argent 1kg Australie": 'ar - 1 kg koala',
    "Pièces Argent Maple Leaf Canadien - Lot de 3 pièces": ('ar - 1 oz maple leaf',3),
    "Pièces d'Argent Philharmonique de Vienne - Lot de 3 pièces": ('ar - 1 oz philharmonique',3),
}

# https://or-investissement.fr/information-or-investissement/1-livraison-achat-or-investissement
def get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Or-Investissement using requests and BeautifulSoup.
    """
    urls = ['https://or-investissement.fr/12-achat-piece-or-investissement','https://or-investissement.fr/13-achat-piece-argent-investissement']
    logger.debug("https://or-investissement.fr")
    for url in urls :

        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        try :
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the span element with class "result2"
            products_div = soup.find_all("article")

            for product in products_div:
                try:
                    price_text = product.find('span','product-price').text

                    price = Price.fromstring(price_text)
                    name_title = product.find("h3", "h3 product-title")
                    url = name_title.find('a')['href']

                    name = name_title.text.strip()
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

                    print(price,name,url)

                    delivery_ranges = [(0,999999999.9,25.0)]
                    price_ranges = [(minimum,9999999999,price)]

                    def price_between(value, ranges):
                        """
                        Returns the price per unit for a given quantity.
                        """
                        for min_qty, max_qty, price in ranges:
                            if min_qty <= value < max_qty:
                                if isinstance(price, Price):
                                    return price.amount_float
                                else:
                                    return price

                    coin = Item(name=name,
                                price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                                buy_premiums=';'.join(
                                    ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price * weights[name])) * 100.0 / (buy_price * weights[name])) for i in range(1, minimum)] +
                                    ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price * weights[name])) * 100.0 / (buy_price * weights[name])) for i in range(minimum, 751)]
                                ),
                                delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                                source=url,
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum, timestamp=datetime.now(pytz.timezone('CET'))
)

                    session_prod.add(coin)
                    session_prod.commit()


                except KeyError as e:
                    logger.error(f"KeyError: {name}")

                except Exception as e:
                    logger.error(f"An error occurred while processing a product: {e}")
                    traceback.print_exc()

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            traceback.print_exc()