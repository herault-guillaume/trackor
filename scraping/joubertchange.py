from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice

def get(session):
    """
    Scrapes the AuCOFFRE website to get the buy price of 20 Francs coins.
    It first locates the div containing a specific flag image,
    then extracts the price text from within that div.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome()
    url = "https://www.joubert-change.fr/or-investissement/cours/piece-or-78-20-francs-napoleon.html?"

    driver.get(url)

    # Locate the div by its data-url attribute (using XPath)
    xpath = "//small[contains(text(), 'min. 5')]"
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//td[contains(text(), '€')][following-sibling::small[contains(text(), 'min')]]"))
    )
    print(price_element)
    price_text = price_element.text.strip()

    # Clean the price text and convert to float
    price = float(price_text.replace('€', '').replace(',','.'))

    coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price,source='joubertchange')
    session.add(coin)
    session.commit()

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.")

