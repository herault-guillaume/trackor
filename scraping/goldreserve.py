import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces

from price_parser import Price
import traceback
import re

CMN = {
    "20 Pesos – Mexique | Or": "or - 20 pesos mex",
    "20 Francs Napoléon – Premier Empire | Or": "or - 20 francs fr napoléon empereur laurée",  # Assuming this is the "tête laurée" type, most common for First Empire
    "2,5 Pesos – Mexique | Or": "or - 2.5 pesos mex",
    "4 Florins / 10 Francs – Franz Joseph | Or": "or - 4 florins 10 francs 1892 refrappe",
    "1 Ducat – Autriche | Or": "or - 1 ducat",
    "40 Francs – Charles X | Or": "or - 40 francs fr charles X",  # This key doesn't exist, handle later
    "1/2 Souverain – Victoria (veuve) | Or": "or - 1/2 souverain victoria",
    "5 Roubles – Nicolas II | Or": "or - 5 roubles",  # This key doesn't exist, handle later
    "40 Francs – Louis Philippe | Or": "or - 40 francs fr louis philippe",  # This key doesn't exist, handle later
    "4 Ducats – Autriche | Or": "or - 4 ducats",
    "1/2 souverain – Edouard VII | Or": "or - 1/2 souverain edouard VII",  # Assuming typo, should be George V
    "10 Lire – Vittorio Emanuele | Or": "or - 10 lire vittorio emanuele II",  # Assuming it's a 20 Lire coin, clarify if needed
    "5 Roubles – Alexandre III | Or": "or - 5 roubles",  # This key doesn't exist, handle later
    "20 Francs – Génie | Or": "or - 20 francs fr génie debout",
    "50 Francs – Napoléon tête nue | Or": "or - 50 francs fr napoléon III tête nue",
    "40 Francs – Bonaparte An XI à An 12 | Or": "or - 40 francs fr napoléon empereur non laurée",  # This key doesn't exist, handle later
    "10 Francs Suisse | Or": "or - 10 francs sui vreneli croix",
    "20 Lire – Umberto I | Or": "or - 20 lire umberto I",
    "40 Francs – Louis XVIII | Or": "or - 40 francs fr louis XVIII",  # This key doesn't exist, handle later
    "100 Francs – Napoléon tête nue | Or": "or - 100 francs fr napoléon III tête nue",
    "1/2 Souverain – Victoria (jubilé) | Or": 'or - 1/2 souverain victoria',
    "40 Francs – Napoléon tête laurée | Or": "or - 40 francs fr napoléon empereur laurée",
    "10 Francs France – Cérès | Or": "or - 10 francs fr cérès 1850-1851",
    "40 Francs – Napoléon Empereur An 13 | Or": "or - 40 francs fr napoléon empereur laurée",  # This key doesn't exist, handle later
    "5 Francs – Napoléon tête nue | Or": "or - 5 francs fr napoléon III",
    "5 Francs – Napoléon tête laurée | Or": "or - 5 francs fr napoléon III nue",  # This key doesn't exist, handle later
    "50 Francs – Napoléon tête laurée | Or": "or - 50 francs fr napoléon III tête laurée",  # This key doesn't exist, handle later
    "100 Francs – Génie | Or": "or - 100 francs fr génie LEF",  # This key doesn't exist, handle later
    "Napoléon 20 Francs Coq Marianne | Or": "or - 20 francs fr coq marianne",
    "Napoléon 20 Francs | Or": "or - 20 francs fr napoléon III",
    "Demi Napoléon | Or": "or - 10 francs fr napoléon III",
    "Croix Suisse 20 Francs | Or": "or - 20 francs sui vreneli croix",
    "Lingotin 10 g | Or": "or - lingot 10 g LBMA",
    "Lingotin 20 g | Or": "or - lingot 20 g LBMA",
    "Lingotin 31,1 g | Or": "or - lingot 1 once LBMA",
    "Souverain George V | Or": "or - 1 souverain georges V",
    "Souverain Elisabeth | Or": "or - 1 souverain elizabeth II",
    "Demi Souverain | Or": "or - 1/2 souverain georges V",
    "Lingotin 50 g | Or": "or - lingot 50 g LBMA",
    "Lingotin 100 g | Or": "or - lingot 100 g LBMA",
    "Lingot 250 g | Or": "or - lingot 250 g LBMA",
    "Union Latine | Or": "or - 20 francs union latine",
    "Reichmark | Or": "or - 20 mark wilhelm II",
    "10 Florins | Or": "or - 10 florins wilhelmina",  # Assuming Wilhelmina, clarify if needed
    "Lingotin 500 g | Or": "or - lingot 500 g LBMA",
    "Lingot 1 kg | Or": "or - lingot 1 kg LBMA",
    "50 Pesos | Or": "or - 50 pesos mex",
    "20 Francs Tunisie | Or": "or - 20 francs tunisie",
    "American Eagle 1 Once | Or": "or - 1 oz american eagle",
    "Krugerrand 1/10 Once | Or": "or - 1/10 oz krugerrand",
    "Krugerrand 1/4 Once | Or": "or - 1/4 oz krugerrand",
    "Philharmonique 1/10 Once | Or": "or - 1/10 oz philharmonique",  # Assuming it's the same as American Eagle 1/10 oz
    "20 dollars Liberty": "or - 20 dollars liberté",
    "10 dollars Indien": "or - 10 dollars tête indien",
    "10 dollars Liberty": "or - 10 dollars liberté",
    "5 dollars indien": "or - 5 dollars tête indien",
    "5 dollars Liberty": "or - 5 dollars liberté",
    "2 Pesos – Mexique | Or": "or - 2 pesos mex",

    "Maple Leaf 1 Once | Argent": "ar - 1 oz maple leaf",
    "Philharmonique de Vienne 1 Once | Argent": "ar - 1 oz philharmonique",
    "Kangourou 1 Once | Argent": "ar - 1 oz kangourou",
    "American Eagle 1 Once | Argent": "ar - 1 oz silver eagle",
    "50 Francs Hercule | Argent": "ar - 50 francs fr hercule (1974-1980)",
    "100 Francs | Argent": "ar - 100 francs fr",
    "10 Francs Turin | Argent": "ar - 10 francs fr turin (1860-1928)",
    "10 Francs Hercule | Argent": "ar - 10 francs fr hercule (1965-1973)",
    "5 Francs Semeuse | Argent": "ar - 5 francs fr semeuse (1959-1969)",


}

