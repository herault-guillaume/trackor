import requests
from bs4 import BeautifulSoup
from models.offre import GoldData, Session
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

header_achat_or_argent_map_model = {
    'Nom': 'nom',
    'AchatVous vendez': 'je_vend',
    'VenteVous achetez': 'j_achete',
    'Cotation française': 'cotation_francaise',
    'Prime achat': 'prime_achat_vendeur',
    'Prime vente': 'prime_vente_vendeur',
}

poids_pieces_or = {
    'Lingot or 1 once LBMA': 31.103,
    'Lingot or 1 g': 1.0,
    'Lingot or 5 g LBMA': 5.0,
    'Lingot or 10 g LBMA': 10.0,
    'Lingot or 20 g LBMA': 20.0,
    'Lingot or 50 g LBMA': 50.0,
    'Lingot or 100 g LBMA': 100.0,
    'Lingot or 250 g LBMA': 250.0,
    'Lingot or 500 g LBMA': 500.0,
    'Lingot or 1 kg LBMA': 1000.0,
    '1 oz philharmonique': 31.103,
    '20 francs or coq marianne': 5.805,
    '20 francs or napoléon III': 5.805,
    '20 francs or génie debout': 5.805,
    '20 francs or cérès': 5.805,
    '10 francs or napoléon III': 2.9025,
    '10 francs or coq marianne': 2.613,
    '10 francs or cérès 1850-1851': 2.903,
    '40 francs or napoléon empereur lauré': 11.613,
    '50 francs or napoléon III tête nue': 14.516,
    '100 francs or napoléon III tête nue': 29.02,
    '20 francs or vreneli croix suisse': 5.806,
    '20 francs or union latine léopold II': 5.805,
    '20 francs or tunisie': 5.80,
    '50 pesos or': 37.5,
    '20 dollars or liberté': 30.093,
    '10 dollars or liberté': 15.047,
    '5 dollars or liberté': 7.523,
    'souverain or georges V': 7.318,
    'souverain or victoria jubilee': 7.318,
    'souverain or elizabeth II': 7.318,
    'demi souverain or georges V': 3.66,
    '20 mark or wilhelm II': 7.168,
    '1 oz maple leaf': 31.103,
    '1 oz krugerrand': 31.103,
    '1 oz american eagle': 31.103,
    '1 oz nugget / kangourou': 31.103,
    '10 florins or wilhelmina': 6.056,
    '10 florins or willem III': 6.048,
    "20 pesos or": 15.0,  # Approximatif
    "10 pesos or": 7.5,   # Approximatif
    "5 pesos or": 3.75,    # Approximatif
    "50 écus or charles quint": 15.552,  # Approximatif
    '1/2 oz maple leaf': 15.552,
    '1/4 oz maple leaf': 7.776,
    '1/10 oz maple leaf': 3.11,
    '1/2 oz krugerrand': 15.269,
    '1/4 oz krugerrand': 7.634,
    '1/10 oz krugerrand': 3.054,
    '1/2 oz american eagle': 15.552,
    '1/4 oz american eagle': 7.776,
    '1/10 oz american eagle': 3.11,
    '1/2 oz nugget / kangourou': 15.552,
    '1/4 oz nugget / kangourou': 7.776,
    '1/10 oz nugget / kangourou': 3.11,
    '100 couronnes or françois joseph I': 30.488,
    '20 couronnes or françois joseph I': 6.098,
    '10 couronnes or françois joseph I': 3.049,
    '8 florins 20 francs or franz joseph I': 5.805,
    '4 florins 10 francs 1892 refrappe': 2.90,
    '4 ducats or': 13.78,
    '1 ducat or': 3.44,
    '20 francs or helvetia suisse': 5.805,
    '20 lire or umberto I': 5.805,
    '20 lire or vittorio emanuele II': 5.805,
    '10 francs or vreneli croix suisse': 2.903
}

