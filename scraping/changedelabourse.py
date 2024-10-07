import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

coin_mapping_name = {
    "Napoléon Or 20 Francs": "20 francs or fr",  # Assuming a standard 20 Francs gold coin
    "50 Pesos": "50 pesos or",
    "Souverain": "souverain or",  # Assuming a modern Sovereign
    "20 Dollars US": "20 dollars or",
    "10 Francs Napoléon": "10 francs or fr",
    "20 Francs Suisse": "20 francs or sui vreneli croix",
    "10 Dollars US": "10 dollars or liberté",
    "5 Dollars US": "5 dollars or liberté",
    "Krugerrand": "1 oz krugerrand",
    "10 Florins": "10 florins or",  # Assuming Wilhelmina reign
    "20 Reichsmarks": "20 mark or",
    "Union Latine": "20 francs or union latine",
    "20 Francs Tunisie": "20 francs or tunisie",
    "Demi Souverain": "1/2 souverain or",  # Assuming a George V half Sovereign
    "1 Ducat Francois-Joseph 1915 Or": "1 ducat or"
}
def get_delivery_price(price):
    if 0 <= price <= 600:
        return 10.0
    elif 600.01 <= price <= 2500:
        return 20.0
    elif 2500.01 <= price <= 5000:
        return 34.0
    elif 5000.01 <= price <= 7500:
        return 50.0
    elif 7500.01 <= price <= 10000:
        return 56.0
    elif 10000.01 <= price <= 15000:
        return 65.0
    else:  # price > 15000.01
        return 0.0  # Free delivery

def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Change de la Bourse using requests and BeautifulSoup.
    """
    print('https://www.changedelabourse.com/or/pieces-d-or-d-investissement')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    response = requests.get('https://www.changedelabourse.com/or/pieces-d-or-d-investissement', headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the 'ul' with class 'product_list list row'
    product_list = soup.find('ul', class_='product_list list row')

    # Iterate over each 'li' within the 'ul'
    for product_item in product_list.find_all('li'):
        try:
            # Extract the price
            price_span = product_item.find('span', class_='price product-price')
            price = Price.fromstring(price_span.text.strip())

            # Extract the product name
            product_name_link = product_item.find('a', class_='product-name')
            product_name = product_name_link.text.strip()
            url = product_name_link['href']

            print(price,coin_mapping_name[product_name], url)

            if price:

                # More robust price cleaning: handle variations in formatting
                #price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))

                coin = CoinPrice(nom=coin_mapping_name[product_name],
                                 j_achete=price.amount_float,
                                 source=url,
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
