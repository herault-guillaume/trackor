import requests
from bs4 import BeautifulSoup
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice, poids_pieces
from price_parser import Price
import traceback

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
    #'Set 5 pièces 20 Fr Or Marianne Coq': None,  # No exact match
    #'Set 5 Pièces 20 Francs Or': 'or - 20 francs',
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
    '50 Cts Semeuse 1897 - 1920': 'ar - 50 centimes francs fr semeuse',
    '100 Francs Argent 1982 - 2002': 'ar - 100 francs fr',
    '20 Francs Turin 1929 - 1939': 'ar - 20 francs fr turin (1929-1939)',
    '50 Francs Hercule 1974 - 1980': 'ar - 50 francs fr hercule (1974-1980)',
    '10 Francs Hercule 1964 - 1973': 'ar - 10 francs fr hercule (1965-1973)',
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
    """Retrieves coin purchase prices using SeleniumBase."""
    print("https://www.achat-or-et-argent.fr/")

    for url in ["https://www.achat-or-et-argent.fr/or/2/pieces-d-or-d-investissement",
                'https://www.achat-or-et-argent.fr/or/4/pieces-modernes',
                'https://www.achat-or-et-argent.fr/argent/5/pieces-francaises']:

        driver = Driver(uc=True, headless=True)
        driver.get(url)

        # Explicitly wait for the target element to be present
        wait = WebDriverWait(driver, 5)  # Adjust timeout as needed
        tableau = wait.until(EC.presence_of_element_located((By.ID, "contentCategVitrine")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.BStooltip.align-items-center")))

        # Use find_elements to get a list of matching elements
        rows = tableau.find_elements(By.CSS_SELECTOR, "div[id*='prod']")
        for row in rows:
            try:

                # Wait for the 'a' tag to be present within the row
                WebDriverWait(driver, 10).until(
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
                price = None

                row_price = row_soup.find('div',class_="row BStooltip align-items-center")
                if row_price :
                    data_content = row_price["data-original-title"]


                    inner_soup = BeautifulSoup(data_content, 'html.parser')
                    target_cells = inner_soup.find_all('div', class_='col-6 text-left selected h5')


                    for cell in target_cells:
                        if '€' in cell.find_next_sibling('div').text:
                            price = Price.fromstring(cell.find_next_sibling('div').text.strip())
                            break  # Exit loop once price is found


                else:
                    row_price = row_soup.find('del', class_="small text-dark").parent
                    price = Price.fromstring(row_price.text)

                print(price,CMN[product_name],source)

                if CMN[product_name][:2] == 'or':
                    metal ='g'
                    buy_price = buy_price_gold
                else :
                    metal = 's'
                    buy_price = buy_price_silver
                coin = CoinPrice(nom=CMN[product_name],
                                 j_achete=price.amount_float,
                                 source=source,
                                 prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                         buy_price * poids_pieces[CMN[product_name]])) * 100.0 / (buy_price *poids_pieces[CMN[product_name]]),

                                 frais_port=get_delivery_price(price.amount_float), session_id=session_id,metal='g')
                session.add(coin)
                session.commit()

            except Exception as e:
                #print(f"An error occurred while processing {url}: {e}")
                traceback.print_exc()