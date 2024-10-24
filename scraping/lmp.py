import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback

#frais de livraison via leur calculette en ligne
CMN = {
    "Souverain": "or - 1 souverain elizabeth II",  # Assuming you want Elizabeth II
    "Union Latine": "or - 20 francs union latine",
    "20 Reichsmark": "or - 20 mark wilhelm II",
    "20 francs Marianne Coq": "or - 20 francs fr coq marianne",
    "Krugerrand": "or - 1 oz krugerrand",
    "50 pesos": "or - 50 pesos mex",
    "20 francs Suisse": "or - 20 francs sui vreneli croix",  # Assuming Vreneli
    "5 dollars US": "or - 5 dollars liberté",
    "10 dollars US": "or - 10 dollars liberté",
    "20 dollars US": "or - 20 dollars",
    "20 francs Napoléon": "or - 20 francs fr napoléon III",

    "10 Francs Turin": "ar - 10 francs fr turin (1860-1928)",
    "5 francs semeuse": "ar - 5 francs fr semeuse (1959-1969)",
    "50 Francs Hercule": "ar - 50 francs fr hercule (1974-1980)",
    "20 Francs Turin": "ar - 20 francs fr turin (1929-1939)",
    "10 Francs Hercule": "ar - 10 francs fr turin (1860-1928)",

}
def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    urls = ['https://www.lesmetauxprecieux.com/achat-vente-or/pieces-or/','https://www.lesmetauxprecieux.com/achat-vente-argent/piece-argent/']

    headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic browser behavior
    for url in urls :
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
                print(price,CMN[name],url)
                #price = float(price_text.replace('€', '').replace(',', '.'))

                bullion_type = CMN[name][:2]
                # Extract and clean:
                #price = float(price_text.replace('€', '').replace(',', '.'))
                if bullion_type == 'or':
                    buy_price = buy_price_gold
                else:
                    buy_price = buy_price_silver

                coin = Item(name=CMN[name],
                            prices=price.amount_float,
                            source=url,
                            buy_premiums=((price.amount_float + 15.79) - (
                                             buy_price * poids_pieces[CMN[name]])) * 100.0 / (buy_price * poids_pieces[
                                                       CMN[name]]),
                            delivery_fee=15.79,
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=1,
                            minimum=1)
                session.add(coin)
                session.commit()

            except Exception as e:
                print(traceback.format_exc())
