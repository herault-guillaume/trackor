

import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

coin_mapping_name = {'20 Francs Marianne Coq': '20 francs or coq marianne',
 '20 Francs Napoleon': '20 francs or',
 '50 Pesos': '50 pesos or',
 '10 Francs Marianne Coq': '10 francs or coq marianne',
 '10 Francs Napoleon': '10 francs or',
 'Krugerrand': '1 oz krugerrand',
 'Souverain': 'souverain or',
 '1/2 Souverain': '1/2 souverain or',
 '20 Francs Union Latine': '20 francs or union latine',
 '20 Francs Croix Suisse': '20 francs or vreneli croix suisse',
 '20 Dollars': '20 dollars or',
 '10 Dollars': '10 dollars or liberté',
 '5 Dollars': '5 dollars or liberté',
 '10 Florins': '10 florins or',
 '20 DeutschMarks': '20 mark or',
 '20 Francs Tunisie': '20 francs or tunisie',
 '5 Roubles': '5 roubles or'}
def get_delivery_price(price):
    if 0 <= price <= 600:
        return 10.0
    elif 600.01 <= price <= 1500:
        return 18.0
    elif 1500.01 <= price <= 3000:
        return 28.0
    elif 3000.01 <= price <= 5000:
        return 38.0
    elif 5000.01 <= price <= 7500:
        return 60.0
    elif 7500.01 <= price <= 10000:
        return 70.0
    elif 10000.01 <= price <= 15000:
        return 85.0
    elif 15000.01 <= price <= 20000:
        return 90.0
    else:  # price > 15000.01
        return 0.0  # Free delivery

def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Change de la Bourse using requests and BeautifulSoup.
    """
    print('https://capornumismatique.com/produits/or/or-bourse')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    response = requests.get('https://capornumismatique.com/produits/or/or-bourse', headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    tableau = soup.find_all('tbody')
    # Iterate over each 'li' within the 'ul'
    for product_item in tableau[1].find_all('tr'):
        try:
            # Extract the price
            prices_span = product_item.find('span', class_='popover-price')

            # Get the 'data-content' attribute
            data_content = prices_span['data-content']

            # Parse the 'data-content' as HTML
            inner_soup = BeautifulSoup(data_content, 'html.parser')

            # Find the first 'ul'
            first_li = inner_soup.find('li')
            price = Price.fromstring(first_li.text.strip())

            # Extract the product name
            product_name_link = product_item.find('a', class_='productLink d-block d-md-none')
            product_name = product_name_link.text.strip()
            url = product_name_link['href']
            #print(product_name)
            print(price,coin_mapping_name[product_name],'https://capornumismatique.com'+url)

            if price:

                # More robust price cleaning: handle variations in formatting
                #price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))

                coin = CoinPrice(nom=coin_mapping_name[product_name],
                                 j_achete=price.amount_float,
                                 source='https://capornumismatique.com'+url,
                                 prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                             buy_price * poids_pieces_or[ coin_mapping_name[product_name]])) * 100.0 / (buy_price *
                                                   poids_pieces_or[coin_mapping_name[product_name]]),
                                 frais_port=get_delivery_price(price.amount_float),session_id=session_id,metal='g')
                session.add(coin)
                session.commit()

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error retrieving or parsing price: {e}",url)
            print(traceback.format_exc())
            pass
