from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice
from price_parser import Price
import traceback

coin_name = {
    "10 Francs Français – Marianne Coq": '10 francs or coq marianne',
    #"MapleGram25 2021 (25 x 1g) Or  – Edition Limitée": 'Lingot or 25 g LBMA',
    #"50 Dollars Eagle 2022 (1Oz)": '1 oz american eagle',
    #"Queen’s Beast 2021 – 1 Oz (Edition Limitée)": 'souverain or elizabeth II',
    "20 Francs Napoléon": '20 francs or napoléon III',
    "20 Francs Marianne Coq": '20 francs or coq marianne',
    "20 Francs Suisse (Vrenelis)": '20 francs or vreneli croix suisse',
    "Krugerrand": '1 oz krugerrand',
    #"Krugerrand 1 Oz Or (2024)": '1 oz krugerrand',
    #"Swiss Bullion 1+ (1 Oz 999,9 ‰)": 'Lingot or 1 once LBMA',
    "Maple Leaf": '1 oz maple leaf',
    "Australian Nugget": '1 oz nugget / kangourou',
    "Louis Belge": '20 francs or union latine léopold II',
    "Souverain": 'souverain or elizabeth II',
    #"Souverain Or 2023 – Roi Charles": 'souverain or elizabeth II',
    "50 Pesos Mexique": '50 pesos or',
    "American Buffalo": '1 oz buffalo',
    "50 dollars eagle": '1 oz american eagle',
    "Demi-souverain": '1/2 souverain georges V',
    "4 Ducats": '4 ducats or',
    "20 Dollars Eagle (US)": '20 dollars or liberté',
    "50 ECU": '50 écus or charles quint',
    #"Chien Lunar 2018 1 once": 'Lingot or 1 once LBMA',
    "10 Francs Français": '10 francs or napoleon'
}

def get_delivery_price(price):
    """
    https://www.orobel.biz/shop/livraisons
    """
    if 1 <= price <= 49.99:
        return 15.0
    elif 50 <= price <= 4999.99:
        return 35.0
    elif 5000 <= price <= 9999.99:
        return 75.0
    elif 10000 <= price <= 14999.99:
        return 90.0
    elif 15000 <= price <= 29999.99:
        return 120.0
    elif 30000 <= price <= 39999.99:
        return 200.0
    elif 40000 <= price <= 44999.99:
        return 235.0
    else :
        return 300.0

def get_price_for(session, session_id):
    """
    Retrieves coin purchase prices from Orobel using Selenium.
    """

    url = "https://www.orobel.biz/catalogue/pieces-or"
    print(url)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Headless mode for efficiency

    # Initialize Selenium webdriver (replace with your preferred browser driver)
    driver = webdriver.Chrome(options=options)  # Or use Firefox, Edge, etc.


    try:
        driver.get(url)

        # Wait for the products to load (adjust the timeout as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "fusion-column-wrapper"))
        )

        # Try to find and click the "Load More Produits" button once
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fusion-load-more-button"))
            )
            load_more_button.click()

            # Wait for new products to load after clicking (adjust timeout if needed)
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "fusion-column-wrapper"))
            )

        except Exception as e:
            # If the button is not found or not clickable, it's okay - we only need to click it once
            pass

        # Find the product divs
        products_div = driver.find_elements(By.CLASS_NAME, "fusion-column-wrapper")

        for product in products_div:
            try:
                price_text = product.find_element(By.CLASS_NAME, 'woocommerce-Price-amount').text
                price = Price.fromstring(price_text)

                name_title = product.find_element(By.TAG_NAME, "h4")
                url = name_title.find_element(By.TAG_NAME, 'a').get_attribute('href')
                name = name_title.text.strip()

                print(name,price)

                # Check if the name is in your coin_name dictionary
                if name in coin_name:
                    coin = CoinPrice(
                        nom=coin_name[name],
                        j_achete=price.amount_float,
                        source=url,
                        frais_port=get_delivery_price(price.amount_float),
                        session_id=session_id
                    )
                    session.add(coin)
                    session.commit()

            except Exception as e:
                pass
                #print(traceback.format_exc())

    finally:
        driver.quit()  # Close the browser window