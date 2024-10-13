from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import Item

def get(session):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    url = "https://www.joubert-change.fr/or-investissement/cours/piece-or-78-20-francs-napoleon.html?"

    driver.get(url)

    # Locate the div by its data-url attribute (using XPath)
    small_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//small[contains(text(),'5')]"))
    )
    # Get the parent element of the <small> tag (the <td>)
    price_element = small_element.find_element(By.XPATH, "..")

    # Extract the price text from the parent element
    price_text = price_element.text.strip()

    # Clean the price text and convert to float
    price = float(price_text.replace('€', '').replace(',','.').replace('\nmin. 5',''))

    coin = Item(name="or - 20 francs coq marianne", buy=price, source='joubertchange')
    session.add(coin)
    session.commit()

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.",url)

