import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get_delivery_price(price):
    if 0 <= price <= 1000:
        return 15.0
    elif 1000.01 <= price <= 2500:
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

def get_price_for(session):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from achat-or-et-argent.fr using requests.
    """
    url = "https://www.achat-or-et-argent.fr/or/20-francs-marianne-coq/17"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific price span element using its ID
        price_element = soup.find('span', id="pa9")

        if price_element:
            # Extract and clean the price text
            price_text = price_element.text.strip().replace('€', '').replace(',', '.')

            try:
                price = float(price_text)
                coin = CoinPrice(nom="20 francs or coq marianne",
                                 j_achete=price,
                                 source=url,
                                 frais_port=get_delivery_price(price))
                session.add(coin)
                session.commit()

                return price
            except ValueError:
                print("Price format could not be parsed.",url)

        else:
            print("Price element not found.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}",url)
    return None  # Return None to indicate an unsuccessful retrieval