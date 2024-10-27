import requests
from bs4 import BeautifulSoup
from models.model import Item, poids_pieces
from price_parser import Price
import traceback

CMN = {
    "20 Francs Or Napoléon type Coq": 'or - 20 francs fr coq marianne',
    "Souverain Or Georges": 'or - 1 souverain georges V',
    "50 Pesos Or Mexique": 'or - 50 pesos mex',
    "Krugerrand Or Afrique du Sud": 'or - 1 oz krugerrand',
    "20 Francs Or Suisse": 'or - 20 francs sui vreneli croix',
    "20 Dollars Or": 'or - 20 dollars liberté longacre',
    "10 Dollars Or": 'or - 10 dollars liberté',
    "10 Francs Or": 'or - 10 francs fr coq marianne',
    "20 Francs Union Latine Or": 'or - 20 francs union latine',
    "10 Florins Or Hollandais": 'or - 10 florins wilhelmina', # or 'or - 10 florins willem III' depending on the specific coin
    "20 Francs Or Tunisie": 'or - 20 francs tunisie',
    "Souverain Elisabeth  II Or": 'or - 1 souverain elizabeth II',
    "1/2 Souverain Or": 'or - 1/2 souverain georges V', # or 'or - 1/2 souverain victoria' depending on the specific coin
    "5 Dollars Or": 'or - 5 dollars liberté',
    "20 Marks Or": 'or - 20 mark wilhelm II',
    "Lingot Or 1 kg": 'or - lingot 1 kg LBMA',
    "Lingotin Or 500 grammes": 'or - lingot 500 g LBMA',
    "Lingotin Or  250 grammes": 'or - lingot 250 g LBMA',
    "Lingotin Or 100 grammes": 'or - lingot 100 g LBMA',
    "Lingotin Or 50 grammes": 'or - lingot 50 g LBMA',
    "Lingotin Or 20 grammes": 'or - lingot 20 g LBMA',
    "Lingotin Or 10 grammes": 'or - lingot 10 g LBMA',
    "Lingotin Or 5 grammes": 'or - lingot 5 g LBMA',
    "Lingotin Once Or": 'or - lingot 1 once LBMA',
    "Lingotin Or 2 Grammes": "or - lingot 2 g", # Assuming this is the intended match, adjust if needed
    "Lingotin Or 1 Gramme": "or - lingot 1 g",
    "5 R. Nicolas II": "or - 5 roubles",

    "50 Francs Hercule Argent": "ar - 50 francs fr hercule (1974-1980)",
    "10 Francs Hercule Argent": "ar - 10 francs fr hercule (1965-1973)",
    "5 Francs Semeuse": "5 francs fr semeuse (1959-1969)",
    "2 Francs Semeuse": "ar - 2 francs fr semeuse",
    "1 Franc Semeuse": "ar - 1 franc fr semeuse",
    "50 Centimes Semeuse": "ar - 50 centimes francs fr semeuse",
    "5 Francs Ecu 3 Têtes": "ar - 5 francs fr ecu (1854-1860)",
    "20 Francs Turin Argent": "ar - 20 francs fr turin (1860-1928)",
    "10 Francs Turin Argent": "ar - 10 francs fr turin (1860-1928)",
    "100 Francs Argent tous modèles": "ar - 100 francs fr",
    "Once D'Argent USA": "ar - 1 oz silver eagle",
    "Once Argent Autriche": "ar - 1 oz philharmonique",
    "Once Argent Chine Panda": "ar - 10 yuan panda 30g",
    "Once Argent Maple Leaf Canada": "ar - 1 oz maple leaf",
}



# https://www.merson.fr/fr/content/1-livraison
def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    urls = ["https://www.merson.fr/fr/18-achat-or-investissement","https://www.merson.fr/fr/21-argent-achat"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    for url in urls :
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the span element with class "result2"
        products_div = soup.find_all("div",'product-container')

        for product in products_div:
            try:
                price = Price.fromstring(product.find("span", "price product-price").text)
                name_title = product.find("h5", "product-name")
                name = name_title.text.strip()
                url = name_title.find('a')['href']
                print(price,CMN[name],url)

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

                delivery_ranges = [(0.0,2000.0,8.9),(2000.0,float('inf'),18.90)]
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
    ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges)*i,delivery_ranges)/(quantity*i)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(minimum,151)]
                            ),
                            delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                            source=url,
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=quantity,
                            minimum=minimum)

                session.add(coin)
                session.commit()

            except Exception as e:
                print(traceback.format_exc())