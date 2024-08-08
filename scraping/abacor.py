import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice
from price_parser import Price

def get_delivery_price(price):
    if price <= 500.0:
        return 14.00
    elif 500 < price <= 1000.0 :
        return 26.70
    else:
        return 56.10

def get_price_for(session,session_id):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
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
    for url, coin_name in urls.items() :
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')


            # Use a more specific CSS selector to target the price element
            price_elements = soup.select('span.woocommerce-Price-amount.amount bdi')  # Find the <bdi> element within the <span>

            if price_elements:
                # Clean the price text
                try:
                    if len(price_elements) == 3:
                        #en cas de reduction
                        price_text = price_elements[2].text.strip()
                    else:
                        price_text = price_elements[1].text.strip()
                    price = Price.fromstring(price_text)

                    coin = CoinPrice(nom=coin_name,
                                     j_achete=price.amount_float,
                                     frais_port=get_delivery_price(price.amount_float),
                                     source=url,session_id=session_id)
                    session.add(coin)
                    session.commit()

                except (ValueError, IndexError) as e:
                    print(f"Failed to parse price: {e}",url)
            else:
                print("Price element not found on page.")

        except requests.RequestException as e:
            print(f"Error making request to {url}: {e}",url)

    return None  # Return None on failure