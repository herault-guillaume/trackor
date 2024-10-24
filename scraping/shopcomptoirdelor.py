import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import Price
import traceback


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
    "Feuille d'Érable 1/20 OZ or diverses années" : 'or - 1/20 maple leaf',
    '4 ducats autrichiens or diverses années' : 'or - 4 ducats',
    "Kangourou 1/2 OZ or diverses années": 'or - 1/2 oz nugget / kangourou',
    'Kangourou 1/4 OZ or diverses années' : 'or - 1/4 oz nugget / kangourou',
    "Kangourou 1/10 OZ or diverses années": 'or - 1/10 oz nugget / kangourou',
    'Lunar 1/2 OZ or diverses années' : 'or - 1/2 oz lunar',
    'Lunar 1/10 OZ or diverses années' : 'or - 1/10 oz lunar',
    "Nugget en or 1 once troy années diverses": 'or - 1 oz nugget / kangourou',
    'Lunar 1/20 OZ en or diverses années' : 'or - 1/10 oz lunar',
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

def get_price_for(session, session_id,buy_price_gold,buy_price_silver):
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
    driver = Driver(uc=True, headless=True)

    for url in urls:
        try :
            driver.get(url)

            # Wait for the products to load (adjust the timeout as needed)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "div"))
            )
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "article-price"))
            )
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
            )
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card-content-title"))
            )
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "row"))
            )

            # Find the product divs
            products_div = driver.find_elements(By.CLASS_NAME, "row")

            for product in products_div:
                try:

                    name_title = product.find_element(By.CLASS_NAME, "card-content-title")
                    url = name_title.get_attribute('href')
                    name = name_title.text.strip()

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

                    #Check if the name is in your CMN dictionary
                    coin = Item(name=name,
                                prices=price.amount_float,
                                source=url,
                                buy_premiums=(((price.amount_float + 24.95 / minimum) / float(quantity)) - (
                                                     buy_price * poids_pieces[name])) * 100.0 / (
                                                        buy_price * poids_pieces[name]),

                                delivery_fee=24.95,
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum)
                    session.add(coin)
                    session.commit()

                except Exception as e:
                    #print(traceback.format_exc())
                    pass
        except Exception as e:
            #print(traceback.format_exc())
            pass