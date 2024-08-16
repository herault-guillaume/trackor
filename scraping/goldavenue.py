from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.model import CoinPrice
from price_parser import Price
import traceback

urls = {
    '1 oz philharmonique': 'https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pur-999-9-philharmonique-annees-mixtes',
    '20 francs or napoléon III': "https://www.goldavenue.com/fr/acheter/or/produit/20-francs-piece-d-or-napoleon-iii-avec-ou-sans-couronne-de-laurier",
    '10 francs or coq marianne': "https://www.goldavenue.com/fr/acheter/or/produit/piece-d-or-pur-900-0-20-francs-napoleon-coq-de-chaplain",
    '40 francs or napoléon empereur lauré': "https://www.goldavenue.com/fr/acheter/or/produit/piece-de-monnaie-d-or-pur-900-0-40-francs-napoleon-bonaparte-premier-consul-an-xi",
    '50 francs or napoléon III tête nue': "https://www.goldavenue.com/fr/acheter/or/produit/piece-de-monnaie-d-or-pur-900-0-50-francs-napoleon-iii-tete-nue-1855-a-paris",
    '100 francs or napoléon III tête laurée': "https://www.goldavenue.com/fr/acheter/or/produit/piece-de-monnaie-d-or-pur-900-0-100-francs-napoleon-iii-tete-lauree-1869-a",
    '20 francs or vreneli croix suisse': "https://www.goldavenue.com/fr/acheter/or/produit/piece-d-or-pur-900-0-vreneli-20-francs-suisse-helvetia-annees-mixtes",
    'souverain or victoria jubilee': "https://www.goldavenue.com/fr/acheter/or/produit/piece-souverain-or-victoria-or-pur-916-7",
    'souverain or edouart VII': "https://www.goldavenue.com/fr/acheter/or/produit/souverain-en-or-pur-916-7-roi-edouard-vii",
    'souverain or elizabeth II': "https://www.goldavenue.com/fr/acheter/or/produit/piece-d-or-pur-916-7-souverain-elizabeth-bu-annees-mixtes",
    '1 oz maple leaf': "https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pur-999-9-maple-leaf-annee-aleatoire",
    '1 oz krugerrand': "https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pur-916-7-krugerrand-annees-mixtes",
    '1 oz american eagle': "https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pur-916-7-american-eagle-bu-annees-mixtes",
    '1 oz nugget / kangourou': "https://www.goldavenue.com/fr/acheter/or/produit/1-once-piece-d-or-pure-999-9-perth-mint-kangourou-bu-mixed-years",
    '1/2 oz maple leaf': "https://www.goldavenue.com/fr/acheter/or/produit/1-2-once-piece-d-or-maple-leaf-4f8cd2d7-fb76-4169-8f34-ebc3539675f7",
    '1/4 oz maple leaf': "https://www.goldavenue.com/fr/acheter/or/produit/1-4-once-piece-d-or-maple-leaf-db8f368c-0fa2-4e01-99c3-dbd14e34d8f5",
    '1/10 oz maple leaf': "https://www.goldavenue.com/fr/acheter/or/produit/1-10-once-piece-d-or-pur-999-9-maple-leaf-bu-annees-mixtes",
    '1/2 oz krugerrand': "https://www.goldavenue.com/fr/acheter/or/produit/1-2-once-piece-d-or-krugerrand-08af2735-b4e0-4928-9c58-033e187fa5df",
    '1/4 oz krugerrand': "https://www.goldavenue.com/fr/acheter/or/produit/1-4-once-piece-d-or-krugerrand-2911fe96-82da-4a42-bed3-25a39c95a915",
    '1/10 oz krugerrand': "https://www.goldavenue.com/fr/acheter/or/produit/1-10-once-piece-d-or-pur-916-7-krugerrand-annees-mixtes",
    '1/2 oz american eagle':"https://www.goldavenue.com/fr/acheter/or/produit/1-2-once-piece-d-or-american-eagle-6bdd8b58-0191-4fe2-8968-64134a4b19cb",
    '1/4 oz american eagle': "https://www.goldavenue.com/fr/acheter/or/produit/1-4-once-piece-d-or-american-eagle-fb260cc5-f784-4831-bfdc-f477a0012208",
    '1/10 oz american eagle': "https://www.goldavenue.com/fr/acheter/or/produit/1-10-once-piece-d-or-pur-916-7-american-eagle-bu-annees-mixtes",
    '1/2 oz nugget / kangourou': "https://www.goldavenue.com/fr/acheter/or/produit/1-2-once-piece-d-or-kangaroo",
    '1/4 oz nugget / kangourou': "https://www.goldavenue.com/fr/acheter/or/produit/1-4-once-piece-d-or-kangaroo",
    '10 francs or vreneli croix suisse': "https://www.goldavenue.com/fr/acheter/or/produit/10-francs-piece-d-or-suisse-vreneli"
}



def get_price_delivery_for(session,session_id):
    # Set up headless Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Use headless mode
    # options.add_argument("--incognito")  # Use incognito mode
    driver = webdriver.Chrome(options=options)

    for coin_name, url in urls.items():
        try:
            driver.get(url)  # Load the page
            print(url)
            # Locate the price element by its unique combination of classes
            price_elements = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.sc-4c919c2a-0.eGPPLD p.sc-8fad5955-0.iqjCoA'))
            )
            price_element = price_elements[1]

            price_text_parts = [span.text.strip() for span in price_element.find_elements(By.TAG_NAME, 'span')]

            # Clean and combine the price text
            price_text = ''.join(price_text_parts).replace('€', '').replace(',', '.')

            # Extract the delivery fee
            delivery_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.sc-8fad5955-0.klSgsp'))
            )
            delivery_text = delivery_element.text.strip().split()[0]
            delivery_fee = float(delivery_text.replace('€', '').replace(',', '.').replace('--', ''))  # Assuming delivery cost is in €

            # Convert to float
            price = Price.fromstring(price_text)
            print(coin_name,price)
            coin = CoinPrice(nom=coin_name,
                             j_achete=price.amount_float,
                             source=url,
                             frais_port=delivery_fee,session_id=session_id)
            session.add(coin)
            session.commit()


        except Exception as e :
            print(traceback.format_exc())