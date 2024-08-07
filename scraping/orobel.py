import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice
def get_delivery_price(price):
    """
    https://www.orobel.biz/shop/livraisons
    """
    if 1 <= price <= 49.99:
        return 15.0
    elif 50 <= price <= 4999.99:
        return 35.0
    elif 5000 <= price <= 9999.99:
        return 75.0
    elif 10000 <= price <= 14999.99:
        return 90.0
    elif 15000 <= price <= 29999.99:
        return 120.0
    elif 30000 <= price <= 39999.99:
        return 200.0
    elif 40000 <= price <= 44999.99:
        return 235.0
    else :
        return 300.0

def get_price_for(session,session_id):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from Goldforex using requests and BeautifulSoup.
    """

    url = "https://www.orobel.biz/produit/acheter-piece-or-20-francs-marianne-en-ligne-orobel"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')


        # Use a more specific CSS selector to target the price element
        price_element = soup.select_one('span.woocommerce-Price-amount.amount bdi')  # Find the <bdi> element within the <span>

        if price_element:
            price_text = price_element.text.strip()

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