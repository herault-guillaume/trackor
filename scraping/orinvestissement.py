import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

coin_name = {
    "Pièce Or 20 Francs Marianne Coq": '20 francs or fr coq marianne',
    "Pièce Or 20 Francs Napoléon III": '20 francs or fr napoléon III',
    "Pièce Or 20 Francs Suisse": '20 francs or sui vreneli croix suisse',  # Assuming "Suisse" refers to the Vreneli coin
    "Pièce Or 10 Dollars US": '10 dollars or liberté',  # Assuming "Liberté" is the most common 10 dollar US gold coin
    "Pièce Or 20 Dollars US": '20 dollars or liberté',  # Similar assumption as above
    "Pièce Or Union Latine": '20 francs or union latine',  # Assuming the most common Union Latine coin
    "Pièce Or 50 Pesos": '50 pesos or',
    "Pièce Or Souverain": 'souverain or elizabeth II',  # Assuming the most recent monarch
    "Pièce Or Krugerrand": '1 oz krugerrand',
    "Pièce Or 100 Francs Napoléon III": '100 francs or fr napoléon III tête nue',
    "Pièce Or 50 Francs Napoléon III": '50 francs or fr napoléon III tête nue',
    "Pièce Or 5 Dollars US": '5 dollars or liberté',  # Same assumption as for 10 dollars
    "Pièce Or 20 Francs Génie": '20 francs or fr génie debout',
    "Pièce Or 20 Mark Allemande": '20 mark or wilhelm II'
}

# https://or-investissement.fr/information-or-investissement/1-livraison-achat-or-investissement
def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Or-Investissement using requests and BeautifulSoup.
    """
    url = 'https://or-investissement.fr/12-achat-piece-or-investissement'
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the span element with class "result2"
    products_div = soup.find_all("article")

    for product in products_div:
        try:
            price_text = product.find('span','product-price').text

            price = Price.fromstring(price_text)
            name_title = product.find("h3", "h3 product-title")
            url = name_title.find('a')['href']

            name = name_title.text.strip()

            print(price,coin_name[name],url)

            #price = float(price_text.replace('€', '').replace(',', '.'))
            coin = CoinPrice(nom=coin_name[name],
                             j_achete=price.amount_float,
                             prime_achat_perso=((price.amount_float + 25.0) - (
                                     buy_price * poids_pieces_or[coin_name[name]])) * 100.0 / (buy_price *
                                               poids_pieces_or[coin_name[name]]),
                             source=url,
                             frais_port=25.0,session_id=session_id,metal='g')
            session.add(coin)
            session.commit()

        except Exception as e:
            print(traceback.format_exc())