from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice


def get(session):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    url = "https://www.changevivienne.com/or/pieces-d-or-d-investissement/20-francs-napoleon"

    driver.get(url)
    following_element = None
    # Locate the element
    td_elements = driver.find_elements(By.TAG_NAME, "td")
    for i, td in enumerate(td_elements):
        if td.text == "de 1 à 9":
            following_element = td_elements[i + 1]
            break

    # Clean the price text and convert to float
    price = float(following_element.text.replace('€', '').replace(',', '.').replace('  net',''))

    coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price, source='changevivienne',frais_port=10.0)
    session.add(coin)
    session.commit()

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.",url)

