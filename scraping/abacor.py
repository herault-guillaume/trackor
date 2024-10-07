import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

def get_delivery_price(price):
    if price <= 500.0:
        return 14.00
    elif 500 < price <= 1000.0 :
        return 26.70
    else:
        return 56.10

def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or fr coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """
    print("https://www.abacor.fr/")

    urls = ['https://www.abacor.fr/boutique-achat-vente/','https://www.abacor.fr/boutique-achat-vente/page/2/']

    coin_to_name = {
        'Lingot d’Or 1 Kg': 'Lingot or 1 kg LBMA',
        'Lingot Or 500 Gr': 'Lingot or 500 g LBMA',
        'Lingot Or 250 Gr': 'Lingot or 250 g LBMA',
        'Lingot Or 100 Gr': 'Lingot or 100 g LBMA',
        'Lingotin Or 50 Gr': 'Lingot or 50 g LBMA',
        'Lingot Or Once 31.1 Gr': '1 oz',
        'Lingotin Or 20 Gr': 'Lingot or 20 g LBMA',
        'Lingotin Or 10 Gr': 'Lingot or 10 g LBMA',
        'Lingotin Or 5 Gr': 'Lingot or 5 g LBMA',
        'Pièce d’Or 20 Francs Coq Marianne': '20 francs or fr coq marianne refrappe pinay',
        'Pièce d’Or 20 Francs Napoléon / Louis d’Or': '20 francs or fr napoléon empereur laurée', # Or '20 francs or fr louis XVIII buste nu' depending on the coin
        'Pièce d’Or 20 Francs Suisse': '20 francs or sui vreneli croix',
        'Union Latine Or': '20 francs or union latine',
        'Pièce d’Or Souverain': 'souverain or',
        'Pièce d’Or 20 Dollars US': '20 dollars or',
        'Pièce d’Or 10 Dollars Liberty': '10 dollars or liberté',
        'Pièce d’Or 10 Dollars Tête d’Indien': '10 dollars or tête indien',
        'Pièce d’Or 50 Pesos Mexicain': '50 pesos or',
        'Pièce d’Or 10 Florins – 10 Gulden': '10 florins or wilhelmina', # Or '10 florins or willem III' depending on the coin
        'Pièce d’Or Krugerrand': '1 oz krugerrand',
        'Pièce d’Or 10 Francs Napoléon': '10 francs or fr napoléon III laurée', # Or '10 francs or fr napoléon III laurée' depending on the coin
        'Pièce d’Or 20 Francs Tunisie': '20 francs or tunisie',
        'Pièce d’Or Souverain Elizabeth II': 'souverain or elizabeth II',
        'Pièce d’Or 5 Dollars US': '5 dollars or liberté',  # Or '5 dollars or tête indien' depending on the coin
    }


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

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
                print(price,coin_to_name[product_name],source)

                coin = CoinPrice(nom=coin_to_name[product_name],
                                 j_achete=price.amount_float,
                                 frais_port=get_delivery_price(price.amount_float),
                                 prime_achat_perso=((price.amount_float+get_delivery_price(price.amount_float))-(buy_price*poids_pieces_or[coin_to_name[product_name]]))*100.0/(buy_price*poids_pieces_or[coin_to_name[product_name]]),
                                 source=source,session_id=session_id,metal='g')
                session.add(coin)
                session.commit()

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    return None  # Return None on failure