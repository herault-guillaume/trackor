import requests
from bs4 import BeautifulSoup
from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights
from price_parser import Price
import re
import logging
from datetime import datetime
import pytz

# Get the logger
logger = logging.getLogger(__name__)

CMN = {
    "https://www.cdt.fr/or/moderne/404-Panda-Chine-piece-15-grammes-Or.html": "or - 1/2 oz panda",
    "https://www.cdt.fr/or/moderne/1319-American-Eagle-USA-1-once-Or.html": "or - 1 oz american eagle",
    "https://www.cdt.fr/or/moderne/1318-Maple-Leaf-Canada-1-once-Or.html": "or - 1 oz maple leaf",
    "https://www.cdt.fr/or/moderne/1317-KANGOUROU-1-OZ-AUSTRALIE.html": "or - 1 oz nugget / kangourou",
    "https://www.cdt.fr/or/moderne/1817-Lunar-III-Dragon-Australie-dizieme-once.html": "or - 1/10 oz dragon 2024 lunar III",
    "https://www.cdt.fr/or/moderne/1806-Lunar-Lievre-Australie-Dixieme-Once-Or.html": "or - 1/10 oz lunar",
    "https://www.cdt.fr/or/moderne/1565-Maple-Leaf-Canada-diziemeoz.html": "or - 1/10 oz maple leaf",
    "https://www.cdt.fr/or/moderne/1809-dizieme-oz-Gold-Britannia-King-Charles-III.html": "or - 1/10 oz britannia",
    "https://www.cdt.fr/or/moderne/1812-1-oz-Gold-Britannia-King-Charles-III.html": "or - 1 oz britannia",
    "https://www.cdt.fr/or/moderne/1818-Lunar-III-Dragon-Australie-quart-once.html": "or - 1/4 oz dragon 2024 lunar III",
    "https://www.cdt.fr/or/moderne/1816-Lunar-III-Dragon-Australie-once.html": "or - 1 oz dragon 2024 lunar III",
    "https://www.cdt.fr/or/moderne/1567-Philharmonique-Autriche-diziemeoz.html": "or - 1/10 oz philharmonique",
    "https://www.cdt.fr/or/moderne/1805-Lunar-Lievre-Australie-Quart-Once-Or.html": "or - 1/4 oz lunar",
    "https://www.cdt.fr/or/moderne/1444-Kangaroo-Australie-quartoz.html": "or - 1/4 oz nugget / kangourou",
    "https://www.cdt.fr/or/moderne/1387-American-Eagle-USA-quartoz.html": "or - 1/4 oz american eagle",
    "https://www.cdt.fr/or/moderne/1381-Philharmonique-Autriche-quart-once-Or.html": "or - 1/4 oz philharmonique",
    "https://www.cdt.fr/or/moderne/1357-quart-ONCE-MAPLE-LEAF-CANADA.html": "or - 1/4 oz maple leaf",
    "https://www.cdt.fr/or/moderne/1470-Krugerrand-New-Afrique-du-Sud-quart-once-or.html": "or - 1/4 oz krugerrand",
    "https://www.cdt.fr/or/moderne/1573-Britannia-Royaume-Unis-quartoz.html": "or - 1/4 oz britannia",
    "https://www.cdt.fr/or/moderne/1386-4-Ducats-New.html": "or - 4 ducats",
    "https://www.cdt.fr/or/moderne/1810-demi-oz-Gold-Britannia-King-Charles-III.html": "or - 1/2 oz britannia",
    "https://www.cdt.fr/or/moderne/1804-Lunar-Lievre-Australie-Demi-Once-Or.html": "or - 1/2 oz lunar",
    "https://www.cdt.fr/or/moderne/1459-Krugerrand-Afrique-du-Sud-demi-Once-or.html": "or - 1/2 oz krugerrand",
    "https://www.cdt.fr/or/moderne/1385-Philharmonique-Autriche-demi-once-Or.html": "or - 1/2 oz philharmonique",
    "https://www.cdt.fr/or/moderne/1380-Kangourou-Australie-demi-once-Or.html": "or - 1/2 oz nugget / kangourou",
    "https://www.cdt.fr/or/moderne/1377-American-Eagle-USA-demi-once-Or.html": "or - 1/2 oz american eagle",
    "https://www.cdt.fr/or/moderne/1336-Maple-Leaf-Canada-demi-once-Or.html": "or - 1/2 oz maple leaf",
    "https://www.cdt.fr/or/moderne/1560-Britannia-Royaume-Unis-demioz.html": "or - 1/2 oz britannia",
    "https://www.cdt.fr/or/moderne/1426-Panda-Chine-piece-30-grammes-or.html": "or - 1 oz panda",
    "https://www.cdt.fr/or/moderne/1803-Lunar-Lievre-Australie-1-once-Or.html": "or - 1 oz lunar",
    "https://www.cdt.fr/or/moderne/1460-Krugerrand-New-Afrique-du-Sud-1-once-or.html": "or - 1 oz krugerrand",
    "https://www.cdt.fr/or/moderne/1379-Buffalo-USA-1-once-Or.html": "or - 1 oz buffalo",
    "https://www.cdt.fr/or/moderne/1378-Britannia-Royaume-Unis-1-once-Or.html": "or - 1 oz britannia",
    "https://www.cdt.fr/or/moderne/1363-Philharmonique-Autriche-1-once-Or.html": "or - 1 oz philharmonique",
    "https://www.cdt.fr/or/bourse-cours/123-20-Francs-Napoleon.html": "or - 20 francs fr",
    "https://www.cdt.fr/or/bourse-cours/125-20-Francs-Tunisie.html": "or - 20 francs tunisie",
    "https://www.cdt.fr/or/bourse-cours/124-20-Francs-Croix-Suisse.html": "or - 20 francs sui vreneli croix",
    "https://www.cdt.fr/or/bourse-cours/126-20-Francs-Union-Latine.html": "or - 20 francs union latine",
    "https://www.cdt.fr/or/bourse-cours/122-20-Dollars-US.html": "or - 20 dollars",
    "https://www.cdt.fr/or/bourse-cours/103-10-Dollars-US-Liberty.html": "or - 10 dollars liberté",
    "https://www.cdt.fr/or/bourse-cours/137-5-Dollars-liberty.html": "or - 5 dollars liberté",
    "https://www.cdt.fr/or/bourse-cours/141-10-Francs-Napoleon.html": "or - 10 francs fr",
    "https://www.cdt.fr/or/bourse-cours/212-Krugerrand.html": "or - 1 oz krugerrand",
    "https://www.cdt.fr/or/bourse-cours/121-20-DeutschMarks.html": "or - 20 mark",
    "https://www.cdt.fr/or/bourse-cours/144-50-Pesos.html": "or - 50 pesos mex",
    "https://www.cdt.fr/or/bourse-cours/151-Souverain-Elizabeth.html": "or - 1 souverain elizabeth II",
    "https://www.cdt.fr/or/bourse-cours/150-Souverain.html": "or - 1 souverain",
    "https://www.cdt.fr/or/bourse-cours/108-10-Florins.html": "or - 10 florins",
    "https://www.cdt.fr/or/bourse-cours/100-demi-Souverain.html": "or - 1/2 souverain",
    "https://www.cdt.fr/argent/moderne/1458-Kookaburra-Australie-1-once-argent.html": "ar - 1 oz nugget / kangourou",
    "https://www.cdt.fr/argent/moderne/182-Libertad-Mexique-1-once-argent-1oz.html": "ar - 1 oz libertad",
    "https://www.cdt.fr/argent/moderne/1819-Lunar-III-Dragon-Australie-once-Argent.html": "ar - 1 oz dragon 2024 lunar III",
    "https://www.cdt.fr/argent/moderne/1465-Panda-Chine-30-grammes-30g-argent.html": "ar - 10 yuan panda 30g",
    "https://www.cdt.fr/argent/moderne/1813-1oz-King-Charles-III-Silver.html": "ar - 1 oz britannia",
    "https://www.cdt.fr/argent/moderne/1801-Lunar-Lievre-Australie-1-once-argent.html": "ar - 1 oz lunar", # Assuming this is the Lunar series
    "https://www.cdt.fr/argent/moderne/1492-Krugerrand-New-Afrique-du-Sud-1-once-Argent.html": "ar - 1 oz krugerrand",
    "https://www.cdt.fr/argent/moderne/1428-Silver-Eagle-USA-1oz.html": "ar - 1 oz american eagle",
    "https://www.cdt.fr/argent/moderne/1413-Kangourou-Australie-1-once-argent-1oz.html": "ar - 1 oz kangourou",
    "https://www.cdt.fr/argent/moderne/1364-Koala-Australie-1oz.html": "ar - 1 oz koala",
    "https://www.cdt.fr/argent/moderne/1312-Maple-Leaf-Canada-1-once-argent-1oz.html": "ar - 1 oz maple leaf",
    "https://www.cdt.fr/argent/moderne/1315-Philharmonique-Autriche-1-once-argent-1oz.html": "ar - 1 oz philharmonique",
    "https://www.cdt.fr/argent/moderne/1359-Kookaburra-Australie-piece-argent-1kg.html": "ar - 1 kg nugget / kangourou", # Assuming Kookaburra is the same as Nugget/Kangaroo
    "https://www.cdt.fr/argent/moderne/1337-Koala-Australie-piece-argent-1kg.html": "ar - 1 kg koala",
    "https://www.cdt.fr/argent/moderne/1474-Boite-250-onces-Kangourou-Australie-argent.html": ("ar - 1 oz kangourou", 250),
    "https://www.cdt.fr/argent/moderne/1477-Boite-500-onces-Silver-Eagle-USA-argent.html": ("ar - 1 oz american eagle", 500),
    "https://www.cdt.fr/argent/moderne/1476-Boite-500-onces-Philharmonique-Autriche-argent.html": ("ar - 1 oz philharmonique", 500),
    "https://www.cdt.fr/argent/moderne/1475-Boite-500-onces-Maple-Leaf-Canada-argent.html": ("ar - 1 oz maple leaf", 500),
    "https://www.cdt.fr/argent/demonetise/51-10-Francs-Hercule-1964-1973.html": "ar - 10 francs fr hercule (1965-1973)",
    "https://www.cdt.fr/argent/demonetise/52-10-Francs-Turin-1929-1939.html": "ar - 10 francs fr turin (1929-1939)",
    "https://www.cdt.fr/argent/demonetise/54-20-Francs-Turin-1929-1939.html": "ar - 20 francs fr turin (1929-1939)",
    "https://www.cdt.fr/argent/demonetise/55-5-Francs-Semeuse-1959-1969.html": "ar - 5 francs fr semeuse (1959-1969)",
    "https://www.cdt.fr/argent/demonetise/56-50-Francs-Hercule-1974-1980.html": "ar - 50 francs fr hercule (1974-1980)",
    "https://www.cdt.fr/argent/demonetise/57-5-francs-Ecus-1795-1889-argent.html": "ar - 5 francs fr ecu (1854-1860)", # Assuming this refers to the Ecu
    "https://www.cdt.fr/argent/demonetise/174-2-francs-Semeuse-1898-1920-argent.html": "ar - 2 francs fr semeuse",
    "https://www.cdt.fr/argent/demonetise/175-1-Franc-Semeuse-1898-1920.html": "ar - 1 franc fr semeuse",
    "https://www.cdt.fr/argent/demonetise/176-50-Centimes-Semeuse-1897-1920-argent.html": "ar - 50 centimes francs fr semeuse",
    "https://www.cdt.fr/argent/demonetise/911-100-Francs-1982-Argent.html": "ar - 100 francs fr", # Assuming this is the 100 Francs

}

