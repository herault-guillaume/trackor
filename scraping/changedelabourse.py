import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback

CMN = {
    "Napoléon Or 20 Francs": "or - 20 francs fr",  # Assuming a standard 20 Francs gold coin
    "50 Pesos": "or - 50 pesos",
    "Souverain": "or - 1 souverain",  # Assuming a modern Sovereign
    "20 Dollars US": "or - 20 dollars",
    "10 Francs Napoléon": "or - 10 francs fr",
    "20 Francs Suisse": "or - 20 francs sui vreneli croix",
    "10 Dollars US": "or - 10 dollars liberté",
    "5 Dollars US": "or - 5 dollars liberté",
    "Krugerrand": "or - 1 oz krugerrand",
    "10 Florins": "or - 10 florins",  # Assuming Wilhelmina reign
    "20 Reichsmarks": "or - 20 mark",
    "Union Latine": "or - 20 francs union latine",
    "20 Francs Tunisie": "or - 20 francs tunisie",
    "Demi Souverain": "or - 1/2 souverain",  # Assuming a George V half Sovereign
    "1 Ducat Francois-Joseph 1915 Or": "or - 1 ducat"
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

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Change de la Bourse using requests and BeautifulSoup.
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

            print(price,CMN[product_name], url)

            if price:

                # More robust price cleaning: handle variations in formatting
                #price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))
                if CMN[product_name][:2] == 'or':
                    coin = Item(name=CMN[product_name],
                                buy=price.amount_float,
                                source=url,
                                buy_premium=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                                 buy_price * poids_pieces[ CMN[product_name]])) * 100.0 / (buy_price *
                                                       poids_pieces[CMN[product_name]]),
                                delivery_fee=get_delivery_price(price.amount_float), session_id=session_id, bullion_type='g')
                session.add(coin)
                session.commit()

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error retrieving or parsing price: {e}",url)
            print(traceback.format_exc())
            pass
