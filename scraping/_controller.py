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
import abacor
import goldreserve
import shopcomptoirdelor

session = Session()

buy_price,sell_price = bullionvault.get(session)
achatorargent.get(buy_price,sell_price,0,session)
achatorargent.get(buy_price,sell_price,1,session)
aucoffre.get(session)
joubertchange.get(session)
gold.get(session)
achatoretargent.get(session)
changedelabourse.get(session)
changevivienne.get(session)
bdor.get(session)
orinvestissement.get(session)
lcdor.get(session)
oretchange.get(session)
goldunion.get(session)
merson.get(session)
goldforex.get(session)
orobel.get(session)
monlingot.get(session)
bullionbypost.get(session)
pieceor.get(session)
changerichelieu.get(session)
lmp.get(session)
goldavenue.get(session)
abacor.get(session)
goldreserve.get(session)
shopcomptoirdelor.get(session)







