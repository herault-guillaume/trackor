import pathlib

from models.model import CoinPrice, Session, poids_pieces_or
from sqlalchemy import func, asc
from sqlalchemy.sql.expression import and_
import json
from datetime import datetime, timedelta
from google.cloud import storage
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import random
import uuid
import statistics
from urllib.parse import urlparse
import traceback

import bullionvault
import acheterorargent
import aucoffre
# import joubertchange_5minimum
import gold
import achatoretargent
import capornumismatique
import changedelabourse
import changevivienne
import bdor
import orinvestissement
import lcdor
import oretchange
# import goldunion
import merson
import goldforex
import orobel
import monlingot
import bullionbypost
# import pieceor
import changerichelieu
import lmp
import goldavenue
import abacor
import goldreserve
import shopcomptoirdelor

def format_date_to_french_quarterly_hour(date):
    """
    Formats a datetime object to a French-formatted string with the quarter of the hour.

    Args:
      date: A datetime object.

    Returns:
      A string representing the date in French format and the quarter of the hour
      (e.g., "04/09/2024 à 11:00").
    """
    # French day and month names
    day_names = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    month_names = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

    day_name = day_names[date.weekday()]
    day = date.day
    month_name = month_names[date.month - 1]
    year = date.year
    hour = date.hour
    minute = date.minute
    quarter = int(minute / 12)  # Calculate the quarter (0, 1, 2, or 3)

    # Format the hour and minute strings with leading zeros
    hour_str = f"{hour:02d}"
    minute_str = f"{quarter * 5:02d}"

    return f" Dernière mise à jour le {day_name} {day} {month_name} {year} à {hour_str}h{minute_str}."

    # Get the current datetime
    current_time = datetime.now()

    # Format the current time to a French formatted string with quarterly hour
    formatted_time = format_date_to_french_quarterly_hour(current_time)

    print(formatted_time)

