import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

def get_delivery_price(price):
    #https://www.changerichelieu.fr/livraison
    if price <= 600.0:
        return 10.0
    elif 600.0 < price <= 2500.0 :
        return 20.0
    elif 2500.0 < price <= 5000.0 :
        return 34.0
    elif 5000.0 < price <= 7500.0 :
        return 50.0
    elif 7500.0 < price <= 10000.0 :
        return 56.0
    elif 10000.0 < price <= 15000.0 :
        return 65.0
    else :
        return 0.0

def get_price_for(session,session_id):
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
                coin = CoinPrice(nom="20 francs or coq marianne",
                                 j_achete=price,
                                 source=url,
                                 frais_port=get_delivery_price(price),session_id=session_id)
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