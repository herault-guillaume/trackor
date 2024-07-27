import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get(session):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Gold.fr using requests and BeautifulSoup.
    """
    url = "https://www.gold.fr/napoleon-or-20-francs-louis-or/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for

        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the price element using a more specific CSS selector
        price_element = soup.select_one("div.product-action p.price span.amount")

        if price_element:
            price_text = price_element.text.strip()

            # Clean the price text, handling variations in formatting and potential errors
            try:
                price = float(price_text.replace('€', '').replace(',', '.').replace('\nmin. 5', ''))
                coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='gold')
                session.add(coin)
                session.commit()

                return price
            except ValueError:
                print(f"Failed to convert price text '{price_text}' to float",url)
        else:
            print("Price element not found on page.",url)

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}",url)

    return None  # Return None on failure