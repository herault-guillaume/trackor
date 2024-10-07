import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.model import CoinPrice, poids_pieces_or
from seleniumbase import Driver

from price_parser import Price
import traceback

urls = {
    "10 francs or fr": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/10-francs-notre-choix/",
    "20 francs or fr": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/20-francs-notre-choix/",
    "20 francs or fr napoléon empereur nue": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/20-francs-napoleon-tete-nue/",
    "20 francs or fr génie debout": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/20-francs-genie-3e-republique/",
    "20 francs or fr cérès": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/20-francs-ceres/",
    "40 francs or fr": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/40-francs-francais-en-or-notre-choix/",
    "100 francs or fr": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/100-francs-notre-choix/",
    "50 francs or fr napoléon III tête nue": "https://www.bullionbypost.fr/pieces-or/francs-francais-piece-or/1857-50-francs-francais-napoleon-iii-tte-nue-a/",
    "20 francs or sui vreneli croix": "https://www.bullionbypost.fr/pieces-or/francs-suisses/20-francs-suisse/",
    "20 francs or sui confederatio suisse": "https://www.bullionbypost.fr/pieces-or/francs-suisses/20-francs-suisse-tete-helvetia/",
    "20 francs or bel leopold I" : "https://www.bullionbypost.fr/pieces-or/pieces-belges/20-francs-belges-notre-choix/",
    "1 oz philharmonique": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-philharmonique-de-Vienne-notre-choix/",
    "1 oz maple leaf": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-maple-notre-choix/",
    "1 oz krugerrand": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-krugerrand-notre-choix-1-once-1/",
    "1 oz buffalo": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-buffalo-americaine-notre-choix/",
    "1 oz american eagle": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-eagle-americain-notre-choix/",
    "1 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-or/piece-ore-une-1-once/piece-or-1-once-kangourou-australien-notre-choix/",
    "1/2 oz krugerrand": "https://www.bullionbypost.fr/pieces-or/pieces-or-demi-once/krugerrand-or-demi-once-notre-choix/",
    "1/2 oz maple leaf": "https://www.bullionbypost.fr/pieces-or/pieces-or-demi-once/maple-leaf-en-or-demi-once-notre-choix/",
    "1/2 oz american eagle": "https://www.bullionbypost.fr/pieces-or/pieces-or-demi-once/eagle-americain-or-10-dollars/",
    "1/2 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-or/pieces-or-demi-once/kangourou-en-or-demi-once-notre-choix/",
    "1/4 oz krugerrand": "https://www.bullionbypost.fr/pieces-or/Pieces-or-quart-once/krugerrand-or-quart-once-notre-choix/",
    "1/4 oz maple leaf": "https://www.bullionbypost.fr/pieces-or/Pieces-or-quart-once/maple-canadienne-or-quart-once/",
    "1/4 oz american eagle": "https://www.bullionbypost.fr/pieces-or/Pieces-or-quart-once/eagle-or-un-quart-once-notre-choix-annees/",
    "1/4 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-or/Pieces-or-quart-once/kangourou-or-quart-once-notre-choix/",
    "1/10 oz maple leaf": "https://www.bullionbypost.fr/pieces-or/pieces-or-dixieme-once/canadian-maple-tenth-ounce-gold-coin/",
    "1/10 oz krugerrand": "https://www.bullionbypost.fr/pieces-or/pieces-or-dixieme-once/krugerrand-or-dixieme-once-notre-choix/",
    "1/10 oz american eagle": "https://www.bullionbypost.fr/pieces-or/pieces-or-dixieme-once/eagle-or-dixieme-once-notre-choix/",
    "1/10 oz nugget / kangourou": "https://www.bullionbypost.fr/pieces-or/pieces-or-dixieme-once/australian-gold-nugget-tenth-ounce/",
    "20 dollars or": "https://www.bullionbypost.fr/pieces-or/1-once-piece-or-eagle-americain/double-eagle-en-or-20-dollars-notre-choix/",
    "souverain or": "https://www.bullionbypost.fr/pieces-or/piece-or-souverain-entiere/piece-or-souverain-meilleure-offre-1/",
    "1/2 souverain or": "https://www.bullionbypost.fr/pieces-or/demi-souverains/demi-souverain-notre-choix/",
    "8 florins 20 francs or franz joseph I": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/20-Francs-8-Florins-Autriche-en-or/",
    "4 florins 10 francs 1892 refrappe": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/10-Francs-4-Florins-Autriche-en-or/",
    "10 couronnes or françois joseph I": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/10-couronnes-autriche-or/",
    "20 couronnes or françois joseph I": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/20-couronnes-autriche-or/",
    "100 couronnes or françois joseph I": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/100-coronas-or-notre-choix/",
    "4 ducats or": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/4-ducats-autriche-or/",
    "1 ducat or": "https://www.bullionbypost.fr/pieces-du-monde/pieces-autrichiennes/1-ducat-autriche-or/",
    "5 dollars or liberté": "https://www.bullionbypost.fr/pieces-du-monde/pieces-americaines/demi-eagle-americain-or-5-dollars-tete-liberte-/",
    "10 dollars or tete liberte": "https://www.bullionbypost.fr/pieces-du-monde/pieces-americaines/eagle-americain-or-10-dollars-tete-liberte/",
    "10 florins or wilhelmina": "https://www.bullionbypost.fr/pieces-du-monde/pieces-hollandaises/10-florins-neerlandais-notre-choix/",
    "20 mark or wilhelm II": "https://www.bullionbypost.fr/pieces-du-monde/pieces-allemandes/20-mark-allemand-meilleur-rapport-qualite-prix/",
    "20 lire or vittorio emanuele II": "https://www.bullionbypost.fr/pieces-du-monde/pieces-italiennes/20-lires-italiennes-or-emmanuel-II/",
    "50 pesos or": "https://www.bullionbypost.fr/pieces-du-monde/pieces-mexicaines/50-pesos-mexicains-or/",
    "10 pesos or": "https://www.bullionbypost.fr/pieces-du-monde/pieces-mexicaines/10-pesos-mexicains-en-or/",
    "5 pesos or": "https://www.bullionbypost.fr/pieces-du-monde/pieces-mexicaines/5-pesos-mexicains-en-or/",
}
def get_price_for(session,session_id,buy_price):
    print("https://www.bullionbypost.fr/")
    driver = Driver(uc=True, headless=True)

    #driver = webdriver.Chrome(options=options)
    for coin_name, url in urls.items():
        try:
            driver.get(url)  # Load the page
            time.sleep(random.randint(10,18))
            # Locate the price element by its text content
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//p[strong[text()='Prix: ']]"))  # Use XPath for text-based search
            )
            price_text = price_element.text.strip()
            price = Price.fromstring(price_text)

            print(price,coin_name,url)
            try :
                coin = CoinPrice(nom=coin_name,
                                 j_achete=price.amount_float,
                                 source=url,
                                 prime_achat_perso=((price.amount_float + 0.0) - (
                                             buy_price * poids_pieces_or[coin_name])) * 100.0 / (buy_price * poids_pieces_or[
                                                       coin_name]),

                                 frais_port=0.0,session_id=session_id,metal='g')
                session.add(coin)
                session.commit()
            except Exception as e:
                print(f"Failed to convert price text '{price_text}' to float", url)
                print(traceback.format_exc())
                pass

        except ValueError:
            print(f"Failed to convert price text '{price_text}' to float",url)
            print(traceback.format_exc())
            pass