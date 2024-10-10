import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces
from price_parser import Price
import traceback

#frais de livraison via leur calculette en ligne
coin_name = {
    "Souverain": "or - 1 souverain elizabeth II",  # Assuming you want Elizabeth II
    "Union Latine": "or - 20 francs union latine",
    "20 Reichsmark": "or - 20 mark wilhelm II",
    "20 francs Marianne Coq": "or - 20 francs fr coq marianne",
    "Krugerrand": "or - 1 oz krugerrand",
    "50 pesos": "or - 50 pesos",
    "20 francs Suisse": "or - 20 francs sui vreneli croix",  # Assuming Vreneli
    "5 dollars US": "or - 5 dollars liberté",
    "10 dollars US": "or - 10 dollars liberté",
    "20 dollars US": "or - 20 dollars",
    "20 francs Napoléon": "or - 20 francs fr napoléon III"
}
def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
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
            print(price,coin_name[name],url)
            #price = float(price_text.replace('€', '').replace(',', '.'))

            # Extract and clean:
            #price = float(price_text.replace('€', '').replace(',', '.'))

            if coin_name[name][:2] == 'or':
                coin = CoinPrice(nom=coin_name[name],
                                 j_achete=price.amount_float,
                                 source=url,
                                 prime_achat_perso=((price.amount_float + 15.79) - (
                                             buy_price * poids_pieces[coin_name[name]])) * 100.0 / (buy_price * poids_pieces[
                                                       coin_name[name]]),
                                 frais_port=15.79,session_id=session_id,metal='g')
            session.add(coin)
            session.commit()

        except Exception as e:
            print(traceback.format_exc())
