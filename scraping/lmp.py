import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get(session):
    url = 'https://www.lesmetauxprecieux.com/produit/20-francs-marianne-coq/'
    headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic browser behavior

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the price element:
        price_elements = soup.select("span.woocommerce-Price-amount.amount bdi")

        if not price_elements:
            raise ValueError("Price element not found")

        # Extract and clean:
        price_text = price_elements[1].text
        price = float(price_text.replace('€', '').replace(',', '.'))

        coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='https://www.lesmetauxprecieux.com/produit/20-francs-marianne-coq/',frais_port=15.79)
        session.add(coin)
        session.commit()

        return price

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error retrieving price: {e}",url)
        return None