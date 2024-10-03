import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

coin_name = {
    "Napoléon 20 francs": "20 francs or napoléon III",
    "Pièce d'or Krugerrand 1 once": "1 oz krugerrand",
    "Lingot d'or 1 kg": "Lingot or 1 kg LBMA",
    "Lingot d'or 500 grammes": "Lingot or 500 g LBMA",
    "Lingot 250 grammes or": "Lingot or 250 g LBMA",
    "Lingot 100 grammes or": "Lingot or 100 g LBMA",
    "Lingot d'or 50 grammes": "Lingot or 50 g LBMA",
    "Lingotin d'or 1 once": "Lingot or 1 once LBMA",
    "Lingot d'or 20 grammes": "Lingot or 20 g LBMA",
    "Lingot d'or 10 grammes": "Lingot or 10 g LBMA",
    "Lingot d'or 5 grammes": "Lingot or 5 g LBMA",
    "Pièce d'or Maple Leaf 1 once": "1 oz maple leaf",
    "Pièce d'or 1 once Eagle de 50 dollars": "1 oz american eagle",  # Assuming this is the American Eagle
    "Pièce d'or Nugget Kangourou 1 once": "1 oz nugget / kangourou",
    "Pièce d'or Philharmonique 1 once": "1 oz philharmonique",
    "Pièce d'or Buffalo 1 once": "1 oz buffalo",
    "Pièce d'or Krugerrand demi once": "1/2 oz krugerrand",
    "Pièce d'or quart 1/4 d'once": "1/4 oz american eagle",  # Assuming this is the American Eagle
    "Pièce d'or 1 dixième d'once Krugerrand": "1/10 oz krugerrand",
    "Pièce d'or 50 écus": "50 écus or charles quint",
    "Pièce d'or Vreneli 20 francs suisse": "20 francs or vreneli croix suisse",
    "Pièce d'or Leopold II 20 francs": "20 francs or union latine léopold II",  # Assuming Leopold II is part of the Latin Monetary Union
    "Pièce d'or Souverain Nouveau Elisabeth 2": "souverain or elizabeth II",
    "Pièce d'or 50 pesos mexicain": "50 pesos or",
    "1 Ducat Autriche": "1 ducat or",
    "20 Tunis Or": "20 francs or tunisie",
    "20 Pesos Mexicains": "20 pesos or",
    "10 Pesos Mexicains": "10 pesos or",
    "Pièce d'or 20 dollars Liberty": "20 dollars or liberté",
    "Pièce d'or 10 dollars Indien": "10 dollars or tête indien",
    "Pièce d'or 10 dollars Liberty": "10 dollars or liberté",
    "Pièce d'or 5 dollars indien": "5 dollars or tête indien",
    "Pièce d'or 5 dollars Liberty": "5 dollars or liberté",
    "Pièce d'or 2.5 dollars Indien": "2.5 dollars or tête indien",
    "Pièce d'or 2.5 dollars Liberty": "2.5 dollars or liberté",
    "Pièce d'or 1/2 demi once": "1/2 oz",
    "Pièce d'or 1 dixième d'once 1/10": "1/10 oz",
    "Pièce d'or Souverain Livre ancienne": "souverain or",
    "Pièce d'or Tientjes 10 Gulden": "10 florins or wilhelmina",
    "Pièce d'or Britannia 1 once": "1 oz britannia",
    "100 Piastres Turc": "100 piastres or turc",
    "2,5 Pesos Mexicains": "2 1/2 pesos or",
    "2,5 Pesos Mexicains": "2 1/2 pesos or",
    "Pièce d'or 20 dollars St Gaudens": '20 dollars or st gaudens',
    "2.5 dollars or liberté": '2.5 dollars or tête liberté',
}

#https://www.goldforex.be/fr/content/1-livraison
def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
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


            print(price,coin_label)
            #price = float(price_text.replace('€', '').replace(',', '.'))
            coin = CoinPrice(nom=coin_name[coin_label],
                             j_achete=price.amount_float,
                             source=url,
                             prime_achat_perso=((price.amount_float + 35.0) - (
                                         buy_price * poids_pieces_or[coin_name[coin_label]])) * 100.0 / (buy_price * poids_pieces_or[
                                                   coin_name[coin_label]]),

                             frais_port=35.0,session_id=session_id,metal='g')
            session.add(coin)
            session.commit()
        except Exception as e:
            print(traceback.format_exc())