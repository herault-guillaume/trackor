import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get_delivery_price(price):
    if price <= 1000.0:
        return 10.0
    elif price > 1000.0:
        return 25.0
# forfait

def get_price_for(session,session_id):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """

    url = "https://www.goldreserve.fr/produit/napoleon-20-francs-coq-marianne/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')


        # Use a more specific CSS selector to target the price element
        price_elements = soup.select('span.woocommerce-Price-amount.amount bdi')  # Find the <bdi> element within the <span>

        if price_elements:
            price_text = price_elements[1].text.strip()

            # Clean the price text
            try:
                price = float(price_text.replace('€', '').replace(',', '.'))
                coin = CoinPrice(nom="20 francs or coq marianne",
                                 j_achete=price,
                                 source=url,
                                 frais_port=get_delivery_price(price),session_id=session_id)
                session.add(coin)
                session.commit()

                return price

            except (ValueError, IndexError) as e:
                print(f"Failed to parse price: {e}",url)
        else:
            print("Price element not found on page.",url)

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}",url)

    return None  # Return None on failure