import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get(session):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Joubert Change using requests and BeautifulSoup.
    """
    url = "https://www.joubert-change.fr/or-investissement/cours/piece-or-78-20-francs-napoleon.html?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for

        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the price element using a more specific CSS selector
        price_element = soup.find('small', text=lambda text: text and 'min. 5' in text)

        if price_element:
            # Extract the price text from the parent td element
            price_text = price_element.parent.text.strip()

            # Clean the price text, handling variations in formatting and potential errors
            try:
                price = float(price_text.split()[0].replace('€', '').replace(',', '.'))  # Take the first element after splitting on whitespace
                coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='joubertchange')
                session.add(coin)
                session.commit()

                return price
            except ValueError:
                print(f"Failed to convert price text '{price_text}' to float")
        else:
            print("Price element not found on page.")

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}")

    return None  # Return None on failure