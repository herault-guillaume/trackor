from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights
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

def get_delivery_price(price):
    if price <= 1000.0:
        return 10.0
    elif price > 1000.0:
        return 25.0
# forfait

def get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver=None):


    urls =["https://www.joubert-change.fr/or-investissement/cours/prix.html",""]
    for url in urls :
        driver = Driver(uc=True, headless=True)

        driver.get(url)

        pricing_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))  # Use XPath for text-based search
        )
        items_tbody = pricing_table.find_element(By.TAG_NAME, "tbody")
        rows = items_tbody.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            try:
                if row['class'] in ['gold','silver'] :
                    continue
                values = row.find_elements(By.TAG_NAME,'td')

                coin_name = values[1].text
                price, minimum = values[6].text.split('min.')
                print(coin_name,price,minimum)
                quit()
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

                # Extract "Prix Net" (Net par Unité) for each row
                prix_net_values = []
                for row in rows:

                    # Assuming "Prix Net" is always the second column (index 1)
                    minimum = int(row.find_elements(By.TAG_NAME, "td")[0].text.replace('+',''))
                    price = Price.fromstring(row.find_elements(By.TAG_NAME, "td")[3].text)

                    print(price, CMN, url)
                    coin = Item(name=name,
                                prices=price.amount_float,
                                source=url,
                                buy_premiums=((price.amount_float + 0.0) - (buy_price * weights[CMN])) * 100.0 / (buy_price * weights[CMN]),
                                delivery_fee=0.0,
                                session_id=session_id,
                                bullion_type=CMN[:2],
                                quantity=quantity,
                                minimum=minimum, timestamp=datetime.now(pytz.timezone('CET'))
)

                    session_prod.add(coin)
                    session_prod.commit()

            except Exception:
                print(traceback.format_exc())
                pass
