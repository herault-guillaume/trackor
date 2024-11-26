from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights
from price_parser import Price
import traceback
import re
import logging
from datetime import datetime
import pytz
# Get the logger. This assumes you have set up logging in logging_config.py
logger = logging.getLogger(__name__)

CMN = {
    '20 Francs Marianne Coq': 'or - 20 francs fr coq marianne',
    '10 Francs Napoléon': 'or - 10 francs fr',
    '20 Fr Or Coq': 'or - 20 francs fr coq marianne',
    '50 Pesos Or': 'or - 50 pesos mex',
    "Louis d'Or - 20 Francs Or": 'or - 20 francs fr',
    '20 Francs Napoléon': 'or - 20 francs fr',
    'Krugerrand': 'or - 1 oz krugerrand',
    'Souverain': 'or - 1 souverain',  # No exact match for "Souverain"
    'Union Latine': 'or - 20 francs union latine',
    '20 Francs Suisse': 'or - 20 francs sui vreneli croix',
    '20 Dollars US': 'or - 20 dollars',
    '10 Dollars US': 'or - 10 dollars liberté',
    '5 Dollars US Or': 'or - 5 dollars liberté',
    '10 Florins Or': 'or - 10 florins',
    '20 Reichsmarks': 'or - 20 mark wilhelm II',
    '1 Ducat Or Francois-Joseph 1915': 'or - 1 ducat',
    'Set 5 pièces 20 Fr Or Marianne Coq': ('or - 20 francs fr coq marianne',5),  # No exact match
    'Set 5 Pièces 20 Francs Or': ('or - 20 francs fr',5),
    '4 Ducats Or': 'or - 4 ducats',
    '20 Francs Tunisie': 'or - 20 francs tunisie',
    'Demi Souverain': 'or - 1/2 souverain',

    'Dragon Lunar Série III 1 Once Or': 'or - 1 oz dragon 2024 lunar III',
    'American Buffalo 1 Once Or': 'or - 1 oz buffalo',
    'Britannia 1 Once Or': 'or - 1 oz britannia',
    #'EpargnOr 1 Once Or': 'or - 1/2 souverain',
    'Maple Leaf 1 Once Or': 'or - 1 oz maple leaf',
    'Philharmonique 1 Once Or': 'or - 1 oz philharmonique',
    'Nugget 1 Once Or': 'or - 1 oz nugget / kangourou',
    'American Eagle 1 Once Or': 'or - 1 oz american eagle',
    'Panda 30g Or': 'or - 500 yuan panda',
    'Maple Leaf 1/2 Once Or': 'or - 1/2 oz maple leaf',
    'American Eagle 1/2 Once Or': 'or - 1/2 oz american eagle',
    'Philharmonique 1/2 Once Or': 'or - 1/2 oz philharmonique',
    'Krugerrand 1/2 Once Or': 'or - 1/2 oz krugerrand',
    'Nugget 1/2 Once Or': 'or - 1/2 oz nugget / kangourou',
    'Britannia 1/2 Once Or': 'or - 1/2 oz britannia',
    'Panda 15g Or': 'or - 200 yuan panda',
    'Maple Leaf 1/4 Once Or': 'or - 1/4 oz maple leaf',
    'American Eagle 1/4 Once Or': 'or - 1/4 oz american eagle',
    'Philharmonique 1/4 Once Or': 'or - 1/4 oz philharmonique',
    'Krugerrand 1/4 Once Or': 'or - 1/4 oz krugerrand',
    'Britannia 1/4 Once Or': 'or - 1/4 oz britannia',
    'Nugget 1/4 Once Or': 'or - 1/4 oz nugget / kangourou',
    'Panda 8g Or': 'or - 100 yuan panda',
    'American Eagle 1/10 Once Or': 'or - 1/10 oz american eagle',
    'Krugerrand 1/10 Once Or': 'or - 1/10 oz krugerrand',
    'Britannia 1/10 Once Or': 'or - 1/10 oz britannia',
    #'EpargnOr 1/10 Once Or': 'or - 1/2 souverain',
    'Maple Leaf 1/10 Once Or': 'or - 1/10 oz maple leaf',
    'Philharmonique 1/10 Once Or': 'or - 1/10 oz philharmonique',
    'Nugget 1/10 once Or': 'or - 1/10 oz nugget / kangourou',
    'Panda 3g Or': 'or - 50 yuan panda',

    '10 Francs Turin 1929 - 1939': 'ar - 10 francs fr turin (1860-1928)',
    '5 Francs Semeuse 1959-1969': 'ar - 5 francs fr semeuse (1959-1969)',
    'Ecu 5 Francs': 'ar - 5 francs fr ecu (1854-1860)',
    '2 Francs Semeuse 1898 - 1920': 'ar - 2 francs fr semeuse',
    '1 Franc Semeuse 1898 - 1920': 'ar - 1 franc fr semeuse',
    '50 Cts Semeuse 1897 - 1920': ('ar - 50 centimes francs fr semeuse',10),
    '100 Francs Argent 1982 - 2002': 'ar - 100 francs fr',
    '20 Francs Turin 1929 - 1939': 'ar - 20 francs fr turin (1929-1939)',
    '50 Francs Hercule 1974 - 1980': 'ar - 50 francs fr hercule (1974-1980)',
    '10 Francs Hercule 1964 - 1973': 'ar - 10 francs fr hercule (1965-1973)',

    'Boite 250 pièces Nugget': ('ar - 1 oz nugget / kangourou',250),
    'Boite 500 Pièces Britannia': ('ar - 1 oz britannia',500),
    'Boite 500 Pièces Krugerrand': ('ar - 1 oz krugerrand',500),
    'Boite 500 Pièces Maple Leaf': ('ar - 1 oz maple leaf',500),
    'Boite 500 Pièces Silver Eagle': ('ar - 1 oz silver eagle',500),
    'Boite 500 Pièces Philharmonique': ('ar - 1 oz philharmonique',500),
    '1 Kilo Argent Fin: sachet 20 Francs Turin': ('ar - 20 francs fr turin (1929-1939)',74),
    'Sachet Scellé 1000 Pièces 5 Francs Semeuse': ('ar - 5 francs fr semeuse (1959-1969)',1000),
    'Sachet Scellé 100 Pièces 5 Francs Semeuse': ('ar - 5 francs fr semeuse (1959-1969)',100),
    '1 Kilo Argent Fin: sachet 10 Francs Turin': ('ar - 10 francs fr turin (1860-1928)',148),
    "Sachet Scellé 45 pièces d'Ecu 5 Francs" : ('ar - 5 francs fr ecu (1854-1860)',45),
}

