import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice

#https://www.aucoffre.com/acheter/tarifs-aucoffre-com

def get_price_for(session,session_id):
    """
    Fetches the buy price of the 20 Francs Marianne coin from AuCOFFRE using requests and BeautifulSoup.
    """
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

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content,'html.parser')

        # Use a more specific selector to avoid accidental matches
        price_element = soup.select_one("div[data-url*='20f-marianne'] .text-xlarge.text-bolder.m-0.text-nowrap")

        if price_element:
            price_text = price_element.text.strip()

            # More robust price cleaning: handle variations in formatting
            price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))

            coin = CoinPrice(nom="20 francs or coq marianne",
                             j_achete=price,
                             source=url,
                             frais_port=15.0,session_id=session_id)
            session.add(coin)
            session.commit()

            return price
        else:
            print("Price element not found on page.")
            return None

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error retrieving or parsing price: {e}",url)
        return None