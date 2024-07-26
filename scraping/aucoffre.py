from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice

mapping_db_names = {
    'Nom': 'nom',
    'AchatVous vendez': 'je_vend',
    'VenteVous achetez': 'j_achete',
    'Cotation française': 'cotation_francaise',
    'Prime achat': 'prime_achat_vendeur',
    'Prime vente': 'prime_vente_vendeur',
}

def get(session):
    """
    Scrapes the AuCOFFRE website to get the buy price of 20 Francs coins.
    It first locates the div containing a specific flag image,
    then extracts the price text from within that div.
    """
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome()
    url = "https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-1/produit"
    driver.get(url)
    print('test')

    # Locate the div by its data-url attribute (using XPath)
    xpath = "//div[contains(@data-url, '20f-marianne')]"
    target_div = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

    # Extract the price text from within the div
    price_element = target_div.find_element(By.CSS_SELECTOR, '.text-xlarge.text-bolder.m-0.text-nowrap')
    price_text = price_element.text.strip()

    # Clean the price text and convert to float
    price = float(price_text.replace('€', '').replace(',','.'))

    coin = CoinPrice(nom="20 francs or coq marianne", j_achete=price,source='aucoffre')
    session.add(coin)
    session.commit()

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.")

