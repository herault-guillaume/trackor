import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

coin_to_name = {
    "20 Francs Or Coq": '20 francs or fr coq marianne',
    "20 Francs Or Napoléon III": '20 francs or fr napoléon III',
    "20 Francs Or Génie": '20 francs or fr génie debout',
    "20 Francs Or Vreneli": '20 francs or sui vreneli croix suisse',
    "20 Francs Or Leopold 2": '20 francs or union latine',
    "Souverain Or": 'souverain or elizabeth II',  # Assuming you want Elizabeth II
    "Souverain Or Elizabeth II": 'souverain or elizabeth II',
    "Krugerrand Or": '1 oz krugerrand',
    "Maple Leaf Or": '1 oz maple leaf',
    "Philharmonique Or": '1 oz philharmonique',
    "50 Pesos Or": '50 pesos or',
    "20 Dollars Or Liberty": '20 dollars or liberté longacre',
    "20 Dollars Or St Gaudens": '20 dollars or liberté st gaudens', # Assuming St Gaudens is similar to Liberty
    "10 Dollars Or Liberty": '10 dollars or liberté',
    "American Buffalo Once": '1 oz buffalo',
    "American Eagle Once": '1 oz american eagle',
    "5 Roubles Or": '5 roubles or',
    "20 Mark Or": '20 mark or wilhelm II',
    #"5 Roubles Or": None  # No match found in the gold prices dictionary
}

#via panier
def get_price_for(session,session_id,buy_price):
    url = 'https://lcdor.fr/achat-or/pieces-dor/'
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic browser behavior

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the price element:
    products_div = soup.find_all("div",class_="product-wrapper")

    for product in products_div :
        try:
            price = Price.fromstring(product.find("span","price").text)
            name_title = product.find("h3","wd-entities-title")
            name = name_title.text
            url = name_title.find('a')['href']
            print( price,coin_to_name[name],url)
            #price = float(price_text.replace('€', '').replace(',', '.'))

            coin = CoinPrice(nom=coin_to_name[name],
                             j_achete=price.amount_float,
                             source=url,
                             prime_achat_perso=((price.amount_float + 7.0) - (
                                         buy_price * poids_pieces_or[coin_to_name[name]])) * 100.0 / (buy_price * poids_pieces_or[
                                                   coin_to_name[name]]),

                             frais_port=7.0,session_id=session_id,metal='g')
            session.add(coin)
            session.commit()


        except Exception as e:
            print(traceback.format_exc())