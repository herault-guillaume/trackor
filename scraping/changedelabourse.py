from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice


def get(session):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    url = "https://www.changedelabourse.com/or/pieces-d-or-d-investissement/napoleon-or-20-francs"

    driver.get(url)

    # Locate the element
    price_element = driver.find_element(By.ID, "our_price_display")

    # Clean the price text and convert to float
    price = float(price_element.text.replace('€', '').replace(',', '.'))

    coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='changedelabourse')
    session.add(coin)
    session.commit()

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.")

