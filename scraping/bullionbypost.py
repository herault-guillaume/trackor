from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.model import CoinPrice

def get_price_for(session,session_id):
    url = "https://www.bullionbypost.fr/francs-francais-piece-or/20-francs-francais/20-francs-notre-choix/"
    # Set up headless Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Use headless mode
    # options.add_argument("--incognito")  # Use incognito mode

    with webdriver.Chrome(options=options) as driver:
        driver.get(url)  # Load the page

        # Locate the price element by its text content
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[strong[text()='Prix: ']]"))  # Use XPath for text-based search
        )
        price_text = price_element.text.strip()

        try:
            price = float(price_text.replace('€', '').replace(',', '.').replace('Prix: à partir de ',''))

            coin = CoinPrice(nom="20 francs or coq marianne",
                             j_achete=price,
                             source=url,
                             frais_port=0.0,session_id=session_id)
            session.add(coin)
            session.commit()

            return price

        except ValueError:
            print(f"Failed to convert price text '{price_text}' to float",url)
            return None