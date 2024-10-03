import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

coin_mapping = {
    "20 Francs Napoléon": "20 francs or fr",
    "20 Francs Suisse": "20 francs or vreneli croix suisse",
    "Union Latine": "20 francs or union latine léopold II",
    "Souverain": "souverain or elizabeth II",
    "Demi Souverain": "1/2 souverain georges V",
    "50 Pesos": "50 pesos or",
    "10 Francs Napoléon": "10 francs or napoléon III",
    "Krugerrand": "1 oz krugerrand",
    "10 Dollars US": "10 dollars or liberté",
    "5 Dollars US": "5 dollars or liberté",
    "20 Reichsmarks": "20 mark or wilhelm II",
    "10 Florins": "10 florins or wilhelmina",
    "Maple Leaf Or 1 OZ": "1 oz maple leaf",
    "American Eagle 1 OZ": "1 oz american eagle",
    "Philharmonique 1 OZ": "1 oz philharmonique",
    "American Buffalo 1 OZ": "1 oz buffalo",
    "Nugget 1 OZ": "1 oz nugget / kangourou",
    '20 Dollars US' : '20 dollars or liberté',
    '20 Francs Marianne...' : '20 francs or coq marianne',
    '10 Francs Napoléon...' : '10 francs or coq marianne',
    'Britannia 1 OZ Or' : '1 oz britannia',
}
def get_delivery_price(price):
    #https://www.changerichelieu.fr/livraison
    if price <= 600.0:
        return 10.0
    elif 600.0 < price <= 2500.0 :
        return 20.0
    elif 2500.0 < price <= 5000.0 :
        return 34.0
    elif 5000.0 < price <= 7500.0 :
        return 50.0
    elif 7500.0 < price <= 10000.0 :
        return 56.0
    elif 10000.0 < price <= 15000.0 :
        return 65.0
    else :
        return 0.0

def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    url = "https://www.changevivienne.com/or"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    target_divs = soup.find_all('div', class_='cv-table-block cv-table-block-item')

    for div in target_divs:
        try :
            # Extract price
            price_element = div.find('p', class_='price product-price')
            price = Price.fromstring(price_element.text.strip())

            # Extract product name
            product_name_element = div.find('a', class_='product-name product_name_grand')
            product_name = product_name_element.text.strip()

            print(product_name,price)
            # Clean the price text
            #price = float(price_text.replace('€', '').replace(',', '.').replace('net',''))
            coin = CoinPrice(nom=coin_mapping[product_name],
                             j_achete=price.amount_float,
                             source=url,
                             prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                         buy_price * poids_pieces_or[ coin_mapping[product_name]])) * 100.0 / (buy_price * poids_pieces_or[
                                                   coin_mapping[product_name]]),

                             frais_port=get_delivery_price(price.amount_float),session_id=session_id,metal='g')
            session.add(coin)
            session.commit()


        except Exception as e:
            print(traceback.format_exc())
