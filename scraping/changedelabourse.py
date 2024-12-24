import requests
from bs4 import BeautifulSoup
from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights
from price_parser import Price
import re
import logging
from datetime import datetime
import pytz
# Get the logger
logger = logging.getLogger(__name__)

CMN = {
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/napoleon-or-20-francs": "or - 20 francs fr",  # Assuming a standard 20 Francs gold coin
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/50-pesos": "or - 50 pesos mex",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/souverain": "or - 1 souverain",  # Assuming a modern Sovereign
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/20-dollars-us": "or - 20 dollars",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/10-francs-napoleon": "or - 10 francs fr",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/20-francs-suisse": "or - 20 francs sui vreneli croix",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/10-dollars-us": "or - 10 dollars liberté",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/5-dollars-us": "or - 5 dollars liberté",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/krugerrand": "or - 1 oz krugerrand",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/10-florins": "or - 10 florins",  # Assuming Wilhelmina reign
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/20-reichsmarks": "or - 20 mark",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/union-latine": "or - 20 francs union latine",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/20-francs-tunisie": "or - 20 francs tunisie",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/demi-souverain": "or - 1/2 souverain",  # Assuming a George V half Sovereign
    "https://www.changedelabourse.com/or/pieces-d-or-modernes/american-eagle-1-oz": "or - 1 oz american eagle",
    "https://www.changedelabourse.com/or/pieces-d-or-modernes/american-buffalo-1-oz": "or - 1 oz buffalo",
    "https://www.changedelabourse.com/or/pieces-d-or-modernes/maple-leaf-or-1-oz": "or - 1 oz maple leaf",
    "https://www.changedelabourse.com/or/pieces-d-or-modernes/philharmonique-1-oz": "or - 1 oz philharmonique",
    "https://www.changedelabourse.com/or/pieces-d-or-modernes/britannia-1-oz-or": "or - 1 oz britannia",
    "https://www.changedelabourse.com/or/pieces-d-or-modernes/nugget-1-oz": "or - 1 oz nugget / kangourou",
    "https://www.changedelabourse.com/or/pieces-d-or-modernes/panda-or-30-grammes": "or - 500 yuan panda",
    "https://www.changedelabourse.com/or/pieces-d-or-modernes/epargnor-1-10-oz": "or - 1/10 oz EpargnOr",
    "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/1-ducat-francois-joseph-1915-or": "or - 1 ducat",

    "https://www.changedelabourse.com/argent/pieces-argent-francaises/5-francs-semeuse": "ar - 5 francs fr semeuse (1959-1969)",
    "https://www.changedelabourse.com/argent/pieces-argent-francaises/10-francs-hercule": "ar - 10 francs fr hercule (1965-1973)",
    "https://www.changedelabourse.com/argent/pieces-argent-francaises/2-francs-semeuse": "ar - 2 francs fr semeuse",
    "https://www.changedelabourse.com/argent/pieces-argent-francaises/1-franc-semeuse": "ar - 1 franc fr semeuse",
    "https://www.changedelabourse.com/argent/pieces-argent-francaises/50-cts-semeuse": "ar - 50 centimes francs fr semeuse",
    "https://www.changedelabourse.com/argent/pieces-argent-francaises/ecu-5-francs": "ar - 5 francs fr ecu (1854-1860)",
    "https://www.changedelabourse.com/argent/pieces-argent-francaises/100-francs-argent": "ar - 100 francs fr",
    "https://www.changedelabourse.com/argent/pieces-argent-modernes/silver-eagle-1-oz": "ar - 1 oz silver eagle",
    "https://www.changedelabourse.com/argent/pieces-argent-modernes/kangourou-1-oz": "ar - 1 oz nugget / kangourou",
    "https://www.changedelabourse.com/argent/pieces-argent-modernes/maple-leaf-1-argent-oz": "ar - 1 oz maple leaf",
    "https://www.changedelabourse.com/argent/pieces-argent-modernes/philharmonique-1-oz-argent": "ar - 1 oz philharmonique",
    "https://www.changedelabourse.com/argent/pieces-argent-modernes/britannia-1-oz-argent": "ar - 1 oz britannia",
    "https://www.changedelabourse.com/argent/gros-volumes-argent/boite-500-pieces-maple-leaf": ("ar - 1 oz maple leaf",500),
    "https://www.changedelabourse.com/argent/gros-volumes-argent/sachet-scelle-1000-pieces-5-francs-semeuse": ("ar - 5 francs fr semeuse (1959-1969)",1000),
    "https://www.changedelabourse.com/argent/gros-volumes-argent/sachet-scelle-100-pieces-5-francs-semeuse": ("ar - 5 francs fr semeuse (1959-1969)",100),
    "https://www.changedelabourse.com/argent/pieces-argent-francaises/50-francs-hercule": "ar - 50 francs fr hercule (1974-1980)",
    "https://www.changedelabourse.com/argent/gros-volumes-argent/boite-250-pieces-kangourou": ("ar - 1 oz nugget / kangourou",250),

}

def get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Change de la Bourse using requests and BeautifulSoup.
    """
    print('https://www.changedelabourse.com/or')
    logger.debug("Scraping started for https://www.changedelabourse.com/or")

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
        (15000.01, 999999999999.0, 0.01)  # Price 15000.01+, free delivery
    ]

    for url, name in CMN.items() :
        try :
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the 'ul' with class 'product_list list row'
            item_data = name

            # Extract the price
            price_span = soup.find('span', id='our_price_display')
            price = Price.fromstring(price_span.text.strip())

            minimum = int(soup.find('input',id="quantity_wanted")['value'])

            mins = soup.find_all('p',class_='cdb-quantite')
            mins_prices = soup.find_all('p',class_='cdb-pricea')

            price_ranges = []
            if mins and mins_prices:
                for i in range(0,len(mins)+1):
                    if i == 0:
                        price_ranges.append((minimum,int(re.search(r"\d+", mins[i].text).group()),price))
                    elif i == len(mins):
                        price_ranges.append((int(re.search(r"\d+", mins[i-1].text).group()),999999999,
                                             Price.fromstring(mins_prices[i-1].text)))
                    else :
                        price_ranges.append((int(re.search(r"\d+", mins[i-1].text).group()),
                                             int(re.search(r"\d+", mins[i].text).group()),
                                             Price.fromstring(mins_prices[i-1].text)))
            else :
                price_ranges.append([minimum,9999999999,price])

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

            print(price,name, url)

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

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")

        except Exception as e:
            logger.error(f"An error occurred while processing: {e}")
