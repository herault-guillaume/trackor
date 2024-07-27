import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get(session):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from BDOR using requests and BeautifulSoup.
    """
    url = "https://www.bdor.fr/achat-or-en-ligne/piece-d-or-20-francs-coq-marianne"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific table row (tr) that contains the price
        target_row = soup.find('tr', text=lambda text: text and "1 à 20" in text)
        if target_row:
            price_cell = target_row.find_next_sibling('tr').find('td')

            if price_cell:
                # Clean the price text and convert to float
                price_text = price_cell.text.strip().replace('€', '').replace(',', '.').replace(' net', '')
                try:
                    price = float(price_text)
                    coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='bdor')
                    session.add(coin)
                    session.commit()

                    return price
                except ValueError:
                    print("Price format could not be parsed.",url)
            else:
                print("Price cell not found in the table.",url)
        else:
            print("Target row not found in the table.",url)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}",url)

    return None  # Return None to indicate an unsuccessful retrieval