def get_price_for(session_prod,session_staging, session_id, buy_price_gold,buy_price_silver,driver):

    base_url = "https://www.achat-or-et-argent.fr"
    print(base_url)
    logger.debug(f"Scraping started for {base_url}") # Example debug log

    # URLs to scrape
    urls = [
        f"{base_url}/argent/5/pieces-francaises",
        f"{base_url}/argent/80/gros-volume-argent",
        f"{base_url}/or/2/pieces-d-or-d-investissement",
        f"{base_url}/or/4/pieces-modernes",

    ]

    delivery_ranges = [
        (0.0,1000.0,15.0),
        (1000.01,2500.0,20.0),
        (2500.01,5000.0,34.0),
        (5000.01,7500.0,50.0),
        (7500.01,10000.0,56.0),
        (10000.01,15000.0,65.0),
        (15000.01,100000000000000.0,0.0),
    ]

    for url in urls:

        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Explicitly wait for the target element to be present
        tableau = wait.until(EC.presence_of_element_located((By.ID, "contentCategVitrine")))

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.row.BStooltip.align-items-center")))

        # Use find_elements to get a list of matching elements
        rows = tableau.find_elements(By.CSS_SELECTOR, "div[id*='prod']")
        print('2')
        for row in rows:
            try:

                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "a"))
                )

                row_html = row.get_attribute('outerHTML')
                row_soup = BeautifulSoup(row_html, 'html.parser')

                product_url_elem = row_soup.find_all('a')

                source = "https://www.achat-or-et-argent.fr" + product_url_elem[1]["href"]
                # Explicitly wait for the span within the product_url_elem to be visible
                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "span")))

                span_elem = row_soup.find('span')
                product_name = span_elem.text.strip()

                item_data = CMN[product_name]
                quantity = 1
                minimum = 1

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

                price = None

                row_price = row_soup.find('div',class_="row BStooltip align-items-center")

                price_ranges = []

                if row_price :

                    data_content = row_price["data-original-title"]

                    inner_soup = BeautifulSoup(data_content, 'html.parser')

                    quantity_divs = inner_soup.find_all("div", class_="col-6 text-left selected h5") + inner_soup.find_all("div", class_="col-6 text-left h5")  # Get divs with quantity text
                    price_divs = inner_soup.find_all("div", class_="col-6 text-right h5")  # Get divs with price text

                    len_price = len(price_divs)
                    i = 0
                    for qty_div, price_div in zip(quantity_divs,price_divs):  # Skip the first qty div ("Vous achetez")
                        match = re.search(r"(\d+)\s*\D+\s*(\d+)", qty_div.get_text(strip=True))
                        if match:
                            min = int(match.group(1))
                            max = int(match.group(2))
                        else:
                            min = int(re.search(r"\d+", qty_div.get_text(strip=True)).group())
                            max = 9999999999.0

                        price = Price.fromstring(price_div.get_text(strip=True))
                        price_ranges.append([min, max, price]),

                else :

                    row_price = row_soup.find('del', class_="small text-dark").parent
                    price = Price.fromstring(row_price.text)

                    if name == 'ar - 50 centimes francs fr semeuse':
                        minimum = int(quantity)
                        quantity = 1

                    price_ranges.append([minimum, 999999999, price]),

                print(price, name, source)

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
                                ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price * weights[name])) * 100.0 / (buy_price * weights[name])) for i in range(1, minimum)] +
                                ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price * weights[name])) * 100.0 / (buy_price * weights[name])) for i in range(minimum, 151)]
                            ),
                            delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                            source=source,
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=quantity,
                            minimum=minimum, timestamp=datetime.now(pytz.timezone('CET')).replace(second=0, microsecond=0)
)
                coin_staging = Item(**coin.__dict__)
                session_prod.add(coin)
                session_prod.commit()
                session_prod.expunge(coin_staging)
                session_staging.add(coin)
                session_staging.commit()

            except KeyError as e:
                logger.error(f"KeyError: {product_name}")

            except Exception as e:
                logger.error(f"An error occurred while processing: {e}")
                traceback.print_exc()