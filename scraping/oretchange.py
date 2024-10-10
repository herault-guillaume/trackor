import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces
from price_parser import Price
import traceback

# https://www.oretchange.com/content/1-livraison
coin_name = {
    "20 Francs Coq Or": 'or - 20 francs fr coq marianne',
    "20 Francs Napoléon Or": 'or - 20 francs fr napoléon III',
    "Souverain Or Victoria ou Edouard VII ou George V": 'or - 1 souverain georges V',
    "20 Francs Suisse Vrénéli ou Confédération": 'or - 20 francs sui',
    "20 Francs Union Latine": 'or - 20 francs union latine',
    "50 Pesos Mexique": 'or - 50 pesos',
    "Krugerrand Or": 'or - 1 oz krugerrand',
    "20 Dollars Or": 'or - 20 dollars',
    "10 Dollars Or Liberté ou Tête d’indien": 'or - 10 dollars liberté',
    "5 Dollars Or Liberté ou Tête d'indien": 'or - 5 dollars liberté',
    "10 Francs Napoléon III": 'or - 10 francs fr napoléon III',
    "Demi-souverain Or Victoria, Edouard VII ou George V": 'or - 1/2 souverain georges V'
}

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    url = "https://www.oretchange.com/15-pieces-or"
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the span element with class "result2"
    products_div = soup.find_all("article")

    for product in products_div:
        try:

            tr_description = product.find('table',class_='metal_product').find_all('tr')

            price_text = ''

            if len(tr_description) == 3:
                price_text = tr_description[2].find_all('td')[0].text
            else :
                price_text = tr_description[0].find('td').text

            price = Price.fromstring(price_text)
            name_title = product.find("h5", "product-name")
            name = name_title.text.strip()
            url = name_title.find('a')['href']

            print(price,coin_name[name],url)

            if coin_name[name][:2] == 'or':
                coin = CoinPrice(nom=coin_name[name],
                                 j_achete=price.amount_float,
                                 source=url,
                                 prime_achat_perso=((price.amount_float + 0.0) - (buy_price * poids_pieces[coin_name[name]])) * 100.0 / (buy_price * poids_pieces[coin_name[name]]),
                                 frais_port=0.0,session_id=session_id,metal='g')
            session.add(coin)
            session.commit()

        except Exception as e:
            print(traceback.format_exc())