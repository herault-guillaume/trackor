import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get(session):
    """
    Fetches the buy price of the 20 Francs Marianne coin from AuCOFFRE using requests and BeautifulSoup.
    """
    url = "https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-1/produit"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content,'html.parser')

        # Use a more specific selector to avoid accidental matches
        price_element = soup.select_one("div[data-url*='20f-marianne'] .text-xlarge.text-bolder.m-0.text-nowrap")

        if price_element:
            price_text = price_element.text.strip()

            # More robust price cleaning: handle variations in formatting
            price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))

            coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='aucoffre',frais_port=15.0)
            session.add(coin)
            session.commit()

            return price
        else:
            print("Price element not found on page.")
            return None

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error retrieving or parsing price: {e}",url)
        return None