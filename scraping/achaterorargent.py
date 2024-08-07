import requests
from bs4 import BeautifulSoup
from models.model import CoinPrice, poids_pieces_or
from datetime import datetime

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
def get_price_for(buy_gp,sell_gp,table_index,session):
    """
    Extracts data from the specified table, maps headers, and stores it in the database.

    Args:
        url: The URL of the web page containing the table.
        table_index: The index of the table to extract (0 for first, 1 for second).
    """
    url = 'https://www.acheter-or-argent.fr/client/plugins/sebtab/tableau.php'

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
                row_data['source'] = 'https://www.acheter-or-argent.fr/client/plugins/sebtab/tableau.php'

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
            print(e,'not present in weight database',url)
            pass
        data.append(row_data)

    try:
        for row_data in data:
            gold_data = CoinPrice(**row_data,frais_port=get_delivery_price(float(row_data['j_achete'])))
            session.add(gold_data)

        session.commit()  # Save changes to the database
    except Exception as e:
        print(f"An error occurred: {e}",url)
        session.rollback()  # Rollback changes in case of an error
    finally:
        session.close()

    return True
