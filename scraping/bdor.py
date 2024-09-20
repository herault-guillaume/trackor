import time

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice, poids_pieces_or
from price_parser import Price
import traceback

table_lookup = {
        "20 Fr Or Coq" : '20 francs or coq marianne',
        "20 Fr Or Vreneli" : '20 francs or vreneli croix suisse',
        "20 Fr Or Génie" : '20 francs or génie debout',
        "20 Fr Or Napoléon Tête Nue" : '20 francs or napoléon III',
        "20 Fr Or Napoléon Lauré" : '20 francs or napoléon empereur lauré',
        "10 Fr Or Coq" : "10 francs or coq marianne",
        "10 Fr Or Napoléon Tête Nue" : "10 francs or napoléon III",
        "10 Fr Or Napoléon Lauré" : "10 francs or napoléon III lauré",
        "10 Fr Or Vreneli" : "10 francs or vreneli croix suisse",
        "20 Dollars Or St Gaudens" : "20 dollars or tete indien",
        "20 Dollars Or Liberty" : "20 dollars or liberté",
        "50 Pesos Or" : "50 pesos or",
        "Krugerrand" : "1 oz krugerrand",
        "10 Gulden Or" : "10 florins or wilhelmina",
        "20 Fr Or Italie" : "20 lire or umberto I",
        "20 Fr Or Autriche" : "8 florins 20 francs or franz joseph I",
        "20 Fr Or Belgique" : "20 francs or leopold I",
        "Souverain Or Elizabeth II" : "souverain or elizabeth II",
        "Demi Souverain Or" : '1/2 souverain georges V',
        "Souverain Or" : 'souverain or georges V',
        # Elizabeth II 2022 RARE
        # Demi Souverain Elizabeth II 2022
        #Charles III Or 2022 RARE
        "10 Dollars Or indien" : '10 dollars or tête indien',
        "10 Dollars Liberty" : '10 dollars or liberté',
        "5 Dollars Or Sioux" : '5 dollars or tête indien',
        "5 Dollars Or Liberty" : '5 dollars or liberté',
        "Maple Leaf Or" : '1 oz maple leaf',
        "20 Fr Or Confédération" : '20 francs or helvetia suisse',
        "20 Mark Or" : '20 mark or wilhelm II',
        "20 Fr Or Tunisie" : '20 francs or tunisie',
        "Philharmonique Or" : '1 oz philharmonique',
        "American Eagle Or" : '1 oz american eagle',
        "100 Frs Tête Nue" : '100 francs or napoléon III tête nue',
        "50 Francs Tête Nue" : '50 francs or napoléon III tête nue',
        "100 Frs Tête Laurée" : '100 francs or napoléon III tête lauré',
        "50 Frs Tête Laurée" : "50 francs or napoléon III tête laurée",
        "100 Corona" : '100 couronnes or françois joseph I',
        "4 Ducats" : '4 ducats or',
        "20 Pesos Or" : "20 pesos or",
        "2,5 Dollars Or" : "2.5 dollars or tête indien",
        "5 Roubles" : "5 roubles or",
}

def get_delivery_price(price):
    #https://www.bdor.fr/achat-or-en-ligne/livraison-or
    if price < 1000.0:
        return 15.0
    else :
        return 0.0

def get_price_for(session,session_id,buy_price):
    driver = Driver(uc=True, headless=True)
    url = "https://www.bdor.fr/achat-or-en-ligne"
    print(url)
    try :
        driver.get(url)
        following_element = None
        # Locate the element
        # Find the div by data-idr using WebDriverWait for dynamic loading

        for id in ['100989','105846']:
            wait = WebDriverWait(driver, 10)  # Adjust timeout as needed
            div_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-idr='{id}']".format(id=id)))
            )
            trs_elements = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr.prixPalier[data-ordre='1']"))
            )
            divs_produit = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "produitOrNom"))
            )
            #time.sleep(5)
            # Find all ligneTab divs within the div_element
            ligne_tab_divs = div_element.find_elements(By.CLASS_NAME, "ligneTab")

            for ligne_tab_div in ligne_tab_divs:
                # Find the specific tr element within each ligneTab div
                tr_element = ligne_tab_div.find_elements(
                    By.CSS_SELECTOR, "tr.prixPalier[data-ordre='1']"
                )

                # Extract product name from the div with produitOrNom class
                product_name_div = ligne_tab_div.find_element(By.CLASS_NAME, "produitOrNom")
                product_name = product_name_div.text

                if not table_lookup.get(product_name,None):
                    continue

                product_name = table_lookup[product_name]

                # Find the div with class "colonne produitOr"
                produit_or_div = ligne_tab_div.find_element(By.CLASS_NAME, "colonne.produitOr")

                # Find the first <a> tag within it
                first_a_tag = produit_or_div.find_element(By.TAG_NAME, "a")

                # Extract the href attribute
                source = first_a_tag.get_attribute("href")
                price = Price.fromstring(tr_element[1].find_elements(By.TAG_NAME, 'td')[1].get_attribute('innerHTML'))
                print(product_name, price)
                coin = CoinPrice(nom=product_name,
                                 j_achete=price.amount_float,
                                 source=source,
                                 prime_achat_perso=((price.amount_float + get_delivery_price(price.amount_float)) - (
                                             buy_price * poids_pieces_or[product_name])) * 100.0 / (buy_price *
                                                   poids_pieces_or[product_name]),

                                 frais_port=get_delivery_price(price.amount_float),
                                 session_id=session_id)
                session.add(coin)
                session.commit()


    except Exception as e:
        print(e)
        print(traceback.format_exc())

