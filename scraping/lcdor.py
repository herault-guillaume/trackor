import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback

CMN = {
    "20 Francs Or Coq": 'or - 20 francs fr coq marianne',
    "20 Francs Or Napoléon III": 'or - 20 francs fr napoléon III',
    "20 Francs Or Génie": 'or - 20 francs fr génie debout',
    "20 Francs Or Vreneli": 'or - 20 francs sui vreneli croix',
    "20 Francs Or Leopold 2": 'or - 20 francs union latine',
    "Souverain Or": 'or - 1 souverain elizabeth II',  # Assuming you want Elizabeth II
    "Souverain Or Elizabeth II": 'or - 1 souverain elizabeth II',
    "Krugerrand Or": 'or - 1 oz krugerrand',
    "Maple Leaf Or": 'or - 1 oz maple leaf',
    "Philharmonique Or": 'or - 1 oz philharmonique',
    "50 Pesos Or": 'or - 50 pesos mex',
    "20 Dollars Or Liberty": 'or - 20 dollars liberté longacre',
    "20 Dollars Or St Gaudens": 'or - 20 dollars liberté st gaudens', # Assuming St Gaudens is similar to Liberty
    "10 Dollars Or Liberty": 'or - 10 dollars liberté',
    "American Buffalo Once": 'or - 1 oz buffalo',
    "American Eagle Once": 'or - 1 oz american eagle',
    "5 Roubles Or": 'or - 5 roubles',
    "20 Mark Or": 'or - 20 mark wilhelm II',
    #"5 Roubles Or": None  # No match found in the gold prices dictionary
}

#via panier
def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    url = 'https://lcdor.fr/achat-or/pieces-dor/'
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic browser behavior

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the price element:
    products_div = soup.find_all("div",class_="product-wrapper")

    for product in products_div :
        try:
            price = Price.fromstring(product.find("span","price").text)
            name_title = product.find("h3","wd-entities-title")
            name = name_title.text
            url = name_title.find('a')['href']
            print( price,CMN[name],url)

            minimum = 1
            quantity = 1
            item_data = CMN[name]
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

            delivery_ranges = [(0.0,price.amount_float,7.0),(price.amount_float,float('inf'),0.0)]
            price_ranges = [(minimum,999999999,price)]

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

            coin = Item(name=name,
                        price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                        buy_premiums=';'.join(
['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(1,minimum)] +
['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges)*i,delivery_ranges)/(quantity*i)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(minimum,151)]
                        ),
                        delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                        source=url,
                        session_id=session_id,
                        bullion_type=bullion_type,
                        quantity=quantity,
                        minimum=minimum)

            session.add(coin)
            session.commit()


        except Exception as e:
            print(traceback.format_exc())