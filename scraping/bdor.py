import time

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import Item, poids_pieces
from price_parser import Price
import traceback
import re

CMN = {
        "20 Fr Or Coq" : 'or - 20 francs fr coq marianne',
        "20 Fr Or Vreneli" : 'or - 20 francs sui vreneli croix',
        "20 Fr Or Génie" : 'or - 20 francs fr génie debout',
        "20 Fr Or Napoléon Tête Nue" : 'or - 20 francs fr napoléon empereur nue',
        "20 Fr Or Napoléon Lauré" : 'or - 20 francs fr napoléon empereur laurée',
        "10 Fr Or Coq" : "or - 10 francs fr coq marianne",
        "10 Fr Or Napoléon Tête Nue" : "or - 10 francs fr napoléon III",
        "10 Fr Or Napoléon Lauré" : "or - 10 francs fr napoléon III laurée",
        "10 Fr Or Vreneli" : "or - 10 francs sui vreneli croix",
        "20 Dollars Or St Gaudens" : "or - 20 dollars liberté st gaudens",
        "20 Dollars Or Liberty" : "or - 20 dollars liberté longacre",
        "50 Pesos Or" : "or - 50 pesos mex",
        "Krugerrand" : "or - 1 oz krugerrand",
        "10 Gulden Or" : "or - 10 florins wilhelmina",
        "20 Fr Or Italie" : "or - 20 lire umberto I",
        "20 Fr Or Autriche" : "or - 8 florins 20 francs franz joseph I",
        "20 Fr Or Belgique" : "or - 20 francs bel leopold I",
        "Souverain Or Elizabeth II" : "or - 1 souverain elizabeth II",
        "Demi Souverain Or" : 'or - 1/2 souverain georges V',
        "Souverain Or" : 'or - 1 souverain georges V',
        # Elizabeth II 2022 RARE
        # Demi Souverain Elizabeth II 2022
        #Charles III Or 2022 RARE
        "10 Dollars Or indien" : 'or - 10 dollars tête indien',
        "10 Dollars Liberty" : 'or - 10 dollars liberté',
        "5 Dollars Or Sioux" : 'or - 5 dollars tête indien',
        "5 Dollars Or Liberty" : 'or - 5 dollars liberté',
        "Maple Leaf Or" : 'or - 1 oz maple leaf',
        "20 Fr Or Confédération" : 'or - 20 francs sui confederatio',
        "20 Mark Or" : 'or - 20 mark wilhelm II',
        "20 Fr Or Tunisie" : 'or - 20 francs tunisie',
        "Philharmonique Or" : 'or - 1 oz philharmonique',
        "American Eagle Or" : 'or - 1 oz american eagle',
        "100 Frs Tête Nue" : 'or - 100 francs fr napoléon III tête nue',
        "50 Francs Tête Nue" : 'or - 50 francs fr napoléon III tête nue',
        "100 Frs Tête Laurée" : 'or - 100 francs fr napoléon III tête laurée',
        "50 Frs Tête Laurée" : "or - 50 francs fr napoléon III tête laurée",
        "100 Corona" : 'or - 100 couronnes françois joseph I',
        "4 Ducats" : 'or - 4 ducats',
        "20 Pesos Or" : "or - 20 pesos mex",
        "2,5 Dollars Or" : "or - 2.5 dollars tête indien",
        "5 Roubles" : "or - 5 roubles",
}

def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    driver = Driver(uc=True, headless=True)
    url = "https://www.bdor.fr/achat-or-en-ligne"
    print(url)

    delivery_ranges = [
        (0.0,1000.0,15.0),
        (1000.0,999999999999.0,0.0)
    ]

    try :
        driver.get(url)
        following_element = None
        # Locate the element
        # Find the div by data-idr using WebDriverWait for dynamic loading

        for id in ['100989','105846']:

            # on attend le chargement de l'ensemble des lignes à scrapper
            wait = WebDriverWait(driver, 10)  # Adjust timeout as needed
            div_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-idr='{id}']".format(id=id)))
            )
            trs_elements = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr.prixPalier"))
            )
            divs_produit = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "produitOrNom"))
            )

            #time.sleep(5)
            # Find all ligneTab divs within the div_element
            ligne_tab_divs = div_element.find_elements(By.CLASS_NAME, "ligneTab")

            for ligne_tab_div in ligne_tab_divs:
                # Find the specific tr element within each ligneTab div

                # Extract product name from the div with produitOrNom class
                product_name_div = ligne_tab_div.find_element(By.CLASS_NAME, "produitOrNom")
                product_name = product_name_div.text
                print(product_name)
                if not CMN.get(product_name,None):
                    continue

                item_data = CMN[product_name]

                # Find the div with class "colonne produitOr"
                produit_or_div = ligne_tab_div.find_element(By.CLASS_NAME, "produitOr")

                # Find the first <a> tag within it
                first_a_tag = produit_or_div.find_element(By.TAG_NAME, "a")

                # Extract the href attribute
                source = first_a_tag.get_attribute("href")

                price_ranges = []
                trs = ligne_tab_div.find_elements(By.CLASS_NAME, "prixPalier")

                len_price = len(trs)
                print(len_price)
                i = 0  # Skip the first qty div ("Vous achetez")
                for tr in trs[:len_price//2]:
                    tds = tr.find_elements(By.TAG_NAME, 'td')
                    tds = [td.get_attribute("innerHTML").replace('<span class="motarticles" style="display: none;"> articles</span>','') for td in tds]

                    match = re.search(r"(\d+)\s*\D+\s*(\d+)",tds[0])
                    if match:
                        min = int(match.group(1))
                        max = int(match.group(2))
                    else:
                        #print(tr)
                        min = int(re.search(r"\d+",tds[0]).group())
                        max = 9999999999.0

                    price = Price.fromstring(tds[1])
                    price_ranges.append([min, max, price]),

                minimum = 1
                quantity = 1

                if isinstance(item_data, tuple):
                    name = item_data[0]
                    quantity = item_data[1]
                    bullion_type = item_data[0][:2]
                else:
                    name = item_data
                    bullion_type = item_data[:2]

                if bullion_type == 'or':
                    buy_price = buy_price_gold
                else:
                    buy_price = buy_price_silver

                def price_between(value, ranges):
                    """
                    Returns the price per unit for a given quantity.
                    """

                    for min_qty, max_qty, price in ranges:
                        if min_qty <= value <= max_qty:
                            if isinstance(price, Price):
                                return price.amount_float
                            else:
                                return price
                print(price,name, url)
                coin = Item(name=name,
                            price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in price_ranges]),
                            buy_premiums=';'.join(
['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(1,minimum)] +
['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges)*i,delivery_ranges)/(quantity*i)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(minimum,151)]
                            ),
                            delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                            source=source,
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=quantity,
                            minimum=minimum)
                session.add(coin)
                session.commit()


    except Exception as e:
        print(e)
        print(traceback.format_exc())

