import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from datetime import datetime
import traceback
from price_parser import Price

header_achat_or_argent_map_model = {
    'Nom': 'nom',
    'AchatVous vendez': 'je_vend',
    'VenteVous achetez': 'j_achete',
    'Cotation française': 'cotation_francaise',
    'Prime achat': 'prime_achat_vendeur',
    'Prime vente': 'prime_vente_vendeur',
}

def get_delivery_price(price):
    if price < 500:
        return 18.0
    elif price < 1000:
        return 15.0
    elif price < 3000:
        return 20.0
    elif price < 10000:
        return 30.0
    elif price < 20000:
        return 45.0
    elif price < 50000:
        return 90.0
    elif price < 75000:
        return 150.0
    elif price < 100000:
        return 180.0
    elif price < 150000:
        return 240.0
    else:
        return 0.0

def get_price_for(session,session_id,buy_price):

    urls = ['https://www.acheter-or-argent.fr/?fond=rubrique&id_rubrique=2&page={i}&nouveaute=&promo='.format(i=i) for i in range(1,9)]
    for url in urls :
        print(url)
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        div_product= soup.find_all('div','petitBlocProduit')
        for product in div_product :
            try :
                product_name_url = product.find('a','art-button')

                product_price = Price.fromstring(product.find('span','prixProduit').text)
                print(product_price,product_name_url.text)
                coin = CoinPrice(nom=product_name_url.text[1:],
                                 j_achete=product_price.amount_float,
                                 source=product_name_url['href'],
                                 prime_achat_perso=((product_price.amount_float + get_delivery_price(product_price.amount_float)) - (
                                             buy_price * poids_pieces_or[product_name_url.text[1:]])) * 100.0 / (buy_price *
                                                   poids_pieces_or[product_name_url.text[1:]]),

                                 frais_port=get_delivery_price(product_price.amount_float), session_id=session_id)
                session.add(coin)
                session.commit()

            except :
                print(traceback.format_exc())



# def get_price_for(buy_gp,sell_gp,table_index,session,session_id):

#
# def get_price_for(buy_gp,sell_gp,table_index,session,session_id):
#     """
#     Extracts data from the specified table, maps headers, and stores it in the database.
#
#     Args:
#         url: The URL of the web page containing the table.
#         table_index: The index of the table to extract (0 for first, 1 for second).
#     """
#     print("https://www.acheter-or-argent.fr/")
#     url = 'https://www.acheter-or-argent.fr/client/plugins/sebtab/tableau.php'
#
#     response = requests.get(url)
#     response.raise_for_status()
#
#     soup = BeautifulSoup(response.content, 'html.parser')
#     table = soup.find_all('table')[table_index]
#
#     # Determine the correct header row based on the table_index
#     header_row_index = 0
#     header_row = table.find_all('tr')[header_row_index]
#     headers = [th.text.strip().replace("\xa0", "").replace("\n", " ") for th in header_row.find_all('td')]
#
#     data = []
#
#     # Set the correct starting row for data extraction based on the table_index
#     start_row = 1
#
#     for row in table.find_all('tr')[start_row:]:
#         cells = row.find_all('td')
#         if not cells:
#             continue
#
#         row_data = {}
#         for i, cell in enumerate(cells):
#             value = cell.text.strip()
#             # Get text from anchor tag for the first column (nom)
#             if i == 0:
#                 anchor = cell.find('a')
#                 row_data['nom'] = anchor.text.strip() if anchor else value
#                 row_data['source'] = 'https://www.acheter-or-argent.fr/client/plugins/sebtab/tableau.php'
#
#             else:
#                 # Use header_to_model_map for attribute names
#                 attribute_name = header_achat_or_argent_map_model.get(headers[i])
#                 if attribute_name:
#                     value = value.replace('€', '')
#                     if value.endswith('%'):
#                         value = float(value.replace('%', ''))
#                     elif value.isdigit():
#                         value = int(value)
#                     elif ',' in value:
#                         value = float(value.replace(',', '.'))
#                     elif value == '':
#                         value = None
#
#                     row_data[attribute_name] = value
#         try :
#             row_data['prime_achat_perso'] = (float(row_data['j_achete']) - (poids_pieces_or[row_data['nom']] * buy_gp)) / float(row_data['j_achete']) * 100
#             row_data['prime_vente_perso'] = (float(row_data['je_vend']) - (poids_pieces_or[row_data['nom']] * sell_gp)) / float(row_data['je_vend']) * 100
#             print(row_data['nom'],float(row_data['j_achete']))
#         except Exception as e:
#             print(traceback.format_exc())
#             pass
#         data.append(row_data)
#
#     try:
#         for row_data in data:
#             gold_data = CoinPrice(**row_data,frais_port=get_delivery_price(float(row_data['j_achete'])),session_id=session_id)
#             session.add(gold_data)
#
#         session.commit()  # Save changes to the database
#     except Exception as e:
#         print(f"An error occurred: {e}",url)
#         print(traceback.format_exc())
#         session.rollback()  # Rollback changes in case of an error
#     finally:
#         session.close()
