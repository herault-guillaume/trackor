import requests
from bs4 import BeautifulSoup
from scraping.dashboard.database import Item
from scraping.dashboard.pieces import weights
from seleniumbase import Driver
from price_parser import Price
import traceback
import logging
from datetime import datetime
import pytz
import re

# Get a logger instance
logger = logging.getLogger(__name__)

def get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver=None):
    if not driver:
        driver = Driver(uc=True, headless=True)
    print("https://stonexbullion.com/")
    logger.debug(f"Scraping started for https://stonexbullion.com/") # Example debug log

    urls = ['https://stonexbullion.com/fr/pieces-or/'] + ["https://stonexbullion.com/fr/pieces-or/?page={i}".format(i=i) for i in range(1,17)]

    CMN = {

        "4 Ducats | Or | Hors-circulation" : "or - 4 ducats",
        "1 oz Maple Leaf | Or | Endommagé" : "or - 1 oz maple leaf" ,
        "20 Francs Francais Cérès 2e République | Or | 1848-1852" : "or - 20 francs fr cérès",
        "100 Schilling Autrichien | Or | 1925-1934" :  "",
        "20 Mark | Ville Hanséatique Libre de Hambourg | Or | 1875-1913" : "or - 20 mark hambourg" ,
        "1 oz Cook Island Pièce Armillaire" : "or - 1 oz"  ,
        "100 Pesos Chilien Liberty | Or | 1895-1980" : "or - 100 pesos liberté chili",
        "20 Kroner Christian IX Danemark | Or | 1863-1906" : "" ,
        "20 Kroner Frederik VIII Danemark | Or | 1908-1912" : "" ,
        "1 oz Angel Isle of Man | Or | diverses années" : "or - 1 oz"  ,
        "1/2 oz Britannia | Or | plusieurs années" : "or - 1/2 oz britannia",
        "1/2 oz Kangourou | Or | Plusieurs Années" : "or - 1/2 oz kangourou" ,
        "1 oz Britannia | Or | plusieurs années 999.9" : "or - 1 oz britannia",
        "20 Francs Suisses Helvetica | Or | 1883-1896" : "or - 20 francs sui"  ,
        "Souverain William IV | Or | 1830-1837" : ""  ,
        "20 Drachme Grecque | Or | plusieurs années" : ""  ,
        "20 Kroner Christian X Danemark | Or | 1913-1917" : "" ,
        "10 Florins Néerlandais Willem III | Or | 1875-1889" : "or - 10 florins willem III" ,
        "50 Pesos Mexicains Centenario | Or | 1821-1947": "or - 50 pesos mex",
        "1 oz Krugerrand | Or | plusieurs années": "or - 1 oz krugerrand",
        "1 oz Bitcoin Or": "or - 1 oz",  # Assuming this is a 1 oz gold coin
        "Souverain Elisabeth II | Pièce d'or | 1957-2021": "or - 1 souverain elizabeth II",
        "Souverain Victoria voilée | Or | 1893-1901": "or - 1 souverain victoria voilée",
        "2 Rand Sud-Africaine | Or | 1961-1983": "or - 2 rand sud-africains",
        "1 Ducat | Or | Plusieurs Années": "or - 1 ducat",
        "Souverain George V Pièce d'or | 1911-1932": "or - 1 souverain georges V",
        "1 oz Maple Leaf | Or | Plusieurs Années": "or - 1 oz maple leaf",
        "20 Francs Suisses Vreneli | Or | 1897-1949": "or - 20 francs sui vreneli croix",
        "Souverain Edouard VII | Or | 1902-1910": "or - 1 souverain edouart VII",
        "20 Lires Italiennes Umberto I | Or | 1879-1897": "or - 20 lire umberto I",
        "10 Rouble Cervonec | Or | 1923-1982": "or - 10 roubles chervonetz",
        "20 Francs Napoléon III | Or | Plusieurs Années": "or - 20 francs fr napoléon III",
        "1 Rand Sud-Africaine | Or | 1961-1983": "or - 1 rand sud-africains",
        "50 Pesos Mexicains Centenario | Or | 1821-1947": "or - 50 pesos mex",
        "1 oz Krugerrand | Or | plusieurs années": "or - 1 oz krugerrand",
        "1 oz Bitcoin Or": "or - 1 oz",  # Assuming this is a 1 oz gold coin
        "Souverain Elisabeth II | Pièce d'or | 1957-2021": "or - 1 souverain elizabeth II",
        "Souverain Victoria voilée | Or | 1893-1901": "or - 1 souverain victoria voilée",
        "2 Rand Sud-Africaine | Or | 1961-1983": "or - 2 rand sud-africains",
        "1 Ducat | Or | Plusieurs Années": "or - 1 ducat",
        "Souverain George V Pièce d'or | 1911-1932": "or - 1 souverain georges V",
        "1 oz Maple Leaf | Or | Plusieurs Années": "or - 1 oz maple leaf",
        "20 Francs Suisses Vreneli | Or | 1897-1949": "or - 20 francs sui vreneli croix",
        "Souverain Edouard VII | Or | 1902-1910": "or - 1 souverain edouart VII",
        "20 Lires Italiennes Umberto I | Or | 1879-1897": "or - 20 lire umberto I",
        "10 Rouble Cervonec | Or | 1923-1982": "or - 10 roubles chervonetz",
        "20 Francs Napoléon III | Or | Plusieurs Années": "or - 20 francs fr napoléon III",
        "1 Rand Sud-Africaine | Or | 1961-1983": "or - 1 rand sud-africains",
        "4 Ducats | Or | Hors-circulation": "or - 4 ducats",
        "20 Lire Vittorio Emanuele II | Or | 1861-1878": "or - 20 lire vittorio emanuele II",
        "1 oz Maple Leaf | Or | Endommagé": "or - 1 oz maple leaf",  # Assuming the weight is the same
        "20 Francs Francais Cérès 2e République | Or | 1848-1852": "or - 20 francs fr cérès",
        "Souverain Victoria Jubilée | Or | 1887-1893": "or - 1 souverain victoria jubilee",
        "Souverain Victoria Jeune | Or | 1838-1887": "or - 1 souverain victoria jeune",
        "100 Couronnes François-Joseph Ier Autriche | Or": "or - 100 couronnes françois joseph I",
        "20 Mark Kaiser Wilhelm II Prusse | Or | 1888-1913": "or - 20 mark wilhelm II",
        "20 Franc Leopold II Belgique | Or | 1876-1882": "or - 20 francs bel leopold II",
        "10 Francs Suisses demi Vreneli | Or | 1911-1922": "or - 10 francs sui vreneli croix",
        "20 Lires Italiennes Carl Albert | Or | diverses années": "or - 20 lire carl albert",
        "1 oz Philharmonique de Vienne | Or | Plusieurs Années": "or - 1 oz philharmonique",
        "100 Schilling Autrichien | Or | 1925-1934": "or - 100 schilling autrichien",  # You might need to add this to 'weights'
        "8 Florin 20 Francs | Or | nouvelle édition": "or - 8 florins 20 francs franz joseph I",
        "20 Mark | Ville Hanséatique Libre de Hambourg | Or | 1875-1913": "or - 20 mark hambourg",
        "1 Ducat | Or | Hors-circulation": "or - 1 ducat",  # Assuming the weight is the same
        '20 Dollar Double Eagle "Saint-Gaudens" | Or | 1907-1933': "or - 20 dollars liberté st gaudens",
        '10 Dollar Eagle "Indian Head" | Gold | 1908-1933': "or - 10 dollars tête indien",
        "1 oz Cook Island Pièce Armillaire": "or - 1 oz",  # Assuming this is a 1 oz gold coin
        "10 Florins Néerlandais Wilhelmina | Or | 1892-1933": "or - 10 florins wilhelmina",
        '20 Dollar Double Eagle "Liberty Head" | Or | 1850-1907': "or - 20 dollars liberté longacre",
        '10 Dollar Eagle "Liberty Head" | Or | 1866-1907"': "or - 10 dollars liberté",
        "4 Florin 10 Francs | Or | nouvelle édition": "or - 4 florins 10 francs 1892 refrappe",
        "100 Pesos Chilien Liberty | Or | 1895-1980": "or - 100 pesos liberté chili",
        "20 Kroner Christian IX Danemark | Or | 1863-1906": "or - 20 kroner christian IX",  # You might need to add this to 'weights'
        "20 Kroner Frederik VIII Danemark | Or | 1908-1912": "or - 20 kroner frederik VIII",  # You might need to add this to 'weights'
        "1 oz Angel Isle of Man | Or | diverses années": "or - 1 oz",  # Assuming this is a 1 oz gold coin
        "20 Francs Tunisiens | Or | plusieurs années": "or - 20 francs tunisie",
        "1 oz Philharmonique de Vienne | Or | Plusieurs Années | EUR": "or - 1 oz philharmonique",
        "20 Franc Leopold I Belgique | Or | 1831-1865": "or - 20 francs bel leopold I",
        "50 Pesos Chilien Liberty | Or | 1926-1980": "or - 50 pesos liberté chili",
        "20 French Franc Marianne Coq | Or | 1899-1914": "or - 20 francs fr coq marianne",
        "1 oz Panda Chinois | Or | plusieurs années": "or - 1 oz panda",
        "1 oz Nugget Kangourou | Or | Plusieurs Années": "or - 1 oz nugget / kangourou",
        "20 Francs Francais Génie 3e République | Or | 1871-1898": "or - 20 francs fr génie debout",
        "1/2 oz Britannia | Or | plusieurs années": "or - 1/2 oz britannia",
        "4 Ducats | Or | Plusieurs Années": "or - 4 ducats",
        "1/2 oz Kangourou | Or | Plusieurs Années": "or - 1/2 oz kangourou",
        "1 oz Britannia | Or | plusieurs années 999.9": "or - 1 oz britannia",
        "10 French Franc Marianne Coq | Or | 1899-1914": "or - 10 francs fr coq marianne",
        "1 oz American Buffalo | Or | plusieurs années": "or - 1 oz buffalo",
        "20 Francs Suisses Helvetica | Or | 1883-1896": "or - 20 francs sui",  # You might need to be more specific in 'weights'
        "20 Francs Suisses Vreneli | 1897-1949 | 2ème choix": "or - 20 francs sui vreneli croix",  # Assuming the weight is the same
        "Souverain | Or | meilleur prix": "or - 1 souverain",  # Assuming this is a standard sovereign
        "20 Pesos Mexicains Azteca | Or | 1917-1959": "or - 20 pesos mex",
        '2.5 Dollar Quarter Eagle "Indian Head" | Or | 1908-1929': "or - 2.5 dollars tête indien",
        "1 oz Libertad Mexicain | Or | plusieurs années": "or - 1 oz libertad",
        '2.5 Dollar Quarter Eagle "Liberty Head" | Or | 1840-1907': "or - 2.5 dollars liberté",
        "40 Francs Francais Napoleon I couronné | Or | 1806-1812": "or - 40 francs fr napoléon empereur non laurée",
        "Souverain William IV | Or | 1830-1837": "or - 1 souverain william IV",  # You might need to add this to 'weights'
        "20 Drachme Grecque | Or | plusieurs années": "or - 20 drachmes grecques",  # You might need to add this to 'weights'
        "20 Kroner Christian X Danemark | Or | 1913-1917": "or - 20 kroner christian X",  # You might need to add this to 'weights'
        "10 Florins Néerlandais Willem III | Or | 1875-1889": "or - 10 florins willem III",
        "£2 Souverain (1887) | Or | meilleur prix": "or - 2 souverain",  # Assuming this is a standard sovereign
        "20 Francs Louis XVIII | 2nd Choix | 1814-1824": "or - 20 francs fr louis XVIII buste nu",
        "Souverain Victoria Jeune avec blason | Or | 1871-1887": "or - 1 souverain victoria jeune armoiries",
        "1/4 oz Nugget Kangourou | Or | Plusieurs Années": "or - 1/4 oz nugget / kangourou",
        "1/4 oz Panda Chinois | Or | plusieurs années": "or - 1/4 oz panda",  # You might need to add this to 'weights'
        "20 Mark Kaiser Wilhelm I Prusse | Or | 1871-1888": "or - 20 mark wilhelm I",
        "1/2 oz Krugerrand | Or | plusieurs années": "or - 1/2 oz krugerrand",
        "20 Francs Français Napoléon Bonaparte | Or | 1809-1814": "or - 20 francs fr napoléon empereur",
        "Souverain | Or | Endommagé": "or - 1 souverain",  # Assuming the weight is the same
        "25 x 1g MapleGram25 d'Or": "or - 25 x 1g maplegram25",  # You might need to add this to 'weights'
        "50 Soles Péruviens | Or | années mixtes": "or - 50 soles péruviens",  # You might need to add this to 'weights'
        "1/10 oz Nugget Kangourou | Or | Plusieurs Années": "or - 1/10 oz nugget / kangourou",
        "100 Couronnes François-Joseph Ier Hongrie | Or | nouvellement forgé": "or - 100 couronnes hongrie",
        "1 oz Krugerrand | Or | 2me choix | plusieurs années": "or - 1 oz krugerrand",  # Assuming the weight is the same
        "20 Couronnes Franz-Joseph I Autriche | Or | 1915 nouvelle édition": "or - 20 couronnes françois joseph I",
        "Souverain Monnaie Canadien | Or | 1908-1919": "or - 1 souverain",  # Assuming this is a standard sovereign
        "10 Florins Néerlandais Willem III ou Wilhelmina | Or | plusieurs années": "or - 10 florins",  # You might need to be more specific in 'weights'
        "20 Pesos Chilien Liberty | Or | 1895-1980": "or - 20 pesos chili",
        "1/2 oz Panda Chinois | Or | plusieurs années": "or - 1/2 oz panda",
        "20 Mark Roi Ludwig II Bavière | Or | 1872-1886": "or - 20 mark ludwig II",
        "20 Mark Kaiser Wilhelm II Uniforme Prusse | Or | 1913-1914": "or - 20 mark wilhelm II uniforme",
        "20 Mark | Roi Wilhelm II Wurtemberg | Or | 1891-1918": "or - 20 mark wilhelm II württemberg",
        "10 Mark Roi Ludwig II Bavière | Or | 1874-1886": "or - 10 mark ludwig II",  # You might need to add this to 'weights'
        "10 Mark | Empereur Wilhelm I Prusse | Gold | 1873-1888": "or - 10 mark wilhelm I",
        "1 oz Maple Leaf | Or | 2ème choix | plusieurs années": "or - 1 oz maple leaf",  # Assuming the weight is the same
        "1/4 oz Britannia | Or | plusieurs années": "or - 1/4 oz britannia",
        '5 Dollar Half Eagle "Indian Head" | Or | 1908-1929': "or - 5 dollars tête indien",
        "100 French Francs - diverse": "or - 100 francs fr",  # You might need to be more specific in 'weights'
        "20 Francs Napoléon III tête laurée | Or | 1861-1870": "or - 20 francs fr napoléon III tête laurée",
        "5 Francs Napoleon III | Or | 1854-1869": "or - 5 francs fr napoléon III",
        "5 Pesos Mexicains Hidalgo | Or | 1905-1955": "or - 5 pesos mex",
        "£5 Souverain | Or | meilleur prix": "or - 5 livres souverain",  # You might need to add this to 'weights'
        "1/4 oz Nugget Kangourou | Or | Plusieurs Années": "or - 1/4 oz nugget / kangourou",
        "1/2 oz Philharmonique de Vienne | Or | Diverses Années | EUR": "or - 1/2 oz philharmonique",
        "1 oz Pièce d'Or | endommagé": "or - 1 oz",  # Assuming this is a 1 oz gold coin
        "1/2 oz Philharmonique de Vienne | Or | Diverses Années": "or - 1/2 oz philharmonique",
        "100 Piastres Turques | Or | diverses années": "or - 100 piastres turc",
        "1/10 oz Philharmonique de Vienne | Or | Plusieurs Années" : "or - 1/10 oz philharmonique",
        "10 Soles Péruviens | Or | années mixtes" : "or - 10 soles péruviens",  # No matching key in weights
        "10 Pesos Cubain | Or | 1902-1916" : "or - ", # No matching key in weights
        "1 oz Libertad Mexicain pièce d'or (1981)" : "or - 1 oz",
        "1 oz Britannia Or (2ème choix)" : "or - 1 oz britannia",
        "20 Francs Charles III Monaco | Or | 1878 - 1879" : "or - 20 francs fr",
        "3g Panda Chinois | Or | plusieurs années" : "", # No matching key in weights (3g is not a standard unit in the weights dict)
        "1/10 oz Maple Leaf | Or | plusieurs années" : "or - 1/10 oz maple leaf",
        "1/10 oz Krugerrand | Or | plusieurs années" : "or - 1/10 oz krugerrand",
        "10 Couronnes Franz-Joseph I Autriche | Or | 1892-1916" : "or - 10 couronnes françois joseph I",
        "100 Francs Tunisiens | Or | 1930-1956" : "or - 100 francs tunisie",
        "10 Mark Roi Karl Wurttemberg | Or | 1864-1891" : "or - 10 mark wilhelm I", # Assuming this is similar to wilhelm I
        "25 Schilling autrichien | Or | 1926-1938" : "", # No matching key in weights
        "10 Francs Tunisiens | Or | plusieurs années" : "or - 10 francs tunisie",
        "1/2 oz Libertad Mexicain | Or | plusieurs années" : "or - 1/2 oz",
        "1/4 oz Libertad Mexicain | Or | plusieurs années" : "or - 1/4 oz",
        "1/10 oz Britannia | Or | plusieurs années" : "or - 1/10 oz britannia",
        '5 Dollar Half Eagle "Liberty Head" | Or | 1795-1929' : "or - 5 dollars liberté",
        "1/10 oz Panda Chinois | Or | plusieurs années" : "or - 1/10 oz panda",
        "20 Mark Grand-Duc Friedrich I Baden | Or | 1872-1895" : "or - 20 mark Friedrich I (Baden)",
        "1/10 oz Libertad Mexicain | Or | plusieurs années" : "or - 1/10 oz",
        "20 Mark Grand-Duc Ernst Ludwig Hesse-Darmstadt | Or | 1890-1915" : "or - 20 mark", # Assuming this is a generic 20 mark
        "20 Mark Roi Albert I Saxe | Or | 1873-1902" : "or - 20 mark", # Assuming this is a generic 20 mark
        "1 oz American Eagle | Or | Plusieurs Années" : "or - 1 oz american eagle",
        "4 Forint 10 Francs Hongrie | Or | 1870 - 1892" : "or - 4 forint 10 Francs hongrie", # No exact match, but could potentially be "or - 4 florins 10 francs 1892 refrappe" if it's a refrappe
        "10 Mark | Hambourg | 1873-1913" : "or - 10 mark hambourg", # Assuming this is similar to the 20 mark Hamburg
        "10 Mark Empereur Wilhelm II Prusse | Or | 1889-1913" : "or - 10 mark wilhelm II",
        "1/4 oz Krugerrand | Or | plusieurs années" : "or - 1/4 oz krugerrand",
        "1 Dollar Grande Princesse Indienne | Or | 1856-1889" : "or - 1 dollar tête indien", # Assuming "Grande Princesse Indienne" refers to the Indian Head
        "20 Francs Louis XVIII | Or | 1814-1824" : "or - 20 francs fr louis XVIII buste nu", # Assuming "buste nu" based on the year range
        "20 Markkaa Finlande | Or | 1860-1913" : "or - 20 markkaa finlande", # No matching key in weights
        "Pièce d'or 10 Francs | Napoleon III tête laurée | Or |1854-1869" : "or - 10 francs fr napoléon III laurée",
        "10 Mark d'or Allemand | Roi Otto | Bavière | 1886-1913" : "or - 10 mark wilhelm I", # Assuming this is similar to wilhelm I
        "10 Mark Roi Albert I Saxe | Or | 1874-1888 et 1891-1902" : "or - 10 mark wilhelm I", # Assuming this is similar to wilhelm I
        "10 Mark Grand-Duc Friedrich I Baden | Or | 1872-1901" : "or - 10 mark wilhelm I", # Assuming this is similar to wilhelm I
        "20 Mark | Grand-Duc Friedrich II Baden | Or | 1907-1918" : "or - 20 mark Friedrich I (Baden)", # Assuming this is similar to Friedrich I
        "10 Pesos Mexicains Hidalgo | Or | 1905-1959" : "or - 10 pesos mex",
        "2.5 Pesos Mexicains Hidalgo | Or | 1918-1948" : "or - 2.5 pesos mex",
        "2 Pesos Mexicains Hidalgo | Or | 1919-1948" : "or - 2 pesos mex",
        "5 Florins Néerlandais Wilhelmina | Or | 1892-1933" : "or - 5 florins wilhelmina",
        "1/2 oz American Eagle | Or | diverses années" : "or - 1/2 oz american eagle",
        "1/4 oz American Eagle | Or | plusieurs années" : "or - 1/4 oz american eagle",
        "Demi Souverain Edouard VII Or | Mix d'années" : "or - 1/2 souverain edouart VII",
        "Demi Souverain Victoria | Or | Mix d'années" : "or - 1/2 souverain victoria",
        "Demi Souverain George V | Or | Mix d'années" : "or - 1/2 souverain georges V",
        "1/4 oz Philharmonique de Vienne | Or | Diverses Années | EUR" : "or - 1/4 oz philharmonique",
        "Pièce d'or 10 Francs | Napoléon III | Or | 1854-1869" : "or - 10 francs fr napoléon III",
        "10 Couronnes Hongrois | Or | 1892-1915" : "or - 10 couronnes hongrie",
        "20 Couronnes Hongrois | Or | 1892-1915" : "or - 20 couronnes hongrie",
        "1/4 oz Philharmonique de Vienne | Or | Diverses Années" : "or - 1/4 oz philharmonique",
        "20 Francs Louis Philippe I | Or | 1830-1848" : "or - 20 francs fr louis philippe laurée", # Assuming "laurée" based on the year range
        "100 Soles Péruviens | Or | années mixtes" : "or - 100 soles péruviens", # No matching key in weights
        "20 Francs Albert I Belgique | Or | 1909-1934" : "or - 20 francs bel albert I",
        '15.04g Eagle "Coronet Head" | Or | 1866-1907' : "or - 10 dollars tête indien", # Assuming this is similar to the 10 dollar Indian Head
        "Demi Souverain Victoria Jubilée Pièce d'or | 1887-1893" : "or - 1/2 souverain victoria jubilee arm.",
        "Demi Souverain Victoria Jeune Pièce d'or | 1837-1887" : "or - 1/2 souverain victoria jeune",
        "1 oz Dragon Rectangulaire | Or | Plusieurs Années" : "or - 1 oz", # Assuming this is a generic 1 oz gold coin
        "20 Mark | Kaiser Friedrich III Prusse | Or | 1888" : "or - 20 mark", # Assuming this is a generic 20 mark
        "10 Dollar George V Canada | Or | 1912-1914" : "or - 100 dollars canadien", # Assuming this is similar to the 100 dollar Canadian coin
        "1/20 oz Panda Chinois | Or | plusieurs années" : "or - 1/20 oz",
        "20 Francs Francais Génie 3e République | Or | 1871-1898 | 2ème Choix" : "or - 20 francs fr génie debout",
        "1/10 oz American Eagle | Or | plusieurs années" : "or - 1/10 oz american eagle",
        "1/20 oz Maple Leaf | Or | plusieurs années" : "or - 1/20 oz maple leaf",
        "20 Mark Roi Johann Saxe | Or | 1872-1873" : "or - 20 mark", # Assuming this is a generic 20 mark
        "20 Mark | Roi Friedrich August III. Saxe | Or | 1904-1918" : "or - 20 mark", # Assuming this is a generic 20 mark
        "20 Mark Roi Otto Bavière | Or |1886-1916" : "or - 20 mark", # Assuming this is a generic 20 mark
        "1/20 oz Nugget Kangourou | Or | Plusieurs Années" : "or - 1/20 oz nugget / kangourou",
        "5 Pesos Colombia Simon Bolivar Pièce d'Or | 1919-1930" : "", # No matching key in weights
        "8 Forint 20 Francs Hongrie | Or | 1870 - 1892" : "or - 8 forint 20 Francs hongrie", # No exact match, but could potentially be "or - 8 florins 20 francs franz joseph I" if it's from that period
        "1/4 oz Maple Leaf | Or | Plusieurs Années" : "or - 1/4 oz maple leaf"

    }


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    delivery_ranges = [
        (1,500,2.95),
        (500,1000,3.95),
        (1000,1500,4.95),
        (1500,2500,5.95)] + [(2500.0 + (i * 500), 2500.0 + ((i+1) * 500), 5.95 + (1.0 * (i+1))) for i,v in enumerate(range(2500,25000,500))]

    already_added = set()
    for url in urls :
        try:
            print(url)

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            products = soup.find_all('div',class_='product-item-in')

            for p in products:
                try :

                    if p.find('small',class_='text-danger',text='Épuisé'):
                        continue
                    if p.find('div',class_='product_thumb_out_stock'):
                        continue
                    product_name = p.find('span',class_="product-item-name text-start").text
                    print(product_name)
                    source = p.find('a')['href']
                    # Use a more specific CSS selector to target the price element
                    price_elements = p.find('div',class_='price')  # Find the <bdi> element within the <span>
                    solde = price_elements.find('span',class_="text-danger")
                    if solde:
                        price = Price.fromstring(solde.text)
                    else:
                        price = Price.fromstring(price_elements.text)

                    item_data = CMN[product_name]
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

                    # def has_year(text):
                    #     pattern = r"\b\d{4}\b"  # Matches a four-digit year
                    #     match = re.search(pattern, text)
                    #     if match:
                    #         # Check if there's another year with an optional hyphen in between
                    #         year = match.group(0)
                    #         start_index = match.start()
                    #         end_index = match.end()
                    #         rest_of_text = text[start_index:]  # Text after the first year
                    #         if not re.search(rf"\s*-\s*\d{{4}}", rest_of_text):
                    #            return True
                    #     return False
                    #
                    # print('"' + product_name + '" : "",' if not has_year(product_name) else 'rejected : ' + product_name)

                    price_ranges = [
                        (1, 9999999999, price),  # Quantity 1-10, price 10.0 per unit
                    ]

                    def price_between(value,ranges):
                        """
                        Returns the price per unit for a given quantity.
                        """
                        for min_qty, max_qty, price in ranges:
                            if (min_qty <= value < max_qty):
                                if isinstance(price,Price):
                                    return price.amount_float
                                else:
                                    return price
                    if source in already_added :
                        continue
                    coin = Item(name=name,
                                price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                                buy_premiums=';'.join(
                                    ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price * weights[name][0] * weights[name][1])) * 100.0 / (buy_price * weights[name][0] * weights[name][1])) for i in range(1, minimum)] +
                                    ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price * weights[name][0] * weights[name][1])) * 100.0 / (buy_price * weights[name][0] * weights[name][1])) for i in range(minimum, 751)]
                                ),
                                delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                                source="https://stonexbullion.com/fr" + source,
                                session_id=session_id,
                                bullion_type=bullion_type,
                                quantity=quantity,
                                minimum=minimum, timestamp=datetime.now(pytz.timezone('CET'))
                    )
                    session_prod.add(coin)
                    session_prod.commit()
                    already_added.add(source)

                except requests.exceptions.RequestException as e:
                    logger.error(f"Request error: {e}")

                except KeyError as e:
                    logger.error(f"KeyError: {product_name}")

        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")  # Log the exception with traceback
            print(traceback.format_exc())