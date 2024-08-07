import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

# https://or-investissement.fr/information-or-investissement/1-livraison-achat-or-investissement
def get_price_for(session,session_id):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Or-Investissement using requests and BeautifulSoup.
    """
    url = 'https://or-investissement.fr/achat-piece-or-investissement/8-achat-piece-20-francs-marianne-coq.html'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad HTTP responses

        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the price element using the itemprop and class attributes
        price_element = soup.select_one('span[itemprop="price"].product-price')

        if price_element:
            # Extract and clean the price text
            price_text = price_element.text.strip().replace('€', '').replace(',', '.').replace('\xa0', '')

            try:
                price = float(price_text)
                coin = CoinPrice(nom="20 francs or coq marianne",
                                 j_achete=price,
                                 source=url,
                                 frais_port=25.0,session_id=session_id)
                session.add(coin)
                session.commit()
                return price
            except ValueError:
                print(f"Failed to convert price text '{price_text}' to float,url")
        else:
            print("Price element not found on page.",url)

    except requests.RequestException as e:
        print(f"An error occurred during the request: {e}",url)

    return None  # Return None on failure