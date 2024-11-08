import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import logging
# Get the logger
logger = logging.getLogger(__name__)

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
    logger.debug('https://www.lesmetauxprecieux.com/achat-vente-or/pieces-or/')
    headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic browser behavior
    for url in urls :
        try :
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

                    # Extract and clean:
                    item_data = CMN[name]
                    minimum = 1
                    quantity = 1
                    if isinstance(item_data, tuple):
                        name = item_data[0]
                        quantity = item_data[1]
                        bullion_type = item_data[0][:2]
                    else:
                        name = item_data
                        bullion_type = item_data[:2]

                    if bullion_type == 'or':
                        buy_price = buy_price_gold
                    else:
                        buy_price = buy_price_silver

                    delivery_ranges = [(0.0,9999999.9,15.79)]
                    price_ranges = [(minimum,999999999,price)]

                    def price_between(value, ranges):
                        """
                        Returns the price per unit for a given quantity.
                        """
                        for min_qty, max_qty, price in ranges:
                            if min_qty <= value <= max_qty:
                                if isinstance(price, Price):
                                    return price.amount_float
                                else:
                                    return price

                    coin = Item(name=name,
                                price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                                buy_premiums=';'.join(
        ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(1,minimum)] +
        ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(minimum,151)]
                                ),
                                delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                                source=url,
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum)

                    session.add(coin)
                    session.commit()


                except KeyError as e:
                    logger.error(f"KeyError: {name}")

                except Exception as e:
                    logger.error(f"An error occurred while processing a product: {e}")
                    traceback.print_exc()

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            traceback.print_exc()
