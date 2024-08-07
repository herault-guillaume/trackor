import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice
def get_delivery_price(url="https://www.shop-comptoirdelor.be/info/livraison"):
    """
    Extracts shipping and administrative fees from the last row of a delivery price table.

    Args:
        url: The URL of the webpage containing the table.

    Returns:
        A tuple containing the shipping fee (str) and the administrative fee (str),
        or None if the values cannot be extracted.
    """

    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table based on its class
        table = soup.find('table', class_='MsoNormalTable')

        # If the table is found, get all rows and select the last one
        if table:
            rows = table.find_all('tr')
            last_row = rows[-2]

            # If the last row has enough cells (columns), get the desired values
            if len(last_row.find_all('td')) >= 5:
                shipping_fee = float(last_row.find_all('td')[3].get_text(strip=True).replace('€ ','').replace('*','').replace(',','.'))
                admin_fee = float(last_row.find_all('td')[4].get_text(strip=True).replace('€ ','').replace('*','').replace(',','.'))
                return shipping_fee + admin_fee

        # Return None if the table or values are not found
        return -1.0

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the data: {e}")
        return None

def get_price_for(session):
    url = "https://www.shop-comptoirdelor.be/achat-or/pieces/20-francs-or-diverses-ann%C3%A9espays"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }

    try:

        delivery_price = get_delivery_price()
        if delivery_price == -1.0:
            return None

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')


        # Attempt to find the price element (this might fail due to dynamic loading)
        price_element = soup.select_one('strong[itemprop="price"]')

        if price_element:
            price_text = price_element.text.strip()
            price = float(price_text.replace('€', '').replace(',', '.').replace('&nbsp;', ''))

            coin = CoinPrice(nom="20 francs or coq marianne",
                             j_achete=price,
                             source=url,
                             frais_port=delivery_price)
            session.add(coin)
            session.commit()

            return price

        else:
            print("Price element not found on page. Likely due to dynamic content.",url)
            return None

    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}",url)
        return None