def update_json_file(new_data,
                     filename,
                     bucket_name='prixlouisdor'):
    """Updates a JSON file in Google Cloud Storage.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        file_name: The name of the JSON file within the bucket.
        new_data: The new JSON data (Python dictionary or list) to write to the file.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\guillaume.herault\PycharmProjects\trackor\trackor-431010-1ff28b492956.json"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    blob.upload_from_string(json.dumps(new_data,indent=0))
    # Set ACL to make the file publicly accessible
    blob.acl.all().grant_read()
    blob.acl.save()
    # Convert to JSON string with formatting

    print(f"File '{filename}' updated in bucket '{bucket_name}'")

def find_best_deals(session, session_id, num_deals=50,filename='./results/best_deals.json'):
    """
    Calculates the `num_deals` best deals (gold weight / price ratio)
    among the available coins and returns information about the corresponding coins.

    Args:
        session: SQLAlchemy Session object to interact with the database.
        : Session ID to filter the results.
        num_deals: Number of best deals to return (default 7).

    Returns:
        A list of dictionaries containing information about the coins with the best ratios,
        sorted in descending order of ratio.
    """

    results = (
        session.query(
            CoinPrice.nom,
            CoinPrice.j_achete,
            CoinPrice.prime_achat_perso,
            CoinPrice.source,
            CoinPrice.timestamp
        )
        .filter(CoinPrice.session_id == session_id )
        .all()
    )

    deals = []

    for row in results:
        if row.nom in poids_pieces_or and not 'lingot' in str(row.nom).lower():
            deals.append({
                "name": row.nom,
                "prime": "{:.1f}".format(row.prime_achat_perso),
                "source": row.source,
                "last_updated": format_date_to_french_quarterly_hour(row.timestamp)
            })

    # Sort deals by ratio in descending order and take the first `num_deals`
    sorted_deals = sorted(deals, key=lambda x: float(x["prime"]), reverse=False)[:num_deals]
    print(sorted_deals)
    try:
        with open(filename, "w") as f:
            json.dump(sorted_deals, f, indent=0)  # indent for better readability
        print(f"The best deals have been saved to {filename}")
        update_json_file(sorted_deals,pathlib.WindowsPath(filename).name)
    except IOError as e:
        print(f"Error writing to JSON file: {e}")

    return sorted_deals


def calculate_and_store_coin_data(session, session_id, coin_names, filename):
    """
    Calcule le total (j_achete + frais_port) pour chaque pièce,
    garde une seule pièce par source avec le prix le plus bas,
    trie par ordre croissant, et stocke les résultats dans un fichier JSON.
    Le diff est calculé par rapport à la médiane de toutes les pièces sélectionnées.

    Args:
        session: Objet Session SQLAlchemy pour interagir avec la base de données.
        : ID de la session de recherche.
        coin_names: Liste des noms de pièces à considérer.
        filename: Nom du fichier JSON pour stocker les résultats.
    """

    # Première requête pour obtenir tous les résultats avec les noms de pièces spécifiés
    all_results = (
        session.query(
            CoinPrice.nom,
            CoinPrice.prime_achat_perso,
            CoinPrice.source,
            CoinPrice.timestamp
        )
        .filter(CoinPrice.nom.in_(coin_names))
        .filter(CoinPrice.session_id == session_id)
        .all()
    )

    # Extraire le domaine de chaque URL source et le stocker dans un dictionnaire
    source_domains = {result: urlparse(result.source).netloc for result in all_results}

    # Filtrer et sélectionner la pièce la moins chère par domaine en Python
    unique_results = []
    seen_domains = set()
    for result in all_results:
        domain = source_domains[result]
        if domain not in seen_domains:
            cheapest_coin = min(
                (r for r in all_results if source_domains[r] == domain),
                key=lambda x: x.prime_achat_perso
            )
            unique_results.append(cheapest_coin)
            seen_domains.add(domain)

    # Trier les résultats par prix total croissant
    unique_results.sort(key=lambda x: x.prime_achat_perso)

    # Calcul de la médiane de tous les prix
    all_totals = [row.prime_achat_perso for row in unique_results]
    # if all_totals:
    #     median_total = statistics.median(all_totals)
    # else:
    #     median_total = 0

    # Conversion des résultats en dictionnaire, en calculant la différence par rapport à la moyenne
    data = []
    for i, row in enumerate(unique_results):
        row_data = {
            "source": row.source,
            "prime": "{:.1f}".format(row.prime_achat_perso),
            "last_updated": format_date_to_french_quarterly_hour(row.timestamp)
        }
        data.append(row_data)

    # Stockage dans un fichier JSON
    with open(filename, "w", encoding='utf8') as f:
        json.dump(data, f, indent=0)

    update_json_file(data, filename=pathlib.WindowsPath(filename).name)

    return data

def fetch_and_update_data():
    for attempt in range(5):
        time.sleep(5)# Retry up to 5 times
        try:
            start_time = time.time()
            session_id = uuid.uuid4()
            session = Session()

            buy_price,sell_price = bullionvault.get(session,session_id)

            abacor.get_price_for(session,session_id,buy_price)
            acheterorargent.get_price_for(session,session_id,buy_price)
            achatoretargent.get_price_for(session,session_id,buy_price)
            aucoffre.get_price_for(session,session_id,buy_price)
            bdor.get_price_for(session,session_id,buy_price)
            bullionbypost.get_price_for(session,session_id,buy_price)
            capornumismatique.get_price_for(session,session_id,buy_price)
            changedelabourse.get_price_for(session,session_id,buy_price)
            changerichelieu.get_price_for(session,session_id,buy_price)
            changevivienne.get_price_for(session,session_id,buy_price)
            gold.get_price_for(session,session_id,buy_price)
            goldavenue.get_price_delivery_for(session,session_id,buy_price)
            goldforex.get_price_for(session,session_id,buy_price)
            goldreserve.get_price_for(session,session_id,buy_price)
            lmp.get_price_for(session,session_id,buy_price)
            lcdor.get_price_for(session,session_id,buy_price)
            merson.get_price_for(session,session_id,buy_price)
            monlingot.get_price_for(session,session_id,buy_price)
            oretchange.get_price_for(session,session_id,buy_price)
            orinvestissement.get_price_for(session,session_id,buy_price)
            orobel.get_price_for(session,session_id,
                                 buy_price)
            shopcomptoirdelor.get_price_for(session,session_id,buy_price)

            # goldunion.get(session,session_id)  # arnaque?
            # joubertchange.get(session,session_id)
            # pieceor.get(session,session_id)

            find_best_deals(session,session_id,num_deals=15)
            calculate_and_store_coin_data(session, session_id, ['1 oz krugerrand'], './results/1_oz_krugerrand.json')
            calculate_and_store_coin_data(session, session_id, ['20 francs or coq marianne',
                                                                        '20 francs or cérès',
                                                                        '20 francs or génie debout',
                                                                        '20 francs or napoléon III',
                                                                        '20 francs or louis XVIII buste nu',
                                                                        '20 francs or charles X',
                                                                        '20 francs or louis XVIII buste habillé',
                                                                        '20 francs or louis philippe lauré',
                                                                        '20 francs or napoléon empereur',
                                                                        '20 francs or napoléon empereur lauré',
                                                                        '20 francs or louis-napoléon bonaparte',
                                                                        '20 francs or fr',
                                                                        '20 francs or',
                                                                        ],
                                          './results/20_fr_france.json')
            calculate_and_store_coin_data(session, session_id, ['20 francs or leopold I','20 francs or union latine',
                                                                '20 lire or umberto I','20 lire or vittorio emanuele II'],
                                          './results/20_fr_union_latine.json')
            calculate_and_store_coin_data(session, session_id, [],
                                          './results/20_lires_italie.json')
            calculate_and_store_coin_data(session, session_id, ['20 francs or vreneli croix suisse',
                                                                        '20 francs or helvetia suisse'],
                                          './results/20_fr_suisse.json')
            calculate_and_store_coin_data(session, session_id, ['souverain or edouart VII',
                                                                        'souverain or georges V',
                                                                        'souverain or elizabeth II'
                                                                        'souverain or victoria jubilee'],
                                          './results/1_souv_ru.json')
            calculate_and_store_coin_data(session, session_id, ['1/2 souverain or georges V',
                                                                        '1/2 souverain or victoria',
                                                                ],
                                          './results/1_2_souv_ru.json')
            calculate_and_store_coin_data(session, session_id, ['50 pesos or'], './results/50_pesos_mex.json')
            calculate_and_store_coin_data(session, session_id, ['20 mark or wilhelm II'], './results/20_mark_all.json')
            calculate_and_store_coin_data(session, session_id, ['5 dollars or liberté','5 dollars or tête indien'],
                                          './results/5_dol_usa.json')
            calculate_and_store_coin_data(session, session_id, ['20 dollars or liberté'], './results/20_dol_usa.json')
            calculate_and_store_coin_data(session, session_id, ['10 dollars or liberté','10 dollars or tête indien'],
                                          './results/10_dol_usa.json')
            calculate_and_store_coin_data(session, session_id, ['10 francs or coq marianne',
                                                                        '10 francs or cérès 1850-1851',
                                                                        '10 francs or napoléon III'],
                                          './results/10_fr_france.json')
            print("--- %s seconds ---" % (time.time() - start_time))
            return  # Sortir de la fonction si la mise à jour est réussie

        except Exception as e:
            print(f"Tentative {attempt + 1} échouée")
            print(traceback.format_exc())
            time.sleep(5)  # Attendre 5 secondes avant de réessayer

scheduler = BackgroundScheduler()
fetch_and_update_data()
# Schedule the jobs at 11 AM and 7 PM with randomization
scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=12, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_12am'
)

scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=19, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_9pm'
)

scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=9, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_9am'
)

scheduler.start()

try:
    while True:
        time.sleep(2)  # Keep the main thread alive
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()