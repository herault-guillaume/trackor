import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or

from price_parser import Price
import traceback

coin_name = {
    "20 Pesos – Mexique | Or": "20 pesos or",
    "20 Francs Napoléon – Premier Empire | Or": "20 francs or fr napoléon empereur laurée",  # Assuming this is the "tête laurée" type, most common for First Empire
    "2,5 Pesos – Mexique | Or": "2 1/2 pesos or",
    "4 Florins / 10 Francs – Franz Joseph | Or": "4 florins 10 francs 1892 refrappe",
    "1 Ducat – Autriche | Or": "1 ducat or",
    "40 Francs – Charles X | Or": "40 francs or fr charles X",  # This key doesn't exist, handle later
    "1/2 Souverain – Victoria (veuve) | Or": "1/2 souverain or victoria",
    "5 Roubles – Nicolas II | Or": "5 roubles or",  # This key doesn't exist, handle later
    "40 Francs – Louis Philippe | Or": "40 francs or fr louis philippe",  # This key doesn't exist, handle later
    "4 Ducats – Autriche | Or": "4 ducats or",
    "1/2 souverain – Edouard VII | Or": "1/2 souverain or georges V",  # Assuming typo, should be George V
    "10 Lire – Vittorio Emanuele | Or": "10 lire or vittorio emanuele II",  # Assuming it's a 20 Lire coin, clarify if needed
    "5 Roubles – Alexandre III | Or": "5 roubles or",  # This key doesn't exist, handle later
    "20 Francs – Génie | Or": "20 francs or fr génie debout",
    "50 Francs – Napoléon tête nue | Or": "50 francs or napoléon III tête nue",
    "40 Francs – Bonaparte An XI à An 12 | Or": "40 francs or napoléon empereur non laurée",  # This key doesn't exist, handle later
    "10 Francs Suisse | Or": "10 francs or vreneli croix suisse",
    "20 Lire – Umberto I | Or": "20 lire or umberto I",
    "40 Francs – Louis XVIII | Or": "40 francs or louis XVIII",  # This key doesn't exist, handle later
    "100 Francs – Napoléon tête nue | Or": "100 francs or napoléon III tête nue",
    "1/2 Souverain – Victoria (jubilé) | Or": '1/2 souverain or victoria',
    "40 Francs – Napoléon tête laurée | Or": "40 francs or napoléon empereur laurée",
    "10 Francs France – Cérès | Or": "10 francs or cérès 1850-1851",
    "40 Francs – Napoléon Empereur An 13 | Or": "40 francs or napoléon empereur laurée",  # This key doesn't exist, handle later
    "5 Francs – Napoléon tête nue | Or": "5 francs or napoléon III",
    "5 Francs – Napoléon tête laurée | Or": "5 francs or napoléon III nue",  # This key doesn't exist, handle later
    "50 Francs – Napoléon tête laurée | Or": "50 francs or napoléon III tête laurée",  # This key doesn't exist, handle later
    "100 Francs – Génie | Or": "100 francs or génie",  # This key doesn't exist, handle later
    "Napoléon 20 Francs Coq Marianne | Or": "20 francs or coq marianne",
    "Napoléon 20 Francs | Or": "20 francs or napoléon III",
    "Demi Napoléon | Or": "10 francs or napoléon III",
    "Croix Suisse 20 Francs | Or": "20 francs or sui vreneli croix",
    "Lingotin 10 g | Or": "Lingot or 10 g LBMA",
    "Lingotin 20 g | Or": "Lingot or 20 g LBMA",
    "Lingotin 31,1 g | Or": "Lingot or 1 once LBMA",
    "Souverain George V | Or": "souverain or georges V",
    "Souverain Elisabeth | Or": "souverain or elizabeth II",
    "Demi Souverain | Or": "1/2 souverain or georges V",
    "Lingotin 50 g | Or": "Lingot or 50 g LBMA",
    "Lingotin 100 g | Or": "Lingot or 100 g LBMA",
    "Lingot 250 g | Or": "Lingot or 250 g LBMA",
    "Union Latine | Or": "20 francs or union latine",
    "Reichmark | Or": "20 mark or wilhelm II",
    "10 Florins | Or": "10 florins or wilhelmina",  # Assuming Wilhelmina, clarify if needed
    "Lingotin 500 g | Or": "Lingot or 500 g LBMA",
    "Lingot 1 kg | Or": "Lingot or 1 kg LBMA",
    "50 Pesos | Or": "50 pesos or",
    "20 Francs Tunisie | Or": "20 francs or tunisie",
    "American Eagle 1 Once | Or": "1 oz american eagle",
    "Krugerrand 1/10 Once | Or": "1/10 oz krugerrand",
    "Krugerrand 1/4 Once | Or": "1/4 oz krugerrand",
    "Philharmonique 1/10 Once | Or": "",  # Assuming it's the same as American Eagle 1/10 oz
    "20 dollars Liberty": "20 dollars or liberté",
    "10 dollars Indien": "10 dollars or tête indien",
    "10 dollars Liberty": "10 dollars or liberté",
    "5 dollars indien": "5 dollars or tête indien",
    "5 dollars Liberty": "5 dollars or liberté",
    "2 Pesos – Mexique | Or": "2 pesos or",
    "2 Pesos – Mexique | Or": "2 pesos or",
}

def get_delivery_price(price):
    if price <= 1000.0:
        return 10.0
    elif price > 1000.0:
        return 25.0
# forfait

def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
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
            print(price,coin_name[coin_label],url)
            #price = float(price_text.replace('€', '').replace(',', '.'))
            coin = CoinPrice(nom=coin_name[coin_label],
                             j_achete=price.amount_float,
                             source=url,
                             prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                         buy_price * poids_pieces_or[coin_name[coin_label]])) * 100.0 / (buy_price * poids_pieces_or[
                                                   coin_name[coin_label]]),

                             frais_port=get_delivery_price(price.amount_float), session_id=session_id,metal='g')
            session.add(coin)
            session.commit()

        except Exception as e:
            print(traceback.format_exc())