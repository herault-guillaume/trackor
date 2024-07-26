import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, Session
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.model import Session

import bullionvault
import achatorargent
import aucoffre
import joubertchange

session = Session()

# buy_price,sell_price = bullionvault.get(session)
# achatorargent.get(buy_price,sell_price,0,session)
# achatorargent.get(buy_price,sell_price,1,session)
# aucoffre.get(session)
joubertchange.get(session)

# buy_gp,sell_gp = get_bullionvault_gold_price_euro()

# Exemple d'utilisation
# url = ''  # Remplacez par l'URL réelle
# lingots = get_achat_or_argent_gold_price_euro(url,buy_gp,sell_gp,0)
# monnaies = get_achat_or_argent_gold_price_euro(url,buy_gp,sell_gp,1)


# https://www.joubert-change.fr/or-investissement/cours/piece-or-78-20-francs-napoleon.html?gclid=CjwKCAjw74e1BhBnEiwAbqOAjNkbnvzC8-BIcBJuzrwKSVtyAi21wmf6EtddVuSQw0sgRzE0KLATjBoCFMoQAvD_BwE
# https://www.gold.fr/napoleon-or-20-francs-louis-or/
# https://www.achat-or-et-argent.fr/or/20-francs-marianne-coq/17
# https://www.lingor.fr/shop/20-francs-or-napoleon/
# https://www.changedelabourse.com/or/pieces-d-or-d-investissement
# https://www.changevivienne.com/or/pieces-d-or-d-investissement
# https://www.bdor.fr/achat-or-en-ligne/piece-d-or-20-francs-napoleon-laure
# https://www.bdor.fr/achat-or-en-ligne/piece-d-or-20-francs-coq-marianne
# https://or-investissement.fr/achat-piece-or-investissement/8-achat-piece-20-francs-marianne-coq.html
# https://www.oretchange.com/pieces-or/196-achat-20-francs-coq.html
# https://lcdor.fr/achat-or/pieces-dor/20-francs-or-coq/
# https://goldunion.fr/products/20-francs-coq
# https://www.merson.fr/fr/achat-or-investissement/91-20-francs-coq.html
# https://www.goldforex.be/fr/cours-de-lor-prix-pieces-lingot-cotation/napoleon-20-francs-france-229.html
# https://www.orobel.biz/produit/acheter-piece-or-20-francs-marianne-en-ligne-orobel
# https://monlingot.fr/or/achat-piece-or-20-francs-napoleon
# https://www.bullionbypost.fr/francs-francais-piece-or/20-francs-francais/20-francs-notre-choix/
# https://www.pieces-or.com/achat-or-argent/1-Napoleon-20-Francs.html
# https://www.changerichelieu.fr/or/pieces-d-or-d-investissement/20-francs-napoleon
# https://cramp.fr/product/20-francs-napoleon/
# https://www.lesmetauxprecieux.com/produit/20-francs-marianne-coq/
# https://www.goldavenue.com/fr/acheter/or/produit/piece-d-or-pur-900-0-20-francs-napoleon-coq-de-chaplain
# https://www.abacor.fr/product-category/achat-or/pieces-d-or/
# https://lcdor.fr/achat-or/pieces-dor/20-francs-or-coq/
# https://www.goldreserve.fr/boutique-goldreserve/?type=pieces
# https://www.oretchange.com/pieces-or/196-achat-20-francs-coq.html
# https://capornumismatique.com/produits/metaux/615
# https://www.shop-comptoirdelor.be/achat-or/pieces/20-francs-or-diverses-ann%C3%A9espays
# https://or-investissement.fr/achat-piece-or-investissement/8-achat-piece-20-francs-marianne-coq.html
# https://www.goldreserve.fr/produit/napoleon-20-francs-coq-marianne/
# https://www.bureaudechange.fr/or/achat-piece-or/20-francs-or-marianne/
# https://www.goldforex.be/fr/cours-de-lor-prix-pieces-lingot-cotation/napoleon-20-francs-france-229.html
#




