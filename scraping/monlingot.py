import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice
from price_parser import Price
import traceback

coin_name = {
    "20 Francs Or Napoléon": '20 francs or napoléon III',
    "American Eagle 1 Once Or": '1 oz american eagle',
    "Lingotin Or 5 grammes": 'Lingot or 5 g LBMA',
    "10 Francs Or Napoléon": '10 francs or napoléon III',
    "Buffalo Or 1 Once": '1 oz buffalo',
    "Lingotin Or 10 grammes": 'Lingot or 10 g LBMA',
    "20 dollars US": '20 dollars or liberté',
    "Maple Leaf Or 1 Once": '1 oz maple leaf',
    "Lingotin Or 20 grammes": 'Lingot or 20 g LBMA',
    "10 Dollars US": '10 dollars or liberté',
    "Philharmonique Or 1 Once": '1 oz philharmonique',
    "Lingotin Or 1 once (31,1...)": 'Lingot or 1 once LBMA',
    "Lingotin Or 50 grammes": 'Lingot or 50 g LBMA',
    "5 Dollars US": '5 dollars or liberté',
    "Demi Souverain": '1/2 souverain georges V',  # Assuming Georges V based on your data
    "Kangaroo Or 1 Once": '1 oz nugget / kangourou',
    "Lingotin Or 100 grammes": 'Lingot or 100 g LBMA',
    "50 pesos or": '50 pesos or',
    "Lingot Or 500 grammes": 'Lingot or 500 g LBMA',
    "Souverain": 'souverain or elizabeth II',  # Assuming Elizabeth II based on your data
    "Lingot Or 1 Kilo": 'Lingot or 1 kg LBMA',
    "Lingot Or 250 grammes": 'Lingot or 250 g LBMA',
    "20 Reichsmark Or": '20 mark or wilhelm II',
    "10 Florins Or": '10 florins or wilhelmina',  # Assuming Wilhelmina based on your data
    "Union Latine Or": '20 francs or union latine léopold II',
    "20 Francs Suisse Or": '20 francs or helvetia suisse',
    "Krugerrand Or 1 Once": '1 oz krugerrand',
    "20 francs Coq Marianne": '20 francs or coq marianne',
    "Britannia Or 1 Once": '1 oz britannia',  # Assuming this is the intended mapping
    #"LEON OR 1 once": None,  # No direct match in your original data
    #"LEON OR 1/10 once": None   # No direct match in your original data
}

def get_delivery_price(price):
    #https://monlingot.fr/conseil/livraison
    if price < 2500 :
        return 9.90 # Not available for higher values
    elif 2500 <= price < 20000 :
        return 19.90
    else:
        return 0.0

#https://monlingot.fr/conseil/livraison
def get_price_for(session,session_id):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """

    urls = ['https://monlingot.fr/or?page=1','https://monlingot.fr/or?page=2','https://monlingot.fr/or?page=3']
    print(urls)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    for url in urls :
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        products_div = soup.find_all("article")

        for product in products_div:
            try:
                price = Price.fromstring(product.find("span", "price").text)
                name_title = product.find("h2", "h3 product-title")
                name = name_title.text
                url = product.find('a')['href']
                print(name,price)

                #price = float(price_text.replace('€', '').replace(',', '.').replace(' ', '').replace('\xa0NET',''))

                coin = CoinPrice(nom=coin_name[name],
                                 j_achete=price.amount_float,
                                 source=url,
                                 frais_port=get_delivery_price(price.amount_float),session_id=session_id)
                session.add(coin)
                session.commit()


            except Exception as e:
                print(traceback.format_exc())