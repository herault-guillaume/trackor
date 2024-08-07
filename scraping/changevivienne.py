from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice


#https://www.changevivienne.com/livraison
def get_delivery_price(price):
    if 0 <= price <= 1000:
        return 15.0
    elif 1000.01 <= price <= 2500:
        return 20.0
    elif 2500.01 <= price <= 5000:
        return 34.0
    elif 5000.01 <= price <= 7500:
        return 50.0
    elif 7500.01 <= price <= 10000:
        return 56.0
    elif 10000.01 <= price <= 15000:
        return 65.0
    else:  # price > 15000.01
        return 0.0  # Frais de port offerts

def get_price_for(session):
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

    coin = CoinPrice(nom="20 francs or coq marianne",
                     j_achete=price,
                     source=url,
                     frais_port=get_delivery_price(price))
    session.add(coin)
    session.commit()

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.",url)

