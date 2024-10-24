import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import re

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
    "https://monlingot.fr/or/achat-piece-or-50-pesos": 'or - 50 pesos mex',
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

    "https://monlingot.fr/piece-argent-Francaise/achat-piece-investissement-argent-10-francs-hercule" : 'ar - 10 francs fr hercule (1965-1973)',  # Assuming this is the intended mapping
    "https://monlingot.fr/piece-argent-Francaise/achat-piece-investissement-argent-5-francs-semeuse" : 'ar - 5 francs fr semeuse (1959-1969)',  # Assuming this is the intended mapping
    "https://monlingot.fr/piece-argent-Francaise/achat-piece-investissement-argent-2-francs-semeuse" : 'ar - 2 francs fr semeuse',  # Assuming this is the intended mapping
    "https://monlingot.fr/piece-argent-Francaise/achat-piece-investissement-argent-1-franc-semeuse" : 'ar - 1 franc fr semeuse',  # Assuming this is the intended mapping
    "https://monlingot.fr/argent/achat-piece-argent-20-francs-turin" : 'ar - 20 francs fr turin (1929-1939)',  # Assuming this is the intended mapping
    "https://monlingot.fr/argent/achat-piece-argent-silver-eagle-1-once" : 'ar - 1 oz silver eagle',  # Assuming this is the intended mapping
    "https://monlingot.fr/argent/achat-piece-argent-maple-leaf-1-once" : 'ar - 1 oz maple leaf',  # Assuming this is the intended mapping
    "https://monlingot.fr/argent/achat-piece-argent-philharmonique-1-once" : 'ar - 1 oz philharmonique',  # Assuming this is the intended mapping
    "https://monlingot.fr/piece-argent-Francaise/Piece-investissement-Argent-50-Francs-Hercule" : 'ar - 50 francs fr hercule (1974-1980)',  # Assuming this is the intended mapping
    "https://monlingot.fr/piece-argent-Francaise/Piece-investissement-Argent-50-Centimes-Semeuse" : 'ar - 50 centimes francs fr semeuse',  # Assuming this is the intended mapping
    "https://monlingot.fr/argent/achat-piece-argent-100-francs" : 'ar - 100 francs fr',  # Assuming this is the intended mapping
    "https://monlingot.fr/argent/achat-boite-piece-argent-500-silver-eagle-1-once" : ('ar - 1 oz silver eagle',500),  # Assuming this is the intended mapping
    "https://monlingot.fr/argent/achat-boite-piece-argent-500-maple-leaf-1-once" : ('ar - 1 oz maple leaf',500),  # Assuming this is the intended mapping
    "https://monlingot.fr/piece-argent-Francaise/achat-piece-investissement-argent-5-francs-ecu" : 'ar - 5 francs fr ecu (1854-1860)',  # Assuming this is the intended mapping
}

def get_delivery_price(price):
    #https://monlingot.fr/conseil/livraison
    if price < 2500 :
        return 9.90 # Not available for higher values
    elif 2500 <= price < 20000 :
        return 39.90
    else:
        return 0.0

#https://monlingot.fr/conseil/livraison
def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    for url, item_data in urls.items() :
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            products_table = soup.find('table',class_='table-product-discounts')
            products_tbody = products_table.find('tbody')

            quantity = 1

            if isinstance(item_data, tuple):
                name = item_data[0]
                quantity = item_data[1]
                bullion_type = item_data[0][:2]
            else:
                name = item_data
                bullion_type = item_data[:2]

            if bullion_type == 'or':
                buy_price = buy_price_gold
            else:
                buy_price = buy_price_silver

            # Find the tr element based on its attributes
            tr_elements = products_tbody.find_all('tr')
            for tr in tr_elements:
            # Extract all td elements within the tr

                td_elements = tr.find_all('td')
                minimum = int(re.search(r"\d+", td_elements[0].text).group())

                min_p = int(soup.find('input', id='quantity_wanted')['min'])
                if min_p>minimum:
                    minimum = min_p

                current_price = Price.fromstring(soup.find('div',class_='current-price').text)
                discount_price = Price.fromstring(td_elements[1].text)
                if current_price.amount_float < discount_price.amount_float and soup.find('div',class_='discount-block').find('span',class_='discount') :
                    price = current_price
                else :
                    price = discount_price
                print(price, name, url)
                coin = Item(name=name,
                            prices=price.amount_float,
                            source=url,
                            buy_premiums=(((price.amount_float + get_delivery_price(
                                price.amount_float) / minimum) / float(quantity)) - (
                                                 buy_price * poids_pieces[name])) * 100.0 / (
                                                buy_price * poids_pieces[name]),

                            delivery_fee=get_delivery_price(price.amount_float*minimum),
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=quantity,
                            minimum=minimum)

                session.add(coin)
                session.commit()

        except Exception as e:
            print(traceback.format_exc())