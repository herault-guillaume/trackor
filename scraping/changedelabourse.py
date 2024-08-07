import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get_delivery_price(price):
    if 0 <= price <= 600:
        return 10.0
    elif 600.01 <= price <= 2500:
        return 20.0
    elif 2500.01 <= price <= 5000:
        return 34.0
    elif 5000.01 <= price <= 7500:
        return 50.0
    elif 7500.01 <= price <= 10000:
        return 56.0
    elif 10000.01 <= price <= 15000:
        return 65.0
    else:  # price > 15000.01
        return 0.0  # Free delivery

def get_price_for(session,session_id):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Change de la Bourse using requests and BeautifulSoup.
    """
    url = "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/napoleon-or-20-francs"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Use a more specific selector to avoid accidental matches
        price_element = soup.select_one("#our_price_display")

        if price_element:
            price_text = price_element.text.strip()

            # More robust price cleaning: handle variations in formatting
            price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))

            coin = CoinPrice(nom="20 francs or coq marianne",
                             j_achete=price,
                             source=url,
                             frais_port=get_delivery_price(price),session_id=session_id)
            session.add(coin)
            session.commit()

            return price
        else:
            print("Price element not found on page.",url)
            return None

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error retrieving or parsing price: {e}",url)
        return None