import time

from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import Price
import traceback
import logging
from datetime import datetime
import pytz

# Get the logger
logger = logging.getLogger(__name__)

CMN = {
    '50 pesos mex mexicains or diverses années' : 'or - 50 pesos mex',
    '20 lires italiennes or diverses années' : 'or - 20 lire vittorio emanuele II',
    "1 ducat autrichien or diverses années": 'or - 1 ducat',
    "Kangourou 1 OZ or diverses années": 'or - 1 oz nugget / kangourou',
    'Lunar 1 OZ or diverses années' : 'or - 1 oz lunar',
    'Lunar 1/4 OZ or diverses années' : 'or - 1/4 oz lunar',
    "50 ECU Belgique diverses années": 'or - 50 écus charles quint',
    "100 ECU Belgique diverses années": 'or - 100 écus or charles quint',
    "10 francs français or diverses années": 'or - 10 francs fr',
    "Aigle américain 1/10 OZ or diverses années": 'or - 1/10 oz american eagle',
    'Aigle américain 1/4 OZ or diverses années' : 'or - 1/4 oz american eagle',
    "Aigle américain 1/2 OZ or diverses années": 'or - 1/2 oz american eagle',
    "5 dollars USA or diverses années": 'or - 5 dollars liberté',
    "10 dollars USA or diverses années": 'or - 10 dollars liberté',
    "1 rand sud-africains or diverses années": 'or - 1 rand sud-africains',
    "2 rands sud-africains or diverses années": 'or - 2 rand sud-africains',
    "Ducat simple d'or néerlandais diverses années": 'or - 1 ducat',
    'Panda en or 30gr diverses années' : 'or - 500 yuan panda',
    '100 Corona en or diverses années': 'or - 100 couronnes françois joseph I',
    "Ducat double d'or néerlandais diverses années" : 'or - 1 ducat',
    '100 Dollars Canada or diverses années' : 'or - 100 dollars canadien',
    "1/2 Souverain d'or / Livre diverses années": 'or - 1/2 souverain georges V',
    "Feuille d'Érable 1 OZ or diverses années" : 'or - 1 oz maple leaf',
    '20 francs français or diverses années' : 'or - 20 francs fr',
    '20 francs belges or diverses années' : 'or - 20 francs bel',
    'Philharmonique 1 OZ or diverses années' : 'or - 1 oz philharmonique',
    'Panda 1 OZ or diverses années' : 'or - 1 oz panda',
    "Feuille d'Érable 1/20 OZ or diverses années" : 'or - 1/20 oz maple leaf',
    '4 ducats autrichiens or diverses années' : 'or - 4 ducats',
    "Kangourou 1/2 OZ or diverses années": 'or - 1/2 oz nugget / kangourou',
    'Kangourou 1/4 OZ or diverses années' : 'or - 1/4 oz nugget / kangourou',
    "Kangourou 1/10 OZ or diverses années": 'or - 1/10 oz nugget / kangourou',
    'Lunar 1/2 OZ or diverses années' : 'or - 1/2 oz lunar',
    'Lunar 1/10 OZ or diverses années' : 'or - 1/10 oz lunar',
    "Nugget en or 1 once troy années diverses": 'or - 1 oz nugget / kangourou',
    'Lunar 1/20 OZ en or diverses années' : 'or - 1/20 oz lunar',
    'Kangourou 1 OZ argent diverses années' : 'ar - 1 oz nugget / kangourou',
    'Britannia en argent 1 OZ diverses années' : 'ar - 1 oz britannia',
    'Monsterbox Britannia en argent 1 OZ diverses années' : ('ar - 1 oz nugget / kangourou',250),
    'Lunar 1 kg argent diverses années' : 'ar - 1 kg lunar',
    'Krugerrand 1 OZ argent diverses années' : 'ar - 1 oz nugget / kangourou',
    'Libertad Mexico 1 OZ argent diverses années' : 'ar - 1 oz libertad',
    'Koala 1 OZ argent diverses années' : 'ar - 1 oz koala',
    'Monsterbox Aigle américain 500x 1 OZ argent diverses années' : ('ar - 1 oz silver eagle',500),
    'Monsterbox Krugerrand 500x 1 OZ argent diverses années' : ('ar - 1 oz krugerrand',500)

}

def get_price_for(session_prod, session_id,buy_price_gold,buy_price_silver,driver):
    """
    Retrieves coin purchase prices from Orobel using Selenium.
    """

    urls = ["https://www.shop-comptoirdelor.be/achat-or/pieces?page=1",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=2",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=3",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=4",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=5",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=6",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=7",
            "https://www.shop-comptoirdelor.be/achat-argent?page=1",
            "https://www.shop-comptoirdelor.be/achat-argent?page=2",
            "https://www.shop-comptoirdelor.be/achat-argent?page=3",
    ]

    print(urls)

    for url in urls:
        try :
            driver.get(url)
            time.sleep(10)
            # Wait for the products to load (adjust the timeout as needed)
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_all_elements_located((By.TAG_NAME, "div"))
            # )
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_all_elements_located((By.CLASS_NAME, "article-price"))
            # )
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
            # )
            # WebDriverWait(driver, 20).until(
            #     EC.presence_of_all_elements_located((By.CLASS_NAME, "card-content-title"))
            # )
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_all_elements_located((By.CLASS_NAME, "row"))
            # )

            # Find the product divs
            products_div = driver.find_elements(By.CLASS_NAME, "row")

            for product in products_div:
                try:
                    name_title = product.find_element(By.CSS_SELECTOR, "a.card-content-title[itemprop='name']")
                except :
                    continue
                try :
                    url = name_title.get_attribute('href')
                    name = name_title.text.strip()
                    print(name)
                    price_text = product.find_element(By.CLASS_NAME, 'article-price').text
                    price = Price.fromstring(price_text)

                    minimum = 1
                    quantity = 1
                    item_data = CMN[name]
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

                    print(price, name, url)

                    price_ranges = [(minimum,9999999999,price)]
                    delivery_ranges =[(0.0,999999999.9,24.95)]

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
                                    ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price * weights[name][0] * weights[name][1])) * 100.0 / (buy_price * weights[name][0] * weights[name][1])) for i in range(1, minimum)] +
                                    ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price * weights[name][0] * weights[name][1])) * 100.0 / (buy_price * weights[name][0] * weights[name][1])) for i in range(minimum, 751)]
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

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            traceback.print_exc()