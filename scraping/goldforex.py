import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback

CMN = {
    "Napoléon 20 francs": "or - 20 francs fr napoléon III",
    "Pièce d'or Krugerrand 1 once": "or - 1 oz krugerrand",
    "Lingot d'or 1 kg": "or - lingot 1 kg LBMA",
    "Lingot d'or 500 grammes": "or - lingot 500 g LBMA",
    "Lingot 250 grammes or": "or - lingot 250 g LBMA",
    "Lingot 100 grammes or": "or - lingot 100 g LBMA",
    "Lingot d'or 50 grammes": "or - lingot 50 g LBMA",
    "Lingotin d'or 1 once": "or - lingot 1 once LBMA",
    "Lingot d'or 20 grammes": "or - lingot 20 g LBMA",
    "Lingot d'or 10 grammes": "or - lingot 10 g LBMA",
    "Lingot d'or 5 grammes": "or - lingot 5 g LBMA",
    "Pièce d'or Maple Leaf 1 once": "or - 1 oz maple leaf",
    "Pièce d'or 1 once Eagle de 50 dollars": "or - 1 oz american eagle",  # Assuming this is the American Eagle
    "Pièce d'or Nugget Kangourou 1 once": "or - 1 oz nugget / kangourou",
    "Pièce d'or Philharmonique 1 once": "or - 1 oz philharmonique",
    "Pièce d'or Buffalo 1 once": "or - 1 oz buffalo",
    "Pièce d'or Krugerrand demi once": "or - 1/2 oz krugerrand",
    "Pièce d'or quart 1/4 d'once": "or - 1/4 oz american eagle",  # Assuming this is the American Eagle
    "Pièce d'or 1 dixième d'once Krugerrand": "or - 1/10 oz krugerrand",
    "Pièce d'or 50 écus": "or - 50 écus charles quint",
    "Pièce d'or Vreneli 20 francs suisse": "or - 20 francs sui vreneli croix",
    "Pièce d'or Leopold II 20 francs": "or - 20 francs union latine",  # Assuming Leopold II is part of the Latin Monetary Union
    "Pièce d'or Souverain Nouveau Elisabeth 2": "or - 1 souverain elizabeth II",
    "Pièce d'or 50 pesos mexicain": "or - 50 pesos mex",
    "1 Ducat Autriche": "or - 1 ducat",
    "20 Tunis Or": "or - 20 francs tunisie",
    "20 Pesos Mexicains": "or - 20 pesos mex",
    "10 Pesos Mexicains": "or - 10 pesos mex",
    "Pièce d'or 20 dollars Liberty": "or - 20 dollars liberté longacre",
    "Pièce d'or 10 dollars Indien": "or - 10 dollars tête indien",
    "Pièce d'or 10 dollars Liberty": "or - 10 dollars liberté",
    "Pièce d'or 5 dollars indien": "or - 5 dollars tête indien",
    "Pièce d'or 5 dollars Liberty": "or - 5 dollars liberté",
    "Pièce d'or 2.5 dollars Indien": "or - 2.5 dollars tête indien",
    "Pièce d'or 2.5 dollars Liberty": "or - 2.5 dollars liberté",
    "Pièce d'or 1/2 demi once": "or - 1/2 oz",
    "Pièce d'or 1 dixième d'once 1/10": "or - 1/10 oz",
    "Pièce d'or Souverain Livre ancienne": "or - 1 souverain",
    "Pièce d'or Tientjes 10 Gulden": "or - 10 florins wilhelmina",
    "Pièce d'or Britannia 1 once": "or - 1 oz britannia",
    "100 Piastres Turc": "or - 100 piastres turc",
    "2,5 Pesos Mexicains": "or - 2.5 pesos mex",
    "2,5 Pesos Mexicains": "or - 2.5 pesos mex",
    "Pièce d'or 20 dollars St Gaudens": 'or - 20 dollars liberté st gaudens',
}

#https://www.goldforex.be/fr/content/1-livraison
def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    url = "https://www.goldforex.be/fr/cours-de-l-or-en-direct"
    print(url)


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the relevant divs
    product_divs = soup.find_all('div', class_='col-md-6 col-sm-12 col-xxs-12 col-xs-12 product-ctn row valign-middle')

    # Extract data from each div
    for div in product_divs:
        try:
            # Extract coin name
            coin_label = div.find('a').find('span').text.strip()

            # Extract URL
            url = div.find('a')['href']

            # Extract price (assuming you want the "sell" price)
            price_span = div.find('div', class_='product-sell').find('span', class_='product-price')
            price = Price.fromstring(price_span.text)

            item_data = CMN[coin_label]
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

            delivery_ranges = [(0.0,15000.0,35.0),(15000.0,float('inf'),0.0)]
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
        except Exception as e:
            print(traceback.format_exc())