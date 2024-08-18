from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver

from models.model import GoldPrice

def get(session):
    """Uses Selenium to click the currency button, then scrapes the 1 kg gold price in Euros."""

    driver = Driver(uc=True, headless=True)

    try:
        url = "https://or.bullionvault.fr/"
        print(url)
        driver.get(url)

        try:
            cookie_button = WebDriverWait(driver, 4).until(  # Adjust wait time as needed
                EC.element_to_be_clickable((By.XPATH, "//button[@onclick='webpageCookies.acceptAllCookies()']"))
            )
            cookie_button.click()

            # Locate and click the Euro button
            euro_button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='btn currency ' and text()='€']"))
            )

            euro_button.click()
            # Wait for the price to update
            WebDriverWait(driver, 0.5).until(
                EC.visibility_of_element_located((By.ID, "buyGOLDPrice"))
            )

            WebDriverWait(driver, 0.5).until(
                EC.visibility_of_element_located((By.ID, "sellGOLDPrice"))
            )

        except Exception as e:
            print(e)

        # Extract the price from the span
        buy_price_element = driver.find_element(By.CSS_SELECTOR, '#buyGOLDPrice span.EUR')
        buy_price_text = buy_price_element.text.strip()

        # Clean the text and convert to a float
        buy_price_eur = float(buy_price_text.split('€')[0].replace('\xa0', '').replace(',', '.').replace(' ',''))/1000.0  # Remove € and nbsp

        # Extract the price from the span
        sell_price_element = driver.find_element(By.CSS_SELECTOR, '#sellGOLDPrice span.EUR')
        sell_price_text = sell_price_element.text.strip()

        # Clean the text and convert to a float
        sell_price_eur = float(sell_price_text.split('€')[0].replace('\xa0', '').replace(',', '.').replace(' ',''))/1000.0  # Remove € and nbsp

        # Create GoldPrice object and add to session
        gold_price = GoldPrice(buy_price=buy_price_eur, sell_price=sell_price_eur)
        session.add(gold_price)
        session.commit()

        return buy_price_eur,sell_price_eur

    except Exception as e:
        print(f"Error scraping BullionVault: {e}",url)
        return None

    finally:
        driver.quit()