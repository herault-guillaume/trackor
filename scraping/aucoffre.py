import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

#https://www.aucoffre.com/acheter/tarifs-aucoffre-com

def get_price_for(session,session_id,buy_price):
    """
    Fetches the buy price of the 20 Francs Marianne coin from AuCOFFRE using requests and BeautifulSoup.
    """
    print('https://www.aucoffre.com/')
    urls = {
        '20 francs or coq marianne': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-1/produit","20f-marianne"],
        '20 francs or napoléon III': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-1/produit","napoleon-20f-napoleon-iii-tete-nue"],
        '20 francs or génie debout': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-1/produit","napoleon-20f-genie"],
        '20 francs or cérès': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-1/produit","napoleon-20f-ceres"],
        '10 francs or cérès 1850-1851': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-7/produit","demi-napoleon-10f-ceres"],
        '10 francs or coq marianne': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-7/produit","demi-napoleon-10f-marianne-coq"],
        '10 francs or napoléon III': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-7/produit","demi-napoleon-10f-napoleon-iii"],
        '40 francs or napoléon empereur lauré': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-11/produit","napoleon-40f"],
        '50 francs or napoléon III tête nue': ["https://www.aucoffre.com/recherche/marketing_list-5/stype-12/produit","napoleon-50f"],
        '100 francs or napoléon III tête nue': ["https://www.aucoffre.com/recherche/marketing_list-5/stype-13/produit","napoleon-100f"],
        '20 francs or vreneli croix suisse': ["https://www.aucoffre.com/recherche/marketing_list-6/stype-180/produit","20-francs-suisse-vreneli"],
        '20 francs or union latine léopold II': ["https://www.aucoffre.com/recherche/stype-51/produit","union-latine"],
        '20 dollars or liberté': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-9/stype-8/produit","20-dollars-us-double-eagle-liberty"],
        '10 dollars or liberté': ["https://www.aucoffre.com/recherche/metal-1/marketing_list-9/stype-56/produit","10-dollars-us-liberty"],
        'souverain or georges V': ["https://www.aucoffre.com/recherche/marketing_list-8/stype-3/produit","souverain-george-v"],
        '1/2 souverain georges V': ["https://www.aucoffre.com/recherche/marketing_list-8/stype-16/produit","demi-souverain"],
        'souverain or elizabeth II': ["https://www.aucoffre.com/recherche/marketing_list-8/stype-6/produit","souverain-elisabeth-ii"],
        'souverain or victoria jubilee': ["https://www.aucoffre.com/recherche/marketing_list-8/stype-3/produit","souverain-victoria-jubilee"],
        '20 mark or wilhelm II': ["https://www.aucoffre.com/recherche/stype-73/produit","20-mark-allemand-wilhelm-ii"],
        '1 oz maple leaf': ["https://www.aucoffre.com/recherche/marketing_list-12/stype-18/produit","maple-leaf-1-once-50-dollars-elizabeth-ii"],
        '1 oz krugerrand': ["https://www.aucoffre.com/recherche/marketing_list-7/stype-2/produit","krugerrand-1-once"],
        '1 oz buffalo': ["https://www.aucoffre.com/recherche/marketing_list-10/stype-131/produit","buffalo-1-once-50-dollars-us"],
        '1 oz nugget / kangourou': ["https://www.aucoffre.com/recherche/marketing_list-13/stype-21/produit","australian-nugget-1-once"],
        "50 pesos or": ["https://www.aucoffre.com/recherche/marketing_list-11/stype-9/produit","50-pesos"],  # Approximatif
        "20 pesos or": ["https://www.aucoffre.com/recherche/marketing_list-11/stype-84/produit","20-pesos"],  # Approximatif
        "10 pesos or": ["https://www.aucoffre.com/recherche/marketing_list-11/stype-68/produit","10-pesos"],  # Approximatif
        "5 pesos or": ["https://www.aucoffre.com/recherche/stype-67/produit","5-pesos"],  # Approximatif
        "2 1/2 pesos or": ["https://www.aucoffre.com/recherche/marketing_list-11/stype-66/produit","2-1-2-pesos"],  # Approximatif
        '1/2 oz maple leaf': ["https://www.aucoffre.com/recherche/marketing_list-12/stype-33/produit","maple-leaf-1-2-once"],
        '1/4 oz maple leaf': ["https://www.aucoffre.com/recherche/marketing_list-12/stype-32/produit","maple-leaf-1-4-once"],
        '1/10 oz maple leaf': ["https://www.aucoffre.com/recherche/marketing_list-12/stype-31/produit","maple-leaf-1-10-once"],
        '1/20 oz maple leaf': ["https://www.aucoffre.com/recherche/marketing_list-12/stype-132/produit","maple-leaf-1-20-once"],
        '1/2 oz krugerrand': ["https://www.aucoffre.com/recherche/marketing_list-7/stype-23/produit","krugerrand-1-2-once"],
        '1/4 oz krugerrand': ["https://www.aucoffre.com/recherche/marketing_list-7/stype-14/produit","krugerrand-1-4-once"],
        '1/10 oz krugerrand': ["https://www.aucoffre.com/recherche/marketing_list-7/stype-15/produit","krugerrand-1-10-once"],
        '1/2 oz american eagle': ["https://www.aucoffre.com/recherche/marketing_list-10/stype-44/produit","eagle-1-2-once"],
        '1/4 oz american eagle': ["https://www.aucoffre.com/recherche/marketing_list-10/stype-45/produit","eagle-1-4-once"],
        '1/10 oz american eagle': ["https://www.aucoffre.com/recherche/marketing_list-10/stype-46/produit","eagle-1-10-once"],
        '1/2 oz nugget / kangourou': ["https://www.aucoffre.com/recherche/marketing_list-13/stype-35/produit","australian-nugget-1-2-once"],
        '1/4 oz nugget / kangourou': ["https://www.aucoffre.com/recherche/stype-36/produit","australian-nugget-1-4-once"],
        '1/10 oz nugget / kangourou': ["https://www.aucoffre.com/recherche/marketing_list-13/stype-37/produit","australian-nugget-1-10-once"],
        '1/20 oz nugget / kangourou': ["https://www.aucoffre.com/recherche/marketing_list-13/stype-38/produit","australian-nugget-1-20-once"],
        '20 francs or helvetia suisse': ["https://www.aucoffre.com/recherche/marketing_list-6/stype-5/produit","20-francs-suisse-vreneli-1901"],
        '10 francs or vreneli croix suisse': ["https://www.aucoffre.com/recherche/marketing_list-6/stype-55/produit","demi-vreneli-10"]
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    for coin_name, url in urls.items():
        try:
            response = requests.get(url[0], headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            soup = BeautifulSoup(response.content,'html.parser')

            # Use a more specific selector to avoid accidental matches
            elements = soup.select("div[data-url*='{coin_name}']".format(coin_name=url[1]))

            for element in elements :
                element_location = element.find("dl","dl-horizontal dl-left dl-small mb-0")

                img_tag = element_location.find('img')

                if not img_tag['title'] == 'Localisation France (FR)' :
                    continue

                price_element = element.select_one("div[data-url*='{coin_name}'] .text-xlarge.text-bolder.m-0.text-nowrap".format(coin_name=url[1]))

                if price_element :

                    price_text = price_element.text.strip()

                    price = Price.fromstring(price_text)
                    print(price,url)
                    # More robust price cleaning: handle variations in formatting
                    #price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))

                    coin = CoinPrice(nom=coin_name,
                                     j_achete=price.amount_float,
                                     source=url[0],
                                     prime_achat_perso=((price.amount_float + 15.0) - (buy_price * poids_pieces_or[
                                         coin_name])) * 100.0 / (buy_price * poids_pieces_or[coin_name]),

                                     frais_port=15.0,session_id=session_id,metal='g')
                    session.add(coin)
                    session.commit()

                else:
                    print("Price element not found on page.", url)
                break
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error retrieving or parsing price: {e}",url)
            print(traceback.format_exc())