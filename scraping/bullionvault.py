import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver

from models.model import MetalPrice

def get(session,session_id):
    """Uses Selenium to click the currency button, then scrapes the 1 kg gold price in Euros."""

    driver = Driver(uc=True, headless=True)

    try:
        url = "https://or.bullionvault.fr/"
        driver.get(url)
        time.sleep(3)
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

            WebDriverWait(driver, 0.5).until(
                EC.visibility_of_element_located((By.ID, "buySILVERPrice"))
            )

            WebDriverWait(driver, 0.5).until(
                EC.visibility_of_element_located((By.ID, "sellSILVERPrice"))
            )

        except Exception as e:
            print(e)

        # Extract the price from the span
        buy_price_element = driver.find_element(By.CSS_SELECTOR, '#buyGOLDPrice span.EUR')
        buy_price_text = buy_price_element.text.strip()

        # Clean the text and convert to a float
        g_buy_price_eur = float(buy_price_text.split('€')[0].replace('\xa0', '').replace(',', '.').replace(' ',''))/1000.0  # Remove € and nbsp

        # Extract the price from the span
        sell_price_element = driver.find_element(By.CSS_SELECTOR, '#sellGOLDPrice span.EUR')
        sell_price_text = sell_price_element.text.strip()

        # Clean the text and convert to a float
        g_sell_price_eur = float(sell_price_text.split('€')[0].replace('\xa0', '').replace(',', '.').replace(' ',''))/1000.0  # Remove € and nbsp


        # Create GoldPrice object and add to session
        gold_price = MetalPrice(buy_price=g_buy_price_eur, sell_price=g_sell_price_eur, session_id=session_id, bullion_type='or')
        session.add(gold_price)
        session.commit()

        # Extract the price from the span
        buy_price_element = driver.find_element(By.CSS_SELECTOR, '#buySILVERPrice span.EUR')
        buy_price_text = buy_price_element.text.strip()

        # Clean the text and convert to a float
        s_buy_price_eur = float(buy_price_text.split('€')[0].replace('\xa0', '').replace(',', '.').replace(' ',''))/1000.0  # Remove € and nbsp

        # Extract the price from the span
        sell_price_element = driver.find_element(By.CSS_SELECTOR, '#sellSILVERPrice span.EUR')
        sell_price_text = sell_price_element.text.strip()

        # Clean the text and convert to a float
        s_sell_price_eur = float(sell_price_text.split('€')[0].replace('\xa0', '').replace(',', '.').replace(' ',''))/1000.0  # Remove € and nbsp

        # Create GoldPrice object and add to session
        silver_price = MetalPrice(buy_price=s_buy_price_eur, sell_price=s_sell_price_eur, session_id=session_id, bullion_type='ar')
        session.add(silver_price)
        session.commit()
        print(g_buy_price_eur,g_sell_price_eur,s_buy_price_eur,s_sell_price_eur)
        return g_buy_price_eur,g_sell_price_eur,s_buy_price_eur,s_sell_price_eur

    except Exception as e:
        print(f"Error scraping BullionVault: {e}",url)
        return None

    finally:
        driver.quit()