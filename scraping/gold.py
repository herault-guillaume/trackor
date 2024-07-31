from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice


def get(session):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    url = "https://www.gold.fr/napoleon-or-20-francs-louis-or/"

    driver.get(url)

    # Locate the <span> element with class "amount"
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.amount'))
    )
    price_text = price_element.text.strip()

    # Clean the price text and convert to float
    price = float(price_text.replace('€', '').replace(',', '.').replace('\nmin. 5', ''))

    coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='https://www.gold.fr/napoleon-or-20-francs-louis-or/',frais_port=30.0)
    session.add(coin)
    session.commit()

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.",url)

