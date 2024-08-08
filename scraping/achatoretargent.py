import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice
from price_parser import Price

def get_delivery_price(price):
    if 0 <= price <= 1000:
        return 15.0
    elif 1000.01 <= price <= 2500:
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

def get_price_for(session,session_id):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from achat-or-et-argent.fr using requests.
    """
    urls = { "https://www.abacor.fr/produit/test-20-dollars-us/" : "20 dollars or liberté",
             "https://www.abacor.fr/produit/piece-dor-20-francs-coq-marianne/" : "20 francs or coq marianne",
             "https://www.abacor.fr/produit/piece-d-or-20-francs-napoleon/" : "20 francs or napoléon III",
             "https://www.abacor.fr/produit/piece-d-or-20-francs-suisse/" : "20 francs or helvetia suisse",
             "https://www.abacor.fr/produit/test-union-latine/" : "20 francs or union latine léopold II",
             "https://www.abacor.fr/produit/piece-d-or-10-dollars-liberty/" : "10 dollars or liberté",
             "https://www.abacor.fr/produit/piece-d-or-10-dollars-tete-d-indien/" : "10 dollars or tête indien",
             "https://www.abacor.fr/produit/piece-d-or-50-pesos/" : "50 pesos or",
             "https://www.abacor.fr/produit/piece-d-or-krugerrand/" : "1 oz krugerrand",
             "https://www.abacor.fr/produit/piece-d-or-10-francs-napoleon/" : "10 francs or napoléon III",
             "https://www.abacor.fr/produit/piece-d-or-20-francs-tunisie/" : "20 francs or tunisie",
             "https://www.abacor.fr/produit/piece-d-or-souverain-elizabeth-ii/" : "souverain or elizabeth II",
             "https://www.abacor.fr/produit/test-5-dollars-us/" : "5 dollars or liberté"
             }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    for url, coin_name in urls.items():
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the specific price span element using its ID
            price_element = soup.find('span', id="pa9")

            if price_element:
                # Extract and clean the price text
                price_text = price_element.text.strip().replace('€', '').replace(',', '.')
                price = Price.fromstring(price_text)
                try:
                    coin = CoinPrice(nom=coin_name,
                                     j_achete=price.amount_float,
                                     source=url,
                                     frais_port=get_delivery_price(price.amount_float),session_id=session_id)
                    session.add(coin)
                    session.commit()

                    return price
                except ValueError:
                    print("Price format could not be parsed.",url)

            else:
                print("Price element not found.")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}",url)
        return None  # Return None to indicate an unsuccessful retrieval