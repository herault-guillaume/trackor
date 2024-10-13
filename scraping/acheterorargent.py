import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from datetime import datetime
import traceback
from price_parser import Price

header_achat_or_argent_map_model = {
    'Nom': 'name',
    'AchatVous vendez': 'sell',
    'VenteVous achetez': 'buy',
}

def get_delivery_price(price):
    if price < 500:
        return 18.0
    elif price < 1000:
        return 15.0
    elif price < 3000:
        return 20.0
    elif price < 10000:
        return 30.0
    elif price < 20000:
        return 45.0
    elif price < 50000:
        return 90.0
    elif price < 75000:
        return 150.0
    elif price < 100000:
        return 180.0
    elif price < 150000:
        return 240.0
    else:
        return 0.0

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):

    urls = ['https://www.acheter-or-argent.fr/?fond=rubrique&id_rubrique=2&page={i}&nouveaute=&promo='.format(i=i) for i in range(1,9)]
    for url in urls :
        print(url)
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        div_product= soup.find_all('div','petitBlocProduit')
        for product in div_product :
            try :

                product_name = product.find('a','art-button').text[1:]
                source = product.find('a','art-button')['href']

                product_price = Price.fromstring(product.find('span','prixProduit').text)
                print(product_price,product_name,source)
                if product_name[:2] == 'or':
                    coin = Item(name=product_name,
                                buy=product_price.amount_float,
                                source=source,
                                buy_premium=((product_price.amount_float + get_delivery_price(product_price.amount_float)) - (
                                                 buy_price * poids_pieces[product_name])) * 100.0 / (buy_price *
                                                       poids_pieces[product_name]),

                                delivery_fee=get_delivery_price(product_price.amount_float), session_id=session_id, bullion_type='g')
                session.add(coin)
                session.commit()

            except :
                print(traceback.format_exc())