

import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback

CMN = {'20 Francs Marianne Coq': 'or - 20 francs fr coq marianne',
 '20 Francs Napoleon': 'or - 20 francs fr',
 '50 Pesos': 'or - 50 pesos mex',
 '10 Francs Marianne Coq': 'or - 10 francs fr coq marianne',
 '10 Francs Napoleon': 'or - 10 francs fr',
 'Krugerrand': 'or - 1 oz krugerrand',
 'Souverain': 'or - 1 souverain',
 '1/2 Souverain': 'or - 1/2 souverain',
 '20 Francs Union Latine': 'or - 20 francs union latine',
 '20 Francs Croix Suisse': 'or - 20 francs sui vreneli croix',
 '20 Dollars': 'or - 20 dollars',
 '10 Dollars': 'or - 10 dollars liberté',
 '5 Dollars': 'or - 5 dollars liberté',
 '10 Florins': 'or - 10 florins',
 '20 DeutschMarks': 'or - 20 mark',
 '20 Francs Tunisie': 'or - 20 francs tunisie',
 '5 Roubles': 'or - 5 roubles'}

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



def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Change de la Bourse using requests and BeautifulSoup.
    """
    print('https://capornumismatique.com/')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    delivery_ranges = [
    (0, 600, 10.0),
    (600.01, 1500, 18.0),
    (1500.01, 3000, 28.0),
    (3000.01, 5000, 38.0),
    (5000.01, 7500, 60.0),
    (7500.01, 10000, 70.0),
    (10000.01, 15000, 85.0),
    (15000.01, 20000, 90.0),
    (20000.01, float('inf'), 0.0)  # Free delivery above 20000
]

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
            url = 'https://capornumismatique.com' + product_name_link['href']
            #print(product_name)

            item_data = CMN[product_name]

            if price:
                minimum = 1
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

            def price_between(value, ranges):
                """
                Returns the price per unit for a given quantity.
                """

                for min_qty, max_qty, price in ranges:
                    if min_qty <= value <= max_qty:
                        if isinstance(price, Price):
                            return price.amount_float
                        else:
                            return price

            price_ranges = [(1,9999999999,price)]

            print(price,name,url)
            coin = Item(name=name,
                        price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                        buy_premiums=';'.join(
['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(1,minimum)] +
['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(minimum,151)]
                        ),
                        delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                        source=url,
                        session_id=session_id,
                        bullion_type=bullion_type,
                        quantity=quantity,
                        minimum=minimum)
            session.add(coin)
            session.commit()

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error retrieving or parsing price: {e}",url)
            print(traceback.format_exc())
            pass
