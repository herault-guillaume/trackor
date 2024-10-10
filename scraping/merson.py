import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces
from price_parser import Price
import traceback

coin_name = {
    "20 Francs Or Napoléon type Coq": 'or - 20 francs fr coq marianne',
    "Souverain Or Georges": 'or - 1 souverain georges V',
    "50 Pesos Or Mexique": 'or - 50 pesos',
    "Krugerrand Or Afrique du Sud": 'or - 1 oz krugerrand',
    "20 Francs Or Suisse": 'or - 20 francs sui vreneli croix',
    "20 Dollars Or": 'or - 20 dollars liberté longacre',
    "10 Dollars Or": 'or - 10 dollars liberté',
    "10 Francs Or": 'or - 10 francs fr coq marianne',
    "20 Francs Union Latine Or": 'or - 20 francs union latine',
    "10 Florins Or Hollandais": 'or - 10 florins wilhelmina', # or 'or - 10 florins willem III' depending on the specific coin
    "20 Francs Or Tunisie": 'or - 20 francs tunisie',
    "Souverain Elisabeth  II Or": 'or - 1 souverain elizabeth II',
    "1/2 Souverain Or": 'or - 1/2 souverain georges V', # or 'or - 1/2 souverain victoria' depending on the specific coin
    "5 Dollars Or": 'or - 5 dollars liberté',
    "20 Marks Or": 'or - 20 mark wilhelm II',
    "Lingot Or 1 kg": 'or - lingot 1 kg LBMA',
    "Lingotin Or 500 grammes": 'or - lingot 500 g LBMA',
    "Lingotin Or  250 grammes": 'or - lingot 250 g LBMA',
    "Lingotin Or 100 grammes": 'or - lingot 100 g LBMA',
    "Lingotin Or 50 grammes": 'or - lingot 50 g LBMA',
    "Lingotin Or 20 grammes": 'or - lingot 20 g LBMA',
    "Lingotin Or 10 grammes": 'or - lingot 10 g LBMA',
    "Lingotin Or 5 grammes": 'or - lingot 5 g LBMA',
    "Lingotin Once Or": 'or - lingot 1 once LBMA',
    "Lingotin Or 2 Grammes": "or - lingot 2 g", # Assuming this is the intended match, adjust if needed
    "Lingotin Or 1 Gramme": "or - lingot 1 g"
}

def get_delivery_price(price):
    if price <= 2000.0 :
        return 8.9
    elif price > 2000.0 :
        return 18.90


# https://www.merson.fr/fr/content/1-livraison
def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    url = "https://www.merson.fr/fr/18-achat-or-investissement"
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the span element with class "result2"
    products_div = soup.find_all("div",'product-container')

    for product in products_div:
        try:
            price = Price.fromstring(product.find("span", "price product-price").text)
            name_title = product.find("h5", "product-name")
            name = name_title.text.strip()
            url = name_title.find('a')['href']
            print(price,coin_name[name],url)

            if coin_name[name][:2] == 'or':
                coin = CoinPrice(nom=coin_name[name],
                                 j_achete=price.amount_float,
                                 prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                             buy_price * poids_pieces[coin_name[name]])) * 100.0 / (buy_price * poids_pieces[
                                                       coin_name[name]]),

                                 source=url,
                                 frais_port=get_delivery_price(price.amount_float),session_id=session_id,metal='g')
            session.add(coin)
            session.commit()

        except Exception as e:
            print(traceback.format_exc())