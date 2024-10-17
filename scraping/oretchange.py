import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import re

# https://www.oretchange.com/content/1-livraison
CMN = {
    "https://www.oretchange.com/pieces-or/196-achat-20-francs-coq.html": 'or - 20 francs fr coq marianne',
    "https://www.oretchange.com/pieces-or/176-achat-20-francs-napoleon-iii.html": 'or - 20 francs fr napoléon III',
    "https://www.oretchange.com/pieces-or/200-achat-souverain-victoria.html": 'or - 1 souverain georges V',
    "https://www.oretchange.com/pieces-or/198-achat-20-francs-suisse-confederation.html": 'or - 20 francs sui',
    "https://www.oretchange.com/pieces-or/179-achat-20-francs-union-latine.html": 'or - 20 francs union latine',
    "https://www.oretchange.com/pieces-or/182-achat-50-pesos-mexique.html": 'or - 50 pesos mex',
    "https://www.oretchange.com/pieces-or/186-achat-krugerrand-afrique-du-sud.html": 'or - 1 oz krugerrand',
    "https://www.oretchange.com/pieces-or/175-achat-20-dollars-liberte.html": 'or - 20 dollars',
    "https://www.oretchange.com/pieces-or/202-achat-10-dollars-tete-d-indien.html": 'or - 10 dollars liberté',
    "https://www.oretchange.com/pieces-or/180-achat-5-dollars-liberte.html": 'or - 5 dollars liberté',
    "https://www.oretchange.com/pieces-or/172-682132-achat-10-francs-napoleon-iii.html#/28-achat_or-achat_au_gre_a_gre": 'or - 10 francs fr napoléon III',
    "https://www.oretchange.com/pieces-or/170-682147-achat-demi-souverain-victoria.html#/28-achat_or-achat_au_gre_a_gre": 'or - 1/2 souverain georges V',

    "https://www.oretchange.com/pieces-d-argent-francaises/194-achat-50-francs-hercule.html": 'ar - 50 francs fr hercule (1974-1980)',
    "https://www.oretchange.com/pieces-d-argent-francaises/195-achat-5-francs-ecu.html": 'ar - 5 francs fr ecu (1854-1860)',
    "https://www.oretchange.com/pieces-d-argent-francaises/207-achat-100-francs-pantheon.html": 'ar - 100 francs fr',
    "https://www.oretchange.com/pieces-d-argent-francaises/192-achat-20-francs-turin.html": 'ar - 20 francs fr turin (1860-1928)',
    "https://www.oretchange.com/pieces-d-argent-francaises/190-achat-10-francs-turin.html": 'ar - 10 francs fr turin (1860-1928)',
    "https://www.oretchange.com/pieces-d-argent-francaises/193-achat-5-francs-semeuse.html": 'ar - 5 francs fr semeuse (1959-1969)',
    "https://www.oretchange.com/pieces-d-argent-internationales/208-achat-maple-leaf-1-once-argent.html" : 'ar - 1 oz maple leaf',
    "https://www.oretchange.com/pieces-d-argent-internationales/209-achat-silver-eagle-1-once-argent.html" : 'ar - 1 oz silver eagle',
    "https://www.oretchange.com/pieces-d-argent-internationales/210-achat-philharmonique-1-once-argent.html" : 'ar - 1 oz philharmonique',
    "https://www.oretchange.com/pieces-d-argent-internationales/217-achat-panda-1-once-argent.html" : 'ar - 10 yuan panda 30g',
    "https://www.oretchange.com/pieces-d-argent-internationales/253-kangourou-1-once-argent.html" : 'ar - 1 oz nugget / kangourou',



}

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """

    print("https://www.oretchange.com/")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    for url, item_data in CMN.items():
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        try:

            quantity = 1
            minimum = 1

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

            minimum = int(soup.find('input', class_='qty')['value'])
            unique_price = soup.find('div',class_='metal_product').find('b')

            if unique_price:
                price = Price.fromstring(unique_price.text)
                print(price,name,url)
                coin = Item(name=name,
                            buy=price.amount_float,
                            source=url,
                            buy_premium=(((price.amount_float + (0.0 * minimum) / minimum) / float(quantity)) - (
                                                 buy_price * poids_pieces[name])) * 100.0 / (
                                                    buy_price * poids_pieces[name]),

                            delivery_fee=0.0,
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=quantity,
                            minimum=minimum)
                session.add(coin)
                session.commit()

            else:
                rows = soup.find('table',class_='table table-bordered').find('tbody').find_all('tr')
                values = [row.find_all('td') for row in rows]

                for v in values:
                    minimum = int(re.search(r"\d+", v[0].text).group())
                    price = Price.fromstring(v[1].text)
                    print(price, name, url)
                    coin = Item(name=name,
                                buy=price.amount_float,
                                source=url,
                                buy_premium=(((price.amount_float + (0.0 * minimum) / minimum) / float(quantity)) - (
                                        buy_price * poids_pieces[name])) * 100.0 / (
                                                    buy_price * poids_pieces[name]),

                                delivery_fee=0.0,
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum)

                    session.add(coin)
                    session.commit()

        except Exception as e:
            print(traceback.format_exc())