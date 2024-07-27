import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get(session):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """

    url = "https://monlingot.fr/or/achat-piece-or-20-francs-napoleon"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the <td> element containing "de 1 à 9"
        target_element = soup.find('td', text='de 1 à 9')

        if target_element:
            # Get the following <td> element
            price_element = target_element.find_next('td')
            price_text = price_element.text.strip()

            # Clean the price text
            try:
                price = float(price_text.replace('€', '').replace(',', '.').replace(' ', '').replace('\xa0NET',''))

                coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='monlingot')
                session.add(coin)
                session.commit()

                return price

            except (ValueError, IndexError) as e:
                print(f"Failed to parse price: {e}")
        else:
            print("Price element not found on page.")

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}")

    return None  # Return None on failure