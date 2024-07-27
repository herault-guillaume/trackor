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
import gold
import achatoretargent
import changedelabourse
import changevivienne
import bdor
import orinvestissement
import lcdor
import oretchange
import goldunion
import merson
import goldforex
import orobel
import monlingot
import bullionbypost
import pieceor
import changerichelieu
import lmp
import goldavenue

session = Session()

# buy_price,sell_price = bullionvault.get(session)
# achatorargent.get(buy_price,sell_price,0,session)
# achatorargent.get(buy_price,sell_price,1,session)
# aucoffre.get(session)
# joubertchange.get(session)
# gold.get(session)
# achatoretargent.get(session)
# changedelabourse.get(session)
# changevivienne.get(session)
# bdor.get(session)
# orinvestissement.get(session)
# lcdor.get(session)
# oretchange.get(session)
# goldunion.get(session)
# merson.get(session)
# goldforex.get(session)
# orobel.get(session)
# monlingot.get(session)
# bullionbypost.get(session)
# pieceor.get(session)
# changerichelieu.get(session)
# lmp.get(session)
goldavenue.get(session)

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




