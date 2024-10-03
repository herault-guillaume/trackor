import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

coin_name = {
    "20 Francs Or Napoléon type Coq": '20 francs or coq marianne',
    "Souverain Or Georges": 'souverain or georges V',
    "50 Pesos Or Mexique": '50 pesos or',
    "Krugerrand Or Afrique du Sud": '1 oz krugerrand',
    "20 Francs Or Suisse": '20 francs or vreneli croix suisse',
    "20 Dollars Or": '20 dollars or liberté',
    "10 Dollars Or": '10 dollars or liberté',
    "10 Francs Or": '10 francs or coq marianne',
    "20 Francs Union Latine Or": '20 francs or union latine léopold II',
    "10 Florins Or Hollandais": '10 florins or wilhelmina', # or '10 florins or willem III' depending on the specific coin
    "20 Francs Or Tunisie": '20 francs or tunisie',
    "Souverain Elisabeth  II Or": 'souverain or elizabeth II',
    "1/2 Souverain Or": '1/2 souverain georges V', # or '1/2 souverain victoria' depending on the specific coin
    "5 Dollars Or": '5 dollars or liberté',
    "20 Marks Or": '20 mark or wilhelm II',
    "Lingot Or 1 kg": 'Lingot or 1 kg LBMA',
    "Lingotin Or 500 grammes": 'Lingot or 500 g LBMA',
    "Lingotin Or  250 grammes": 'Lingot or 250 g LBMA',
    "Lingotin Or 100 grammes": 'Lingot or 100 g LBMA',
    "Lingotin Or 50 grammes": 'Lingot or 50 g LBMA',
    "Lingotin Or 20 grammes": 'Lingot or 20 g LBMA',
    "Lingotin Or 10 grammes": 'Lingot or 10 g LBMA',
    "Lingotin Or 5 grammes": 'Lingot or 5 g LBMA',
    "Lingotin Once Or": 'Lingot or 1 once LBMA',
    "Lingotin Or 2 Grammes": "Lingot or 2 g", # Assuming this is the intended match, adjust if needed
    "Lingotin Or 1 Gramme": "Lingot or 1 g"
}

def get_delivery_price(price):
    if price <= 2000.0 :
        return 8.9
    elif price > 2000.0 :
        return 18.90


# https://www.merson.fr/fr/content/1-livraison
def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
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
            print(name,price)

            #price = float(price_text.replace('€', '').replace(',', '.'))
            coin = CoinPrice(nom=coin_name[name],
                             j_achete=price.amount_float,
                             prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                         buy_price * poids_pieces_or[coin_name[name]])) * 100.0 / (buy_price * poids_pieces_or[
                                                   coin_name[name]]),

                             source=url,
                             frais_port=get_delivery_price(price.amount_float),session_id=session_id,metal='g')
            session.add(coin)
            session.commit()

        except Exception as e:
            print(traceback.format_exc())