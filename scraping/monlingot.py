import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

urls = {
    "https://monlingot.fr/or/achat-piece-or-20-francs-napoleon": 'or - 20 francs fr napoléon III',
    "https://monlingot.fr/or/achat-piece-or-american-eagle-1-once": 'or - 1 oz american eagle',
    "https://monlingot.fr/or/achat-lingotin-or-5-grammes": 'or - lingot 5 g LBMA',
    "https://monlingot.fr/or/achat-piece-or-10-francs-napoleon": 'or - 10 francs fr napoléon III',
    "https://monlingot.fr/or/achat-piece-or-buffalo-1-once": 'or - 1 oz buffalo',
    "https://monlingot.fr/or/achat-lingotin-or-10-grammes": 'or - lingot 10 g LBMA',
    "https://monlingot.fr/or/achat-piece-or-20-dollars-us": 'or - 20 dollars liberté longacre',
    "https://monlingot.fr/or/achat-piece-or-maple-leaf-1-once": 'or - 1 oz maple leaf',
    "https://monlingot.fr/or/achat-lingotin-or-20-grammes": 'or - lingot 20 g LBMA',
    "https://monlingot.fr/pieces-or-americaines/achat-piece-or-investissement-10-dollars-us": 'or - 10 dollars liberté',
    "https://monlingot.fr/or/achat-piece-or-philharmonique-1-once": 'or - 1 oz philharmonique',
    "https://monlingot.fr/or/achat-lingotin-1-onces-311-gr": 'or - lingot 1 once LBMA',
    "https://monlingot.fr/or/achat-lingotin-or-50-grammes": 'or - lingot 50 g LBMA',
    "https://monlingot.fr/or/achat-piece-or-5-dollars-us": 'or - 5 dollars liberté',
    "https://monlingot.fr/or/achat-piece-or-demi-souverain": 'or - 1/2 souverain georges V',  # Assuming Georges V based on your data
    "https://monlingot.fr/pieces-or-modernes/nugget-1-once-d-or": 'or - 1 oz nugget / kangourou',
    "https://monlingot.fr/or/achat-lingotin-or-100-grammes": 'or - lingot 100 g LBMA',
    "https://monlingot.fr/or/achat-piece-or-50-pesos": 'or - 50 pesos',
    "https://monlingot.fr/or/lingot-or-500-grammes": 'or - lingot 500 g LBMA',
    "https://monlingot.fr/or/achat-piece-or-souverain": 'or - 1 souverain elizabeth II',  # Assuming Elizabeth II based on your data
    "https://monlingot.fr/or/achat-lingot-or-1-Kilo": 'or - lingot 1 kg LBMA',
    "https://monlingot.fr/or/achat-lingot-or-250-grammes": 'or - lingot 250 g LBMA',
    "https://monlingot.fr/pieces-or/Piece-investissement-Or-20-Reichsmark": 'or - 20 mark wilhelm II',
    "https://monlingot.fr/pieces-or/10-florins-or": 'or - 10 florins wilhelmina',  # Assuming Wilhelmina based on your data
    "https://monlingot.fr/pieces-or/Piece-investissement-Or-Union-Latine": 'or - 20 francs union latine',
    "https://monlingot.fr/or/achat-piece-or-20-francs-suisse": 'or - 20 francs sui confederatio',
    "https://monlingot.fr/or/achat-piece-or-krugerrand-1-once": 'or - 1 oz krugerrand',
    "https://monlingot.fr/or/achat-piece-or-20-francs-coq-marianne": 'or - 20 francs fr coq marianne',
    "https://monlingot.fr/or/achat-piece-or-britannia-1-once" : 'or - 1 oz britannia',  # Assuming this is the intended mapping
    #"https://monlingot.fr/or/achat-piece-or-leon-1-once": None,  # No direct match in your original data
    #"Lhttps://monlingot.fr/or/achat-piece-or-leon-1-10-once": None   # No direct match in your original data
}

def get_delivery_price(price):
    #https://monlingot.fr/conseil/livraison
    if price < 2500 :
        return 9.90 # Not available for higher values
    elif 2500 <= price < 20000 :
        return 19.90
    else:
        return 0.0

#https://monlingot.fr/conseil/livraison
def get_price_for(session,session_id,buy_price):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    for url, coin_name in urls.items() :
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            products_div = soup.find_all("article")
            # Find the tr element based on its attributes
            tr_element = soup.find('tr', {'data-discount-type': 'percentage', 'data-discount': '0',
                                          'data-discount-quantity': '1'})

            # Extract all td elements within the tr
            td_elements = tr_element.find_all('td')

            # Get the second td (index 1)
            second_td = td_elements[1]

            price = Price.fromstring(second_td.text)
            print(price,coin_name,url)

            if coin_name[:2] == 'or':
                coin = CoinPrice(nom=coin_name,
                                 j_achete=price.amount_float,
                                 source=url,
                                 prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                         buy_price * poids_pieces_or[coin_name])) * 100.0 / (buy_price *poids_pieces_or[coin_name]),
                                 frais_port=get_delivery_price(price.amount_float),session_id=session_id,metal='g')
            session.add(coin)
            session.commit()


        except Exception as e:
            print(traceback.format_exc())