def get_delivery_price(price):
    if price <= 1000.0:
        return 10.0
    elif price > 1000.0:
        return 25.0
# forfait

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """

    url = "https://www.goldreserve.fr/boutique-goldreserve/?type=pieces"
    print(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')


    # Use a more specific CSS selector to target the price element
    product_divs = soup.find_all('div',
                                 class_='jet-woo-products__item jet-woo-builder-product')

    for div in product_divs:
        try:
            # Extract coin name
            coin_label = div.find('h5',class_="jet-woo-product-title").text.strip()

            # Extract URL
            url = div.find('a')['href']

            # Extract price (assuming you want the "sell" price)
            price_span = div.find('span', class_='woocommerce-Price-amount amount')
            price = Price.fromstring(price_span.text)

            minimum = 1

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
            
            print(price,CMN[coin_label],url)

            #price = float(price_text.replace('€', '').replace(',', '.'))
            coin = Item(name=name,
                        buy=price.amount_float,
                        source=url,
                        buy_premium=(((price.amount_float + get_delivery_price(
                            price.amount_float) / minimum) / float(quantity)) - (
                                             buy_price * poids_pieces[name])) * 100.0 / (
                                            buy_price * poids_pieces[name]),

                        delivery_fee=get_delivery_price(price.amount_float),
                        session_id=session_id,
                        bullion_type=bullion_type,
                        quantity=quantity,
                        minimum=minimum)

            session.add(coin)
            session.commit()

        except Exception as e:
            print(traceback.format_exc())