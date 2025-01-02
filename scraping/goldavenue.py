from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights
from price_parser import Price
import traceback
import logging
from datetime import datetime
import pytz

# Get the logger
logger = logging.getLogger(__name__)

urls = {
    'or - 1 oz philharmonique': 'https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pur-999-9-philharmonique-annees-mixtes',
    'or - 20 francs fr napoléon III': "https://www.goldavenue.com/fr/acheter/or/produit/20-francs-piece-d-or-napoleon-iii-avec-ou-sans-couronne-de-laurier",
    'or - 20 francs fr coq marianne': "https://www.goldavenue.com/fr/acheter/or/produit/piece-d-or-pur-900-0-20-francs-napoleon-coq-de-chaplain",
    'or - 40 francs fr napoléon empereur laurée': "https://www.goldavenue.com/fr/acheter/or/produit/piece-de-monnaie-d-or-pur-900-0-40-francs-napoleon-bonaparte-premier-consul-an-xi",
    'or - 50 francs fr napoléon III tête nue': "https://www.goldavenue.com/fr/acheter/or/produit/piece-de-monnaie-d-or-pur-900-0-50-francs-napoleon-iii-tete-nue-1855-a-paris",
    'or - 100 francs fr napoléon III tête laurée': "https://www.goldavenue.com/fr/acheter/or/produit/piece-de-monnaie-d-or-pur-900-0-100-francs-napoleon-iii-tete-lauree-1869-a",
    'or - 20 francs sui vreneli croix': "https://www.goldavenue.com/fr/acheter/or/produit/piece-d-or-pur-900-0-vreneli-20-francs-suisse-helvetia-annees-mixtes",
    'or - 1 souverain victoria jubilee': "https://www.goldavenue.com/fr/acheter/or/produit/piece-souverain-or-victoria-or-pur-916-7",
    'or - 1 souverain edouart VII': "https://www.goldavenue.com/fr/acheter/or/produit/souverain-en-or-pur-916-7-roi-edouard-vii",
    'or - 1 souverain elizabeth II': "https://www.goldavenue.com/fr/acheter/or/produit/piece-d-or-pur-916-7-souverain-elizabeth-bu-annees-mixtes",
    'or - 1 oz maple leaf': "https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pur-999-9-maple-leaf-annee-aleatoire",
    'or - 1 oz krugerrand': "https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pur-916-7-krugerrand-annees-mixtes",
    'or - 1 oz american eagle': "https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pur-916-7-american-eagle-bu-annees-mixtes",
    'or - 1 oz nugget / kangourou': "https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pure-999-9-perth-mint-kangourou-bu-mixed-years",
    'or - 1/2 oz maple leaf': "https://www.goldavenue.com/fr/acheter/or/produit/1-2-once-piece-d-or-maple-leaf-4f8cd2d7-fb76-4169-8f34-ebc3539675f7",
    'or - 1/4 oz maple leaf': "https://www.goldavenue.com/fr/acheter/or/produit/1-4-once-piece-d-or-maple-leaf-db8f368c-0fa2-4e01-99c3-dbd14e34d8f5",
    'or - 1/10 oz maple leaf': "https://www.goldavenue.com/fr/acheter/or/produit/1-10-once-piece-d-or-pur-999-9-maple-leaf-bu-annees-mixtes",
    'or - 1/2 oz krugerrand': "https://www.goldavenue.com/fr/acheter/or/produit/1-2-once-piece-d-or-krugerrand-08af2735-b4e0-4928-9c58-033e187fa5df",
    'or - 1/4 oz krugerrand': "https://www.goldavenue.com/fr/acheter/or/produit/1-4-once-piece-d-or-krugerrand-2911fe96-82da-4a42-bed3-25a39c95a915",
    'or - 1/10 oz krugerrand': "https://www.goldavenue.com/fr/acheter/or/produit/1-10-once-piece-d-or-pur-916-7-krugerrand-annees-mixtes",
    'or - 1/2 oz american eagle':"https://www.goldavenue.com/fr/acheter/or/produit/1-2-once-piece-d-or-american-eagle-6bdd8b58-0191-4fe2-8968-64134a4b19cb",
    'or - 1/4 oz american eagle': "https://www.goldavenue.com/fr/acheter/or/produit/1-4-once-piece-d-or-american-eagle-fb260cc5-f784-4831-bfdc-f477a0012208",
    'or - 1/10 oz american eagle': "https://www.goldavenue.com/fr/acheter/or/produit/1-10-once-piece-d-or-pur-916-7-american-eagle-bu-annees-mixtes",
    'or - 1/2 oz nugget / kangourou': "https://www.goldavenue.com/fr/acheter/or/produit/1-2-once-piece-d-or-kangaroo",
    'or - 1/4 oz nugget / kangourou': "https://www.goldavenue.com/fr/acheter/or/produit/1-4-once-piece-d-or-kangaroo",
    'or - 10 francs sui vreneli croix': "https://www.goldavenue.com/fr/acheter/or/produit/10-francs-piece-d-or-suisse-vreneli"
}



def get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver=None):
    if not driver:
        driver = Driver(uc=True, headless=True)
    logger.debug("https://www.goldavenue.com/")
    for CMN, url in urls.items():
        try:
            driver.get(url)  # Load the page
            # Locate the price element by its unique combination of classes
            # Wait for the span element to be present (adjust timeout as needed)
            span_discount = None
            span_price = None
            try :
                span_discount = WebDriverWait(driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//p[@color='danger' and @display='inline']"))
                )
            except Exception:
                span_price = WebDriverWait(driver, 7).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//span[@color='primary' and .//p[@display='inline']]"))
                )
                pass

            price = ''
            if span_discount:
                price = Price.fromstring("".join(span_discount[1].text))
            else:
                price = Price.fromstring("".join(span_price[1].text))
            # Clean and combine the price text
            #price_text = ''.join(price_text_parts).replace('€', '').replace(',', '.')

            # Extract the delivery fee
            delivery_elements = WebDriverWait(driver, 7).until(
                EC.presence_of_all_elements_located((By.XPATH, "//p[@text-decoration='underline' and @font-style='italic']"))
            )
            print(price,CMN,url)
            # Find the span element within the p element
            span_element = delivery_elements[1].find_element(By.XPATH, ".//span[@font-style='italic']")
            delivery_fee = Price.fromstring(span_element.text)

            item_data = CMN
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

            delivery_ranges = [(0.0,999999999.9,delivery_fee.amount_float)]
            price_ranges = [(minimum,9999999999,price)]

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
                        minimum=minimum, timestamp=datetime.now(pytz.timezone('CET'))
)

            session_prod.add(coin)
            session_prod.commit()


        except KeyError as e:
            logger.error(f"KeyError: {name}")

        except Exception as e:
            logger.error(f"An error occurred while scraping: {e}")
            traceback.print_exc()

