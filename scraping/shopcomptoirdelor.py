import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get(session):
    url = "https://www.shop-comptoirdelor.be/achat-or/pieces/20-francs-or-diverses-ann%C3%A9espays"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')


        # Attempt to find the price element (this might fail due to dynamic loading)
        price_element = soup.select_one('strong[itemprop="price"]')

        if price_element:
            price_text = price_element.text.strip()
            price = float(price_text.replace('€', '').replace(',', '.').replace('&nbsp;', ''))

            coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='shopcomptoirdelor',frais_port=4.95)
            session.add(coin)
            session.commit()

            return price

        else:
            print("Price element not found on page. Likely due to dynamic content.",url)
            return None

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}",url)
        return None