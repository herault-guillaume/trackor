import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import Price
import traceback


coin_name = {
    "1 ducat autrichien or diverses années": '1 ducat or',
    "Kangourou 1 OZ or diverses années": '1 oz nugget / kangourou',
    "Kangourou 1/2 OZ or diverses années": '1/2 oz nugget / kangourou',
    "Kangourou 1/10 OZ or diverses années": '1/10 oz nugget / kangourou',
    #"Lunar 1/4 OZ or diverses années": '1/4 oz nugget / kangourou',
    #"Lunar 1/10 OZ or diverses années": '1/10 oz nugget / kangourou',
    "50 ECU Belgique diverses années": '50 écus or charles quint',
    "100 ECU Belgique diverses années": '100 écus or charles quint',
    "10 francs français or diverses années": '10 francs or coq marianne',
    "Aigle américain 1/2 OZ or diverses années": '1/2 oz american eagle',
    "Aigle américain 1/10 OZ or diverses années": '1/10 oz american eagle',
    "5 dollars USA or diverses années": '5 dollars or liberté',
    "10 dollars USA or diverses années": '10 dollars or liberté',
    "1 rand sud-africains or diverses années": '1 rand sud-africains or',
    #"2 rands sud-africains or diverses années": '20 rands',
    "Nugget en or 1 once troy années diverses": '1 oz nugget / kangourou',
    "Ducat simple d'or néerlandais diverses années": '1 ducat or',
    #"Panda en or 15gr 2024": 'Lingot or 15 g',
    #"Panda en or 30gr 2024": 'Lingot or 30 g',
    #"Panda en or 8gr 2024": 'Lingot or 8 g',
    "Kangourou 1/2 OZ or 2024": '1/2 oz nugget / kangourou',
    "Kangourou 1/4 OZ or 2024": '1/4 oz nugget / kangourou',
    "Kangourou 1/10 OZ or 2024": '1/10 oz nugget / kangourou',
    "Kangourou 1 OZ or 2024": '1 oz nugget / kangourou',
    #'Lunar 1 OZ or 2024': '1 oz nugget / kangourou',
    #'Lunar 1/2 OZ or 2024': '1/2 oz nugget / kangourou',
    #'Lunar 1/4 OZ or 2024': '1/4 oz nugget / kangourou',
    #'Lunar 1/10 OZ or 2024': '1/10 oz nugget / kangourou',
    '100 Corona en or diverses années': '100 couronnes or françois joseph I',
    #"Feuille d'Érable 25 x 1 gramme or diverses années": 'Lingot or 25 g LBMA',
    #'100 Dollars Canada or diverses années': '100 Dollars Canada or diverses années',
    #'Aigle américain 1 OZ or 2023': '1 oz american eagle',
    #'Aigle américain 1/4 OZ or 2023': '1/4 oz american eagle',
    #'Gouden American Eagle 1/2 OZ 2023': '1/2 oz american eagle',
    #'Aigle américain 1/10 OZ or 2023': '1/10 oz american eagle',
    #'Brittannia 1oz or 2024': '1 oz britannia',
    #'Brittannia 1/2oz or 2024': '1/2 oz krugerrand',
    #"Feuille d'Érable 1/2 OZ or 2024": '1/2 oz maple leaf',
    #"Feuille d'Érable 1/4 OZ or 2024": '1/4 oz maple leaf',
    #'Philharmonique 1/4 OZ or 2024': '1/4 oz nugget / kangourou',
    #'Philharmonique 1/2 OZ or 2024': '1/2 oz nugget / kangourou',
    #'Krugerrand 1/10 OZ or 2024': '1/10 oz krugerrand',
    ##'Krugerrand 1/4 OZ or 2024': '1/4 oz krugerrand',
    #'Brittannia 1/4 oz or 2024': '1/4 oz krugerrand',
    "1/2 Souverain d'or / Livre diverses années": '1/2 souverain georges V',
}

# def get_delivery_price(url="https://www.shop-comptoirdelor.be/info/livraison"):
#     """
#     Extracts shipping and administrative fees from the last row of a delivery price table.
#
#     Args:
#         url: The URL of the webpage containing the table.
#
#     Returns:
#         A tuple containing the shipping fee (str) and the administrative fee (str),
#         or None if the values cannot be extracted.
#     """
#
#     try:
#         # Fetch the webpage content
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error if the request fails
#
#         # Parse the HTML with BeautifulSoup
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         # Find the table based on its class
#         table = soup.find('table', class_='MsoNormalTable')
#
#         # If the table is found, get all rows and select the last one
#         if table:
#             rows = table.find_all('tr')
#             last_row = rows[-2]
#
#             # If the last row has enough cells (columns), get the desired values
#             if len(last_row.find_all('td')) >= 5:
#                 shipping_fee = float(last_row.find_all('td')[3].get_text(strip=True).replace('€ ','').replace('*','').replace(',','.'))
#                 admin_fee = float(last_row.find_all('td')[4].get_text(strip=True).replace('€ ','').replace('*','').replace(',','.'))
#                 return shipping_fee + admin_fee
#
#         # Return None if the table or values are not found
#         return -1.0
#
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred while fetching the data: {e}")
#         return None

def get_price_for(session, session_id,buy_price):
    """
    Retrieves coin purchase prices from Orobel using Selenium.
    """

    urls = ["https://www.shop-comptoirdelor.be/achat-or/pieces?page=1",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=2",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=3",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=4",
            "https://www.shop-comptoirdelor.be/achat-or/pieces?page=5"]

    print(urls)
    driver = Driver(uc=True, headless=True)

    for url in urls:
        try :
            driver.get(url)

            # Wait for the products to load (adjust the timeout as needed)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.row"))
            )

            # Find the product divs
            products_div = driver.find_elements(By.CSS_SELECTOR, "div.row")

            for product in products_div:
                try:
                    price_text = product.find_element(By.CSS_SELECTOR, 'div.article-price').text
                    price = Price.fromstring(price_text)

                    name_title = product.find_element(By.CSS_SELECTOR, "a.card-content-title")
                    url = name_title.get_attribute('href')
                    name = name_title.text.strip()

                    print(name)

                    #Check if the name is in your coin_name dictionary
                    if name in coin_name:
                        coin = CoinPrice(
                            nom=coin_name[name],
                            j_achete=price.amount_float,
                            source=url,
                            prime_achat_perso=((price.amount_float +24.95) - (
                                    buy_price * poids_pieces_or[coin_name[name]])) * 100.0 / (buy_price *
                                              poids_pieces_or[coin_name[name]]),
                            frais_port=24.95,
                            session_id=session_id
                        )
                        session.add(coin)
                        session.commit()

                except Exception as e:
                    pass
                    #print(traceback.format_exc())
        except Exception as e:
            pass
            # print(traceback.format_exc())