def get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver=None):
    """
    Retrieves the 'or - 20 francs coq marianne' coin purchase price from Oretchange using requests and BeautifulSoup.
    """
    logger.debug("https://www.cdt.fr")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    delivery_ranges = [(0, 400, 10.0),(400.0, 800, 15.0), (800.0, 900, 21.0)] + [ (900.0 + (i * 100), 900.0 + ((i+1) * 100), 21.0 + (0.2 * (i+1))) for i,v in enumerate(range(900,15000,100))] + [(15000.00, 999999999999.9, 0.01)]

    for url,item_data in CMN.items():
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find('table', class_='bord uk-table')
            if table.find('th', string=lambda text: "courtage" in text):
                continue

            minimum=None
            price_ranges =[]
            for row in table.find_all('tr')[1:]:

                cols = row.find_all('td')
                quantity_str = cols[0].text.strip()
                price_str = cols[1].text.strip()

                # Parse quantity
                if "à" in quantity_str:
                    min_q, max_q = map(int, re.findall(r'\d+', quantity_str))
                    if minimum is None:  # Save the first minimum
                        minimum = min_q
                    price_ranges.append((min_q, max_q, Price.fromstring(price_str)))

                elif "plus de" in quantity_str or "et plus" in quantity_str :
                    min_q = int(re.findall(r'\d+', quantity_str)[0])
                    price_ranges.append((min_q, 999999999999.9,Price.fromstring(price_str)))
                    if minimum is None:  # Save the first minimum
                        minimum = min_q
                elif "indifférente" in quantity_str:
                    price_ranges.append((1, 9999999999,Price.fromstring(price_str)))
                    if minimum is None:  # Save the first minimum
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


            def price_between(value, ranges):
                """
                Returns the price per unit for a given quantity.
                """

                for min_qty, max_qty, price in ranges:
                    if min_qty <= value < max_qty:
                        if isinstance(price, Price):
                            return price.amount_float
                        else:
                            return price

            coin = Item(name=name,
                        price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                        buy_premiums=';'.join(
                            ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price * weights[name][0] * weights[name][1])) * 100.0 / (buy_price * weights[name][0] * weights[name][1])) for i in range(1, minimum)] +
                            ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price * weights[name][0] * weights[name][1])) * 100.0 / (buy_price * weights[name][0] * weights[name][1])) for i in range(minimum, 751)]
                        ),
                        delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                        source=url,
                        session_id=session_id,
                        bullion_type=bullion_type,
                        quantity=quantity,
                        minimum=minimum, timestamp=datetime.now(pytz.timezone('CET')))
            print(name,url,price_ranges)
            session_prod.add(coin)
            session_prod.commit()


        except KeyError as e:
            logger.error(f"KeyError: {name}")

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")

        except Exception as e:
            logger.error(f"An error occurred while processing: {e}")
