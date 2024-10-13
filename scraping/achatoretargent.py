import requests
from bs4 import BeautifulSoup
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import re

from scraping.changedelabourse import CMN

CMN = {
    '20 Francs Marianne Coq': 'or - 20 francs fr coq marianne',
    '10 Francs Napoléon': 'or - 10 francs fr',
    '50 Pesos Or': 'or - 50 pesos',
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
    'Panda 30g Or': 'or - 500 yuan panda 2024 30g',
    'Maple Leaf 1/2 Once Or': 'or - 1/2 oz maple leaf',
    'American Eagle 1/2 Once Or': 'or - 1/2 oz american eagle',
    'Philharmonique 1/2 Once Or': 'or - 1/2 oz philharmonique',
    'Krugerrand 1/2 Once Or': 'or - 1/2 oz krugerrand',
    'Nugget 1/2 Once Or': 'or - 1/2 oz nugget / kangourou',
    'Britannia 1/2 Once Or': 'or - 1/2 oz britannia',
    'Panda 15g Or': 'or - 200 yuan panda 2024 15g',
    'Maple Leaf 1/4 Once Or': 'or - 1/4 oz maple leaf',
    'American Eagle 1/4 Once Or': 'or - 1/4 oz american eagle',
    'Philharmonique 1/4 Once Or': 'or - 1/4 oz philharmonique',
    'Krugerrand 1/4 Once Or': 'or - 1/4 oz krugerrand',
    'Britannia 1/4 Once Or': 'or - 1/4 oz britannia',
    'Nugget 1/4 Once Or': 'or - 1/4 oz nugget / kangourou',
    'Panda 8g Or': 'or - 100 yuan panda 2024 8g',
    'American Eagle 1/10 Once Or': 'or - 1/10 oz american eagle',
    'Krugerrand 1/10 Once Or': 'or - 1/10 oz krugerrand',
    'Britannia 1/10 Once Or': 'or - 1/10 oz britannia',
    #'EpargnOr 1/10 Once Or': 'or - 1/2 souverain',
    'Maple Leaf 1/10 Once Or': 'or - 1/10 oz maple leaf',
    'Philharmonique 1/10 Once Or': 'or - 1/10 oz philharmonique',
    'Nugget 1/10 once Or': 'or - 1/10 oz nugget / kangourou',
    'Panda 3g Or': 'or - 50 yuan panda 2024 3g',

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

def get_delivery_price(price):
    if 0 <= price <= 1000:
        return 15.0
    elif 1000.01 <= price <= 2500:
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

def get_price_for(session, session_id, buy_price_gold,buy_price_silver):

    base_url = "https://www.achat-or-et-argent.fr"
    print(base_url)

    # URLs to scrape
    urls = [
        f"{base_url}/or/2/pieces-d-or-d-investissement",
        f"{base_url}/or/4/pieces-modernes",
        f"{base_url}/argent/5/pieces-francaises",
        f"{base_url}/argent/80/gros-volume-argent"
    ]

    for url in urls:

        driver = Driver(uc=True, headless=True)
        driver.get(url)

        # Explicitly wait for the target element to be present
        wait = WebDriverWait(driver, 15)  # Adjust timeout as needed
        tableau = wait.until(EC.presence_of_element_located((By.ID, "contentCategVitrine")))
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.row.BStooltip.align-items-center")))

        # Use find_elements to get a list of matching elements
        rows = tableau.find_elements(By.CSS_SELECTOR, "div[id*='prod']")

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
                if isinstance(item_data,tuple):
                    name = item_data[0]
                    quantity = item_data[1]
                    bullion_type = item_data[0][:2]
                else :
                    name=item_data
                    quantity = 1
                    bullion_type = item_data[:2]

                if bullion_type == 'or':
                    buy_price = buy_price_gold
                else :
                    buy_price = buy_price_silver

                price = None
                row_price = row_soup.find('div',class_="row BStooltip align-items-center")

                if row_price :

                    data_content = row_price["data-original-title"]

                    inner_soup = BeautifulSoup(data_content, 'html.parser')

                    quantity_divs = inner_soup.find_all("div", class_="col-6 text-left selected h5") + inner_soup.find_all("div", class_="col-6 text-left h5")  # Get divs with quantity text
                    price_divs = inner_soup.find_all("div", class_="col-6 text-right h5")  # Get divs with price text

                    for qty_div, price_div in zip(quantity_divs,price_divs):  # Skip the first qty div ("Vous achetez")
                        minimum = int(re.search(r"\d+", qty_div.get_text(strip=True)).group())
                        price = Price.fromstring(price_div.get_text(strip=True))

                        print(price, name, source,quantity)
                        if name == 'ar - 50 centimes francs fr semeuse':
                            price= Price.fromstring(str(Price.price.amount_float * quantity) + '€')
                            minimum = quantity

                        coin = Item(name=name,
                                    buy=price.amount_float,
                                    source=source,
                                    buy_premium=(((price.amount_float + get_delivery_price(price.amount_float*minimum)/minimum)/float(quantity)) - (
                                        buy_price * poids_pieces[name])) * 100.0 / (buy_price * poids_pieces[name]),
                                    delivery_fee=get_delivery_price(price.amount_float),
                                    session_id=session_id,
                                    bullion_type=bullion_type,
                                    quantity=quantity,
                                    minimum=minimum)

                        session.add(coin)
                        session.commit()

                else:
                    row_price = row_soup.find('del', class_="small text-dark").parent
                    price = Price.fromstring(row_price.text)

                    print(price,name,source)
                    minimum = 1

                    if name == 'ar - 50 centimes francs fr semeuse':
                        price = Price.fromstring(str(price.amount_float * quantity)+'€')
                        minimum = quantity

                    coin = Item(name=name,
                                buy=price.amount_float,
                                source=source,
                                buy_premium=(((price.amount_float + get_delivery_price(price.amount_float))/float(quantity)) - (
                                             buy_price * poids_pieces[name])) * 100.0 / (buy_price *poids_pieces[name]),
                                delivery_fee=get_delivery_price(price.amount_float),
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum)

                    session.add(coin)
                    session.commit()
            except Exception as e:
                print(f"An error occurred while processing : {e}")
                traceback.print_exc()

    driver.quit()