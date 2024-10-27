import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from models.model import Item, poids_pieces
from seleniumbase import Driver

from price_parser import Price
import traceback

urls = {
    "or - 10 francs fr": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/10-francs-notre-choix/",
    "or - 20 francs fr": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/20-francs-notre-choix/",
    "or - 20 francs fr napoléon empereur nue": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/20-francs-napoleon-tete-nue/",
    "or - 20 francs fr génie debout": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/20-francs-genie-3e-republique/",
    "or - 20 francs fr cérès": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/20-francs-ceres/",
    "or - 40 francs fr": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/40-francs-francais-en-or-notre-choix/",
    "or - 100 francs fr": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/100-francs-notre-choix/",
    "or - 50 francs fr napoléon III tête nue": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/1857-50-francs-francais-napoleon-iii-tte-nue-a/",
    "or - 20 francs sui vreneli croix": "https://www.bullionbypost.fr/pieces-or/francs-suisses/20-francs-suisse/",
    "or - 20 francs sui confederatio": "https://www.bullionbypost.fr/pieces-or/francs-suisses/20-francs-suisse-tete-helvetia/",
    "or - 20 francs bel leopold I" : "https://www.bullionbypost.fr/pieces-or/pieces-belges/20-francs-belges-notre-choix/",
    "or - 1 oz philharmonique": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-philharmonique-de-Vienne-notre-choix/",
    "or - 1 oz maple leaf": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-maple-notre-choix/",
    "or - 1 oz krugerrand": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-krugerrand-notre-choix-1-once-1/",
    "or - 1 oz buffalo": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-buffalo-americaine-notre-choix/",
    "or - 1 oz american eagle": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-eagle-americain-notre-choix/",
    "or - 1 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-kangourou-australien-notre-choix/",
    "or - 1/2 oz krugerrand": "https://www.bullionbypost.fr/pieces-or/pieces-or-demi-once/krugerrand-or-demi-once-notre-choix/",
    "or - 1/2 oz maple leaf": "https://www.bullionbypost.fr/pieces-or/pieces-or-demi-once/maple-leaf-en-or-demi-once-notre-choix/",
    "or - 1/2 oz american eagle": "https://www.bullionbypost.fr/pieces-or/pieces-or-demi-once/eagle-americain-or-10-dollars/",
    "or - 1/2 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-or/pieces-or-demi-once/kangourou-en-or-demi-once-notre-choix/",
    "or - 1/4 oz krugerrand": "https://www.bullionbypost.fr/pieces-or/Pieces-or-quart-once/krugerrand-or-quart-once-notre-choix/",
    "or - 1/4 oz maple leaf": "https://www.bullionbypost.fr/pieces-or/Pieces-or-quart-once/maple-canadienne-or-quart-once/",
    "or - 1/4 oz american eagle": "https://www.bullionbypost.fr/pieces-or/Pieces-or-quart-once/eagle-or-un-quart-once-notre-choix-annees/",
    "or - 1/4 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-or/Pieces-or-quart-once/kangourou-or-quart-once-notre-choix/",
    "or - 1/10 oz maple leaf": "https://www.bullionbypost.fr/pieces-or/pieces-or-dixieme-once/canadian-maple-tenth-ounce-gold-coin/",
    "or - 1/10 oz krugerrand": "https://www.bullionbypost.fr/pieces-or/pieces-or-dixieme-once/krugerrand-or-dixieme-once-notre-choix/",
    "or - 1/10 oz american eagle": "https://www.bullionbypost.fr/pieces-or/pieces-or-dixieme-once/eagle-or-dixieme-once-notre-choix/",
    "or - 1/10 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-or/pieces-or-dixieme-once/australian-gold-nugget-tenth-ounce/",
    "or - 20 dollars": "https://www.bullionbypost.fr/pieces-or/1-once-piece-or-eagle-americain/double-eagle-en-or-20-dollars-notre-choix/",
    "or - 1 souverain": "https://www.bullionbypost.fr/pieces-or/piece-or-souverain-entiere/piece-or-souverain-meilleure-offre-1/",
    "or - 1/2 souverain": "https://www.bullionbypost.fr/pieces-or/demi-souverains/demi-souverain-notre-choix/",
    "or - 8 florins 20 francs franz joseph I": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/20-Francs-8-Florins-Autriche-en-or/",
    "or - 4 florins 10 francs 1892 refrappe": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/10-Francs-4-Florins-Autriche-en-or/",
    "or - 10 couronnes françois joseph I": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/10-couronnes-autriche-or/",
    "or - 20 couronnes": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/20-couronnes-autriche-or/",
    "or - 100 couronnes françois joseph I": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/100-coronas-or-notre-choix/",
    "or - 4 ducats": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/4-ducats-autriche-or/",
    "or - 1 ducat": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/1-ducat-autriche-or/",
    "or - 5 dollars liberté": "https://www.bullionbypost.fr/pieces-du-monde/pieces-americaines/demi-eagle-americain-or-5-dollars-tete-liberte-/",
    "or - 10 dollars liberté": "https://www.bullionbypost.fr/pieces-du-monde/pieces-americaines/eagle-americain-or-10-dollars-tete-liberte/",
    "or - 10 florins wilhelmina": "https://www.bullionbypost.fr/pieces-du-monde/pieces-hollandaises/10-florins-neerlandais-notre-choix/",
    "or - 20 mark wilhelm II": "https://www.bullionbypost.fr/pieces-du-monde/pieces-allemandes/20-mark-allemand-meilleur-rapport-qualite-prix/",
    "or - 20 lire vittorio emanuele II": "https://www.bullionbypost.fr/pieces-du-monde/pieces-italiennes/20-lires-italiennes-or-emmanuel-II/",
    "or - 50 pesos mex": "https://www.bullionbypost.fr/pieces-du-monde/pieces-mexicaines/50-pesos-mexicains-or/",
    "or - 10 pesos mex": "https://www.bullionbypost.fr/pieces-du-monde/pieces-mexicaines/10-pesos-mexicains-en-or/",

    "ar - 1 oz britannia": "https://www.bullionbypost.fr/pieces-argent/britannia-argent/piece-argent-britannia-notre-choix/",
    "ar - 1 oz maple leaf": "https://www.bullionbypost.fr/pieces-argent/maple-canadienne-argent/piece-maple-leaf-argent-1-once-notre-choix/",
    "ar - 1 oz philharmonique": "https://www.bullionbypost.fr/pieces-argent/1-once-piece-argent-philharmonique-vienne/",
    "ar - 1 oz silver eagle": "https://www.bullionbypost.fr/pieces-argent/eagle-americain-argent/piece-eagle-americain-argent-1-once-notre-choix/",
    "ar - 1 oz krugerrand": "https://www.bullionbypost.fr/pieces-argent/krugerrand/piece-krugerrand-argent-1-once-notre-choix/",
    "ar - 1 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-argent/kangourou-argent/kangourou-argent-1-once-2024/",
    "ar - 10 yuan panda 30g": "https://www.bullionbypost.fr/pieces-argent/panda-argent/piece-30g-panda-chinois-argent-notre-choix/",
    "ar - 1 oz": "https://www.bullionbypost.fr/pieces-argent/pieces-argent-1-once-notre-choix/piece-argent-1-once-meilleure-offreb/",
}
def get_price_for(session,session_id,buy_price_gold,buy_price_silver):
    print("https://www.bullionbypost.fr/")
    driver = Driver(uc=True, headless=True)

    delivery_ranges = [
        (0.0,99999999999.0,0.0)
    ]

    #driver = webdriver.Chrome(options=options)
    for CMN, url in urls.items():
        try:
            driver.get(url)  # Load the page
            time.sleep(random.randint(5,10))
            # Locate the price element by its text content
            # price_element = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//p[strong[text()='Prix: ']]"))  # Use XPath for text-based search
            # )
            pricing_table  = WebDriverWait(driver, 10).until(
                 EC.presence_of_all_elements_located((By.CLASS_NAME, "pricing-table"))  # Use XPath for text-based search
            )
            # Get all rows from the table body
            rows = pricing_table[1].find_elements(By.CSS_SELECTOR, "tbody tr")

            item_data = CMN

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


            price_ranges = []

            # Extract "Prix Net" (Net par Unité) for each row
            for i, row in enumerate(rows):

                # Assuming "Prix Net" is always the second column (index 1)
                min = int(row.find_elements(By.TAG_NAME, "td")[0].text.replace('+',''))
                if i == len(rows)-1 :
                    max = 9999999999
                else:
                    max = int(rows[i+1].find_elements(By.TAG_NAME, "td")[0].text.replace('+',''))-1

                try :
                    row.find_elements(By.TAG_NAME, "td")[3].find_element(By.TAG_NAME,'del')
                    price = Price.fromstring(row.find_elements(By.TAG_NAME, "td")[3].find_element(By.TAG_NAME,'span').text)
                except NoSuchElementException:
                    price = Price.fromstring(row.find_elements(By.TAG_NAME, "td")[3].text)

                price_ranges.append([min, max, price]),

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
            print(price,name,url)
            coin = Item(name=name,
                        price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].price_amount) for r in price_ranges]),
                        buy_premiums=';'.join(
['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(1,minimum)] +
['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges)*i,delivery_ranges)/(quantity*i)) - (buy_price*poids_pieces[name]))*100.0/(buy_price*poids_pieces[name])) for i in range(minimum,151)]
                        ),
                        delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                        source=url,
                        session_id=session_id,
                        bullion_type=bullion_type,
                        quantity=quantity,
                        minimum=minimum)

            session.add(coin)
            session.commit()

        except Exception:
            print(traceback.format_exc())
            pass

    driver.quit()