# poids_pieces_or_total = {
#     "Lingot or 1 once LBMA": 31.103,
#     "Lingot or 1 g": 1.0,
#     "Lingot or 5 g LBMA": 5.0,
#     "Lingot or 10 g LBMA": 10.0,
#     "Lingot or 20 g LBMA": 20.0,
#     "Lingot or 50 g LBMA": 50.0,
#     "Lingot or 100 g LBMA": 100.0,
#     "Lingot or 250 g LBMA": 250.0,
#     "Lingot or 500 g LBMA": 500.0,
#     "Lingot or 1 kg LBMA": 1000.0,
#     "1 oz philharmonique": 31.103,
#     "20 francs or coq marianne": 6.451,
#     "20 francs or napoléon III": 6.451,
#     "20 francs or génie debout": 5.806,
#     "20 francs or cérès": 6.4516,
#     "10 francs or napoléon III": 3.225,
#     "10 francs or coq marianne": 2.9032,
#     "10 francs or cérès 1850-1851": 3.2258,
#     "40 francs or napoléon empereur lauré": 12.903,
#     "50 francs or napoléon III tête nue": 16.129,
#     "100 francs or napoléon III tête nue": 32.258,
#     "20 francs or vreneli croix suisse": 6.451,
#     "20 francs or union latine léopold II": 6.451,
#     "20 francs or tunisie": 5.806,
#     "50 pesos or": 41.666,
#     "20 dollars or liberté": 33.437,
#     "10 dollars or liberté": 16.718,
#     "5 dollars or liberté": 8.359,
#     "souverain or georges V": 7.988,
#     "souverain or victoria jubilee": 7.988,
#     "souverain or elizabeth II": 7.988,
#     "demi souverain or georges V": 3.994,
#     "20 mark or wilhelm II": 7.965,
#     "1 oz maple leaf": 31.103,
#     "1 oz krugerrand": 33.931,
#     "1 oz american eagle": 31.103,
#     "1 oz nugget / kangourou": 31.103,
#     "10 florins or wilhelmina": 6.729,  # Approximatif
#     "10 florins or willem III": 6.72,  # Approximatif
#     "20 pesos or": 16.66,  # Approximatif
#     "10 pesos or": 8.33,   # Approximatif
#     "5 pesos or": 4.16,    # Approximatif
#     "2,5 pesos or": 2.08,   # Approximatif
#     "2 pesos or": 1.66,    # Approximatif
#     "50 écus or charles quint": 16.129,  # Approximatif
#     "1/2 oz maple leaf": 15.551,
#     "1/4 oz maple leaf": 7.775,
#     "1/10 oz maple leaf": 3.110,
#     "1/2 oz krugerrand": 16.965,
#     "1/4 oz krugerrand": 8.482,
#     "1/10 oz krugerrand": 3.393,
#     "1/2 oz american eagle": 15.551,
#     "1/4 oz american eagle": 7.775,
#     "1/10 oz american eagle": 3.110,
#     "1/2 oz nugget / kangourou": 15.551,
#     "1/4 oz nugget / kangourou": 7.775,
#     "1/10 oz nugget / kangourou": 3.110,
#     "100 couronnes or françois joseph I": 33.875,  # Approximatif
#     "20 couronnes or françois joseph I": 6.775,   # Approximatif
#     "10 couronnes or françois joseph I": 3.387,   # Approximatif
#     "8 florins 20 francs or franz joseph I": 6.8,   # Approximatif
#     "4 florins 10 francs 1892 refrappe": 3.4,     # Approximatif
#     "4 ducats or": 13.96,  # Approximatif
#     "1 ducat or": 3.49,  # Approximatif
#     "20 francs or helvetia suisse": 6.451,
#     "20 lire or umberto I": 6.451,
#     "20 lire or vittorio emanuele II": 6.451,
#     "10 francs or vreneli croix suisse": 3.225,
# }
def get_bullionvault_gold_price_euro():
    """Uses Selenium to click the currency button, then scrapes the 1 kg gold price in Euros."""

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')  # Headless mode for efficiency
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://or.bullionvault.fr/"
        driver.get(url)

        # Locate and click the Euro button
        euro_button = WebDriverWait(driver, 2).until(
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

        # Extract the price from the span
        buy_price_element = driver.find_element(By.CSS_SELECTOR, '#buyGOLDPrice span.EUR')
        buy_price_text = buy_price_element.text.strip()

        # Clean the text and convert to a float
        buy_price_eur = float(buy_price_text.split('€')[0].replace('\xa0', '').replace(',', '.').replace(' ',''))/1000.0  # Remove € and nbsp

        # Extract the price from the span
        sell_price_element = driver.find_element(By.CSS_SELECTOR, '#sellGOLDPrice span.EUR')
        sell_price_text = sell_price_element.text.strip()

        # Clean the text and convert to a float
        sell_price_eur = float(sell_price_text.split('€')[0].replace('\xa0', '').replace(',', '.').replace(' ',''))/1000.0  # Remove € and nbsp


        return buy_price_eur,sell_price_eur

    except Exception as e:
        print(f"Error scraping BullionVault: {e}")
        return None

    finally:
        driver.quit()

def get_aucoffre_price():
    """
    Scrapes the AuCOFFRE website to get the buy price of 20 Francs coins.
    It first locates the div containing a specific flag image,
    then extracts the price text from within that div.
    """
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome()
    url = "https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-1/produit"
    driver.get(url)
    print('test')

    # Locate the div by its data-url attribute (using XPath)
    xpath = "//div[contains(@data-url, '20f-marianne')]"
    target_div = WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

    print(target_div)

    # Extract the price text from within the div
    price_element = target_div.find_element(By.CSS_SELECTOR, '.text-xlarge.text-bolder.m-0.text-nowrap')
    price_text = price_element.text.strip()

    # Clean the price text and convert to float
    price = float(price_text.replace('€', ''))

    if price:
        return price
    else:
        raise ValueError("Could not parse the price correctly.")


# Example Usage:


def get_achat_or_argent_gold_price_euro(url,buy_gp,sell_gp,table_index):
    """
    Extracts data from the specified table, maps headers, and stores it in the database.

    Args:
        url: The URL of the web page containing the table.
        table_index: The index of the table to extract (0 for first, 1 for second).
    """
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')[table_index]

    # Determine the correct header row based on the table_index
    header_row_index = 0
    header_row = table.find_all('tr')[header_row_index]
    headers = [th.text.strip().replace("\xa0", "").replace("\n", " ") for th in header_row.find_all('td')]

    data = []

    # Set the correct starting row for data extraction based on the table_index
    start_row = 1

    for row in table.find_all('tr')[start_row:]:
        cells = row.find_all('td')
        if not cells:
            continue

        row_data = {}
        for i, cell in enumerate(cells):
            value = cell.text.strip()
            # Get text from anchor tag for the first column (nom)
            if i == 0:
                anchor = cell.find('a')
                row_data['nom'] = anchor.text.strip() if anchor else value
                row_data['source'] = 'achat-or-argent'

            else:
                # Use header_to_model_map for attribute names
                attribute_name = header_achat_or_argent_map_model.get(headers[i])
                if attribute_name:
                    value = value.replace('€', '')
                    if value.endswith('%'):
                        value = float(value.replace('%', ''))
                    elif value.isdigit():
                        value = int(value)
                    elif ',' in value:
                        value = float(value.replace(',', '.'))
                    elif value == '':
                        value = None

                    row_data[attribute_name] = value
        try :
            row_data['prime_achat_perso'] = (float(row_data['j_achete']) - (poids_pieces_or[row_data['nom']] * buy_gp)) / float(row_data['j_achete']) * 100
            row_data['prime_vente_perso'] = (float(row_data['je_vend']) - (poids_pieces_or[row_data['nom']] * sell_gp)) / float(row_data['je_vend']) * 100
        except Exception as e:
            print(e,'not present in weight database')
            pass
        data.append(row_data)
    # Add data to the session (same as before)
    session = Session()
    try:
        for row_data in data:
            # Check if the item already exists (to prevent duplicates)
            # existing_item = session.query(GoldData).filter_by(nom=row_data['nom']).first()
            #
            # if existing_item:
            #     # Update existing item if it's newer
            #     if existing_item.timestamp < datetime.datetime.utcnow():
            #         for key, value in row_data.items():
            #             setattr(existing_item, key, value)
            # else:
            # Create a new GoldData object
            gold_data = GoldData(**row_data)
            session.add(gold_data)

        session.commit()  # Save changes to the database
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback changes in case of an error
    finally:
        session.close()

    return True

# buy_gp,sell_gp = get_bullionvault_gold_price_euro()

# Exemple d'utilisation
# url = 'https://www.acheter-or-argent.fr/client/plugins/sebtab/tableau.php'  # Remplacez par l'URL réelle
# lingots = get_achat_or_argent_gold_price_euro(url,buy_gp,sell_gp,0)
# monnaies = get_achat_or_argent_gold_price_euro(url,buy_gp,sell_gp,1)

# https://www.aucoffre.com/recherche/metal-1/marketing_list-5/stype-1/produit
buy_price = get_aucoffre_price()
if buy_price:
    print(f"Buy price on AuCOFFRE: €{buy_price:.2f}")

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




