from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.model import CoinPrice

def get_price_delivery_for(session):
    url = "https://www.goldavenue.com/fr/acheter/or/produit/piece-d-or-pur-900-0-20-francs-napoleon-coq-de-chaplain"

    # Set up headless Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Use headless mode
    # options.add_argument("--incognito")  # Use incognito mode

    with webdriver.Chrome(options=options) as driver:
        driver.get(url)  # Load the page

        try:
            # Locate the price element by its unique combination of classes
            price_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.sc-4c919c2a-0.eGPPLD p.sc-8fad5955-0.iqjCoA'))
            )
            price_element = price_elements[1]

            price_text_parts = [span.text.strip() for span in price_element.find_elements(By.TAG_NAME, 'span')]

            # Clean and combine the price text
            price_text = ''.join(price_text_parts).replace('€', '').replace(',', '.')

            # Extract the delivery fee
            delivery_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.sc-8fad5955-0.klSgsp'))
            )
            delivery_text = delivery_element.text.strip().split()[0]
            delivery_fee = float(delivery_text.replace('€', '').replace(',', '.').replace('--', ''))  # Assuming delivery cost is in €



            # Convert to float
            price = float(price_text)

            coin = CoinPrice(nom="20 francs or coq marianne",
                             j_achete=price,
                             source=url,
                             frais_port=delivery_fee)
            session.add(coin)
            session.commit()


        except ValueError:
            print(f"Failed to convert price text '{price_text}' to float",url)
            return None