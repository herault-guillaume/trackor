import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice
def get(session):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    url = "https://goldunion.fr/products/20-francs-coq"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the span with aria-hidden="true" containing the price
        price_element = soup.find('span', attrs={"aria-hidden": "true"})

        if price_element:
                price_text = price_element.text.strip()

                # Clean the price text
                try:
                    price = float(price_text.replace('€', '').replace(',', '.'))
                    coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='goldunion')
                    session.add(coin)
                    session.commit()

                    return price
                except ValueError:
                    print(f"Failed to convert price text '{price_text}' to float")
        else:
            print("Price element not found on page.")

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}")

    return None