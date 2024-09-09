import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

#frais de livraison via leur calculette en ligne
coin_name = {
    "Souverain": "souverain or elizabeth II",  # Assuming you want Elizabeth II
    "Union Latine": "20 francs or union latine léopold II",
    "20 Reichsmark": "20 mark or wilhelm II",
    "20 francs Marianne Coq": "20 francs or coq marianne",
    "Krugerrand": "1 oz krugerrand",
    "50 pesos": "50 pesos or",
    "20 francs Suisse": "20 francs or vreneli croix suisse",  # Assuming Vreneli
    "5 dollars US": "5 dollars or liberté",
    "10 dollars US": "10 dollars or liberté",
    "20 dollars US": "20 dollars or liberté",
    "20 francs Napoléon": "20 francs or napoléon III"
}
def get_price_for(session,session_id,buy_price):
    url = 'https://www.lesmetauxprecieux.com/achat-vente-or/pieces-or/'
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic browser behavior

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the price element:
    products_div = soup.find_all("li","ast-article-single")

    for product in products_div :
        try:
            price = Price.fromstring(product.find("span","price").text)
            name_title = product.find("h2","woocommerce-loop-product__title")
            name = name_title.text
            url = product.find('a')['href']
            print(name,price)
            #price = float(price_text.replace('€', '').replace(',', '.'))

            # Extract and clean:
            #price = float(price_text.replace('€', '').replace(',', '.'))

            coin = CoinPrice(nom=coin_name[name],
                             j_achete=price.amount_float,
                             source=url,
                             prime_achat_perso=((price.amount_float + 15.79) - (
                                         buy_price * poids_pieces_or[coin_name[name]])) * 100.0 / (buy_price * poids_pieces_or[
                                                   coin_name[name]]),

                             frais_port=15.79,session_id=session_id)
            session.add(coin)
            session.commit()

        except Exception as e:
            print(traceback.format_exc())
