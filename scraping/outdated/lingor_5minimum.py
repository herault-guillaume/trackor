from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import Item

def get(session):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    url = "https://www.lingor.fr/shop/20-francs-or-napoleon/"

    driver.get(url)

    # Locate the element
    span_element = driver.find_element(By.ID, "pa9")

    # Clean the price text and convert to float
    price = float(span_element.text.replace('€', '').replace(',', '.'))

    coin = Item(name="or - 20 francs coq marianne", prices=price, source='achatoretargent')
    session.add(coin)
    session.commit()

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.",url)

