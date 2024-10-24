import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs fr coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """
    print("https://www.abacor.fr/")

    urls = ['https://www.abacor.fr/boutique-achat-vente/','https://www.abacor.fr/boutique-achat-vente/page/2/','https://www.abacor.fr/product-category/achat-argent/pieces-d-argent/']

    CMN = {
        'Lingot d’Or 1 Kg': 'or - lingot 1 kg LBMA',
        'Lingot Or 500 Gr': 'or - lingot 500 g LBMA',
        'Lingot Or 250 Gr': 'or - lingot 250 g LBMA',
        'Lingot Or 100 Gr': 'or - lingot 100 g LBMA',
        'Lingotin Or 50 Gr': 'or - lingot 50 g LBMA',
        'Lingot Or Once 31.1 Gr': 'or - 1 oz',
        'Lingotin Or 20 Gr': 'or - lingot 20 g LBMA',
        'Lingotin Or 10 Gr': 'or - lingot 10 g LBMA',
        'Lingotin Or 5 Gr': 'or - lingot 5 g LBMA',
        'Pièce d’Or 20 Francs Coq Marianne': 'or - 20 francs fr coq marianne refrappe pinay',
        'Pièce d’Or 20 Francs Napoléon / Louis d’Or': 'or - 20 francs fr napoléon empereur laurée',
        'Pièce d’Or 20 Francs Suisse': 'or - 20 francs sui vreneli croix',
        'Union Latine Or': 'or - 20 francs union latine',
        'Pièce d’Or Souverain': 'or - 1 souverain',
        'Pièce d’Or 20 Dollars US': 'or - 20 dollars',
        'Pièce d’Or 10 Dollars Liberty': 'or - 10 dollars liberté',
        'Pièce d’Or 10 Dollars Tête d’Indien': 'or - 10 dollars tête indien',
        'Pièce d’Or 50 Pesos Mexicain': 'or - 50 pesos mex',
        'Pièce d’Or 10 Florins – 10 Gulden': 'or - 10 florins wilhelmina',
        'Pièce d’Or Krugerrand': 'or - 1 oz krugerrand',
        'Pièce d’Or 10 Francs Napoléon': 'or - 10 francs fr napoléon III laurée',
        'Pièce d’Or 20 Francs Tunisie': 'or - 20 francs tunisie',
        'Pièce d’Or Souverain Elizabeth II': 'or - 1 souverain elizabeth II',
        'Pièce d’Or 5 Dollars US': 'or - 5 dollars liberté',

        'Lingot Argent 5 Kg' : 'ar - lingot 5 kg',
        '50 Francs Argent Hercule': 'ar - 50 francs fr hercule (1974-1980)',
        '10 Francs Argent Hercule': 'ar - 10 francs fr hercule (1965-1973)',
        '5 Francs Argent Semeuse': 'ar - 5 francs fr semeuse (1959-1969)',
        '2 Francs Argent Semeuse': 'ar - 2 francs fr semeuse',
        '1 Franc Argent Semeuse': 'ar - 1 franc fr semeuse',
        '50 Centimes Argent Semeuse': 'ar - 50 centimes francs fr semeuse',
        '100 Francs Argent': 'ar - 100 francs fr',
        '20 Francs Argent Turin': 'ar - 20 francs fr turin (1860-1928)',
        '10 Francs Argent Turin': 'ar - 10 francs fr turin (1860-1928)',
    }


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    delivery_ranges = (
        [1,500,14.0],
        [500,1000,26.0],
        [1000,100000000,56.0],
    )

    for url in urls :
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            tableau = soup.find('ul',class_='products columns-4')
            products = tableau.find_all('li')
            for p in products:

                product_name = p.find('h2').text
                source = p.find('a')['href']
                # Use a more specific CSS selector to target the price element
                price_elements = p.find('span',class_='price')  # Find the <bdi> element within the <span>
                solde = price_elements.find('ins')
                if solde:
                    price = Price.fromstring(solde.text)
                else:
                    price = Price.fromstring(price_elements.text)

                item_data = CMN[product_name]
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

                print(price,name,source)

                price_ranges = [
                    (1, 1000, price),  # Quantity 1-10, price 10.0 per unit
                ]

                def price_between(value,ranges):
                    """
                    Returns the price per unit for a given quantity.
                    """
                    for min_qty, max_qty, price in ranges:
                        if min_qty <= value <= max_qty:
                            if isinstance(price,Price):
                                return price.amount_float
                            else:
                                return price

                coin = Item(name=name,
                            prices=';'.join(['{:.1f}'.format(p[2].amount_float) for p in price_ranges]),
                            ranges=';'.join(['{min_}-{max_}'.format(min_=r[0],max_=r[1]) for r in price_ranges]),

                            buy_premiums=';'.join(['{:.1f}'.format(((price_between(min,price_ranges)+price_between(price.amount_float*min,delivery_ranges)/min)/float(quantity)-
                                                    (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name]))
                                                  for min in range(1,minimum)])
                                        + ';'.join(['{:.1f}'.format(((price_between(q,price_ranges)+price_between(price.amount_float*q,delivery_ranges))/float(q)-
                                                     (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name]))
                                                  for q in range(1,quantity)])
                                         + ';'.join(['{:.1f}'.format(((price_between(min,price_ranges)+price_between(price.amount_float*min,delivery_ranges)/min)-
                                                      (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name]))
                                                  for min in range(minimum,150)]),

                            delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                            source=source,
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=quantity,
                            minimum=minimum)
                session.add(coin)
                session.commit()

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    return None  # Return None on failure