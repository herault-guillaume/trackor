import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import re
import logging
# Get the logger
logger = logging.getLogger(__name__)

# https://www.oretchange.com/content/1-livraison
CMN = {
    "https://www.oretchange.com/pieces-or/196-achat-20-francs-coq.html": 'or - 20 francs fr coq marianne',
    "https://www.oretchange.com/pieces-or/176-achat-20-francs-napoleon-iii.html": 'or - 20 francs fr napoléon III',
    "https://www.oretchange.com/pieces-or/200-achat-souverain-victoria.html": 'or - 1 souverain',
    "https://www.oretchange.com/pieces-or/198-achat-20-francs-suisse-confederation.html": 'or - 20 francs sui',
    "https://www.oretchange.com/pieces-or/179-achat-20-francs-union-latine.html": 'or - 20 francs union latine',
    "https://www.oretchange.com/pieces-or/182-achat-50-pesos-mexique.html": 'or - 50 pesos mex',
    "https://www.oretchange.com/pieces-or/186-achat-krugerrand-afrique-du-sud.html": 'or - 1 oz krugerrand',
    "https://www.oretchange.com/pieces-or/175-achat-20-dollars-liberte.html": 'or - 20 dollars',
    "https://www.oretchange.com/pieces-or/202-achat-10-dollars-tete-d-indien.html": 'or - 10 dollars liberté',
    "https://www.oretchange.com/pieces-or/180-achat-5-dollars-liberte.html": 'or - 5 dollars liberté',
    "https://www.oretchange.com/pieces-or/172-682132-achat-10-francs-napoleon-iii.html#/28-achat_or-achat_au_gre_a_gre": 'or - 10 francs fr napoléon III',
    "https://www.oretchange.com/pieces-or/170-682147-achat-demi-souverain-victoria.html#/28-achat_or-achat_au_gre_a_gre": 'or - 1/2 souverain georges V',

    "https://www.oretchange.com/pieces-d-argent-francaises/194-achat-50-francs-hercule.html": 'ar - 50 francs fr hercule (1974-1980)',
    "https://www.oretchange.com/pieces-d-argent-francaises/195-achat-5-francs-ecu.html": 'ar - 5 francs fr ecu (1854-1860)',
    "https://www.oretchange.com/pieces-d-argent-francaises/207-achat-100-francs-pantheon.html": 'ar - 100 francs fr',
    "https://www.oretchange.com/pieces-d-argent-francaises/192-achat-20-francs-turin.html": 'ar - 20 francs fr turin (1860-1928)',
    "https://www.oretchange.com/pieces-d-argent-francaises/190-achat-10-francs-turin.html": 'ar - 10 francs fr turin (1860-1928)',
    "https://www.oretchange.com/pieces-d-argent-francaises/193-achat-5-francs-semeuse.html": 'ar - 5 francs fr semeuse (1959-1969)',
    "https://www.oretchange.com/pieces-d-argent-internationales/208-achat-maple-leaf-1-once-argent.html" : 'ar - 1 oz maple leaf',
    "https://www.oretchange.com/pieces-d-argent-internationales/209-achat-silver-eagle-1-once-argent.html" : 'ar - 1 oz silver eagle',
    "https://www.oretchange.com/pieces-d-argent-internationales/210-achat-philharmonique-1-once-argent.html" : 'ar - 1 oz philharmonique',
    "https://www.oretchange.com/pieces-d-argent-internationales/217-achat-panda-1-once-argent.html" : 'ar - 10 yuan panda 30g',
    "https://www.oretchange.com/pieces-d-argent-internationales/253-kangourou-1-once-argent.html" : 'ar - 1 oz nugget / kangourou',

}

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """

    print("https://www.oretchange.com/")
    logger.debug("https://www.oretchange.com/")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    delivery_ranges = [(0.0,999999999.9,0.0)]
    for url, item_data in CMN.items():
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        try:

            quantity = 1
            minimum = 1

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

            price_ranges = []

            table = soup.find('table',class_='table table-bordered')

            if not table:
                unique_price = soup.find('div',class_='metal_product').find('b')
                price = Price.fromstring(unique_price.text)
                price_ranges.append((1,999999999,price))

            else :
                rows = table.find('tbody').find_all('tr')
                values = [row.find_all('td') for row in rows]

                for v in values:
                    match = re.search(r"(\d+)\s*\D+\s*(\d+)", v[0].text)

                    if match:
                        min = int(match.group(1))
                        max = int(match.group(2))
                    else:
                        min = int(re.search(r"\d+", v[0].text).group())
                        max = 9999999999.9



                    price = Price.fromstring(v[1].text)
                    price_ranges.append((min,max,price))

            min_p = int(soup.find('input', class_='qty')['value'])
            if min_p>minimum:
                minimum = min_p

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
            print(price,name,url)
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
            logger.error(f"Request error occurred: {e}")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            traceback.print_exc()