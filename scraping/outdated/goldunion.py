import requests
from bs4 import BeautifulSoup
from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights


#gold union faq combien coute une expédition

def get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver=None):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    url = "https://goldunion.fr/products/20-francs-coq"
    print(url)

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
                    coin = Item(name="or - 20 francs coq marianne",
                                prices=price,
                                source='https://goldunion.fr/products/20-francs-coq',
                                buy_premiums=((price.amount_float + get_delivery_price(price.amount_float)) - (buy_price * weights[CMN])) * 100.0 / (buy_price * weights[CMN]),

                                delivery_fee=20.0, session_id=session_id, bullion_type='g')
                    session_prod.add(coin)
                    session_prod.commit()

                    return price
                except ValueError:
                    print(f"Failed to convert price text '{price_text}' to float",url)
        else:
            print("Price element not found on page.",url)

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}",url)

    return None