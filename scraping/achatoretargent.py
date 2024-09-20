import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

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

def get_price_for(session,session_id,buy_price):
    """
    Retrieves the '20 francs or coq marianne' coin purchase price from achat-or-et-argent.fr using requests.
    """
    print("https://www.achat-or-et-argent.fr/")

    urls = {
        "20 dollars or liberté": "https://www.achat-or-et-argent.fr/or/20-dollars-us/19",
        "20 francs or coq marianne": "https://www.achat-or-et-argent.fr/or/20-francs-marianne-coq/17",
        "20 francs or napoléon III": "https://www.achat-or-et-argent.fr/or/louis-d-or-20-francs-or/5231",
        "20 francs or helvetia suisse": "https://www.achat-or-et-argent.fr/or/20-francs-suisse/15",
        "20 francs or union latine léopold II": "https://www.achat-or-et-argent.fr/or/union-latine/20",
        "10 dollars or liberté": "https://www.achat-or-et-argent.fr/or/10-dollars-us/13",
        "50 pesos or": "https://www.achat-or-et-argent.fr/or/50-pesos/11",
        "1 oz krugerrand": "https://www.achat-or-et-argent.fr/or/krugerrand/12",
        "10 francs or napoléon III": "https://www.achat-or-et-argent.fr/or/10-francs-napoleon/32",
        "souverain or georges V": "https://www.achat-or-et-argent.fr/or/souverain/14",
        "5 dollars or liberté": "https://www.achat-or-et-argent.fr/or/5-dollars-us/33",
        "10 florins or willem III" : "https://www.achat-or-et-argent.fr/or/10-florins/18",
        "20 mark or wilhelm II" : "https://www.achat-or-et-argent.fr/or/20-reichsmarks/34",
        "1 ducat or" : "https://www.achat-or-et-argent.fr/or/1-ducat-or-francois-joseph-1915/4767",
        "4 ducat or" : "https://www.achat-or-et-argent.fr/or/4-ducats-or/839",
        "20 francs or tunisie" : "https://www.achat-or-et-argent.fr/or/20-francs-tunisie/44",
        "1/2 souverain georges V" : "https://www.achat-or-et-argent.fr/or/demi-souverain/49",
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    # for coin_name, url  in urls.items():
        # try:
    response = requests.get('https://www.achat-or-et-argent.fr/or/2/pieces-d-or-d-investissement', headers=headers)
    response.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(response.content, 'html.parser')

    tableau = soup.find('div',id='contentCategVitrine')

    for row in tableau.find_all('div',class_='row BStooltip align-items-center'):
        try :
            product_url = row.find('a')
            url = 'https://www.achat-or-et-argent.fr'+product_url
            print(url)
            product_name= product_url.find('span').text.strip()
            print(product_name)
            div_prices = row.find('div',class_='row BStooltip align-items-center')
            # Get the 'data-content' attribute
            data_content = div_prices['title data-original-title']

            # Parse the 'data-content' as HTML
            inner_soup = BeautifulSoup(data_content, 'html.parser')
            target_cells = inner_soup.find_all('div', class_='col-6 text-left selected h5')
            price = None
            for cell in target_cells:
                if '€' in cell.find_next_sibling('div').text:
                    price = Price.fromstring(cell.find_next_sibling('div').text.strip())
            print(product_name, price)
            continue

            coin = CoinPrice(nom=coin_name,
                             j_achete=price.amount_float,
                             source=url,
                             prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                         buy_price * poids_pieces_or[coin_name])) * 100.0 / (buy_price *
                                               poids_pieces_or[coin_name]),

                             frais_port=get_delivery_price(price.amount_float),session_id=session_id)
            session.add(coin)
            session.commit()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}",url)
            print(traceback.format_exc())