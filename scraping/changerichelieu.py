import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice


def get(session):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    url = "https://www.changerichelieu.fr/or/pieces-d-or-d-investissement/20-francs-napoleon"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the span element with class "result2"
        price_element = soup.find('p', class_='cdb-pricea')  # Update the class nam

        if price_element:
            price_text = price_element.text.strip()

            # Clean the price text
            try:
                price = float(price_text.replace('€', '').replace(',', '.').replace('net',''))
                coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='changerichelieu',frais_port=10.0)
                session.add(coin)
                session.commit()

                return price
            except ValueError:
                print(f"Failed to convert price text '{price_text}' to float",url)
        else:
            print("Price element not found on page.",url)

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}",url)

    return None