from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
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
    "10 Francs Français – Marianne Coq": 'or - 10 francs fr coq marianne',
    #"MapleGram25 2021 (25 x 1g) Or  – Edition Limitée": 'or - lingot 25 g LBMA',
    #"50 Dollars Eagle 2022 (1Oz)": 'or - 1 oz american eagle',
    #"Queen’s Beast 2021 – 1 Oz (Edition Limitée)": 'or - 1 souverain elizabeth II',
    "20 Francs Napoléon": 'or - 20 francs fr napoléon III',
    "20 Francs Marianne Coq": 'or - 20 francs fr coq marianne',
    "20 Francs Suisse (Vrenelis)": 'or - 20 francs sui vreneli croix',
    "Krugerrand": 'or - 1 oz krugerrand',
    #"Krugerrand 1 Oz Or (2024)": 'or - 1 oz krugerrand',
    #"Swiss Bullion 1+ (1 Oz 999,9 ‰)": 'or - lingot 1 once LBMA',
    "Maple Leaf": 'or - 1 oz maple leaf',
    "Australian Nugget": 'or - 1 oz nugget / kangourou',
    "Louis Belge": 'or - 20 francs union latine',
    "Souverain": 'or - 1 souverain elizabeth II',
    #"Souverain Or 2023 – Roi Charles": 'souverain or elizabeth II',
    "50 Pesos Mexique": 'or - 50 pesos mex',
    "American Buffalo": 'or - 1 oz buffalo',
    "50 dollars eagle": 'or - 1 oz american eagle',
    "Demi-souverain": 'or - 1/2 souverain georges V',
    "4 Ducats": 'or - 4 ducats',
    "20 Dollars Eagle (US)": 'or - 20 dollars liberté st gaudens',
    "50 ECU": 'or - 50 écus charles quint',
    #"Chien Lunar 2018 1 once": 'or - lingot 1 once LBMA',
    "10 Francs Français": 'or - 10 francs fr'
}

def get_price_for(session_prod, session_id,buy_price_gold,buy_price_silver,driver=None):
    if not driver:
        driver = Driver(uc=True, headless=True)
    urls = ["https://www.orobel.biz/catalogue/pieces-or","https://www.orobel.biz/catalogue/pieces-or/page/2","https://www.orobel.biz/catalogue/pieces-en-argent"]
    print(urls)

    delivery_ranges = [
    (1, 50.0, 15.0),
    (50.0, 5000.0, 35.0),
    (5000.0, 10000.0, 75.0),
    (10000.0, 15000.0, 90.0),
    (15000.0, 30000.0, 120.0),
    (30000.0, 40000.00, 200.0),
    (40000.0, 45000.00, 235.0),
    (45000.0, 999999999999.9, 300.0)  # For any price above 44999.99
]
    try :
        for url in urls : 
            driver.get(url)
    
            # Wait for the products to load (adjust the timeout as needed)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "fusion-product-wrapper"))
            )
            # Wait for the products to load (adjust the timeout as needed)
            out_of_stock_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "fusion-out-of-stock"))
            )
            # Try to find and click the "Load More Produits" button once
    
            # Find the product divs
            products_div = driver.find_elements(By.CLASS_NAME, "fusion-product-wrapper")
    
            for product in products_div:
                try:
                    product.find_element(By.CLASS_NAME,"fusion-out-of-stock")
                    continue
                except Exception:
                    name_title = product.find_element(By.CLASS_NAME,'product-images').get_attribute('aria-label')
                    source = product.find_element(By.CLASS_NAME,'product-images').get_attribute('href')
                    name = name_title.strip()
                    price_text = product.find_element(By.CLASS_NAME, 'woocommerce-Price-amount').text
                    price = Price.fromstring(price_text)

                    minimum = 1
                    quantity = 1
                    item_data = CMN.get(name,None)
                    if not item_data:
                        continue
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

                    print(price, name, url)
                    coin = Item(name=name,
                                price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                                buy_premiums=';'.join(
                                    ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price * weights[name][0] * weights[name][1])) * 100.0 / (buy_price * weights[name][0] * weights[name][1])) for i in range(1, minimum)] +
                                    ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price * weights[name][0] * weights[name][1])) * 100.0 / (buy_price * weights[name][0] * weights[name][1])) for i in range(minimum, 751)]
                                ),
                                delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                                source=source,
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