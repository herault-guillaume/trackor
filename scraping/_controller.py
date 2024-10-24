import pathlib

from models.model import Item, Session, poids_pieces
from sqlalchemy import func, asc
from sqlalchemy.sql.expression import and_, or_
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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Guillaume Hérault\PycharmProjects\trackor\trackor-431010-1ff28b492956.json"
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
            Item.name,
            Item.buy,
            Item.buy_premiums,
            Item.source,
            Item.timestamp
        )
        .filter(Item.session_id == session_id)
        .all()
    )

    print(        session.query(
            Item.name,
            Item.buy,
            Item.buy_premiums,
            Item.source,
            Item.timestamp
        )
        .filter(Item.session_id == session_id)
        .all())
    deals = []

    for row in results:
        if row.name in poids_pieces and not 'lingot' in str(row.name).lower():
            deals.append({
                "name": row.name[5:],
                "prime": "{:.1f}".format(row.buy_premiums),
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


def calculate_and_store_coin_data(session, session_id, coin_names, range_,filename):
    """
    Calcule le total (j_achete + delivery_fee) pour chaque pièce,
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

    for r in range_ :
        all_results = (
            session.query(
                Item.name,
                Item.buy_premiums,
                Item.source,
                Item.timestamp
            )
            .filter(
                or_(
                    Item.name.like(f"{coin_name}%") for coin_name in coin_names
                )
            )
            .filter(Item.session_id == session_id)
            .filter(
                or_(
                    and_ (
                            r[0] <= Item.quantity,
                            Item.quantity < r[1],
                    ),
                    and_ (
                            r[0] <= Item.minimum,
                            Item.minimum < r[1],
                    )
                ))
            .all()
        )

        print([i for i in all_results])

        # Extraire le domaine de chaque URL source et le stocker dans un dictionnaire
        source_domains = {result: urlparse(result.source).netloc for result in all_results}

        # Filtrer et sélectionner la pièce la moins chère par domaine
        unique_results = []
        seen_domains = set()
        for result in all_results:
            domain = source_domains[result]
            if domain not in seen_domains:
                cheapest_coin = min(
                    (r for r in all_results if source_domains[r] == domain),
                    key=lambda x: x.buy_premiums
                )
                unique_results.append(cheapest_coin)
                seen_domains.add(domain)

        # Trier les résultats par prix total croissant
        unique_results.sort(key=lambda x: x.buy_premiums)

        # Calcul de la médiane de tous les prix
        all_totals = [row.buy_premiums for row in unique_results]
        # if all_totals:
        #     median_total = statistics.median(all_totals)
        # else:
        #     median_total = 0

        # Conversion des résultats en dictionnaire, en calculant la différence par rapport à la moyenne
        data = []
        for i, row in enumerate(unique_results):
            row_data = {
                "source": row.source,
                "prime": "{:.1f}".format(row.buy_premiums),
                "last_updated": format_date_to_french_quarterly_hour(row.timestamp)
            }
            data.append(row_data)
        filename = pathlib.WindowsPath(filename)
        fp = filename.parent
        fn = filename.stem + '_{r_min}_{r_max}'.format(r_min = r[0],r_max = r[1]) + filename.suffix
        filepath = fp / fn
        # Stockage dans un fichier JSON
        with open(filepath, "w", encoding='utf8') as f:
            json.dump(data, f, indent=0)

        update_json_file(data, filename=filepath.name)

def fetch_and_update_data():
    for attempt in range(5):
        time.sleep(5)# Retry up to 5 times
        try:
            start_time = time.time()
            session_id = uuid.uuid4()
            session = Session()

            # buy_price_gold,g_sell_price_eur,buy_price_silver,s_sell_price_eur = bullionvault.get(session,session_id)
            buy_price_gold,g_sell_price_eur,buy_price_silver,s_sell_price_eur = 81.57, 81.42, 1.022, 1.019
            #
            # abacor.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # achatoretargent.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            acheterorargent.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # aucoffre.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # bdor.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # bullionbypost.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # capornumismatique.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # changedelabourse.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # changerichelieu.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # changevivienne.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # gold.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # goldavenue.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # goldforex.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # goldreserve.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # lmp.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # lcdor.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # merson.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # monlingot.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # oretchange.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # orinvestissement.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # orobel.get_price_for(session,session_id,buy_price_gold,buy_price_silver)
            # shopcomptoirdelor.get_price_for(session,session_id,buy_price_gold,buy_price_silver)

            # goldunion.get(session,session_id)  # arnaque?
            # joubertchange.get(session,session_id)
            # pieceor.get(session,session_id)

            # range_ = [(1,5),(5,10),(10,50),(50,500)]
            # find_best_deals(session,session_id,num_deals=15)
            # calculate_and_store_coin_data(session, session_id, ['or - 1 oz krugerrand'], range_,'./results/1_oz_krugerrand.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 20 francs fr'], range_,'./results/20_fr_france.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 20 francs bel leopold I','or - 20 francs union latine','or - 20 lire umberto I','or - 20 lire vittorio emanuele II'], range_, './results/20_fr_union_latine.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 20 lire'],range_,'./results/20_lires_italie.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 20 francs sui'],range_,'./results/20_fr_suisse.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 1 souverain'],range_,'./results/1_souv_ru.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 1/2 souverain'],range_,'./results/1_2_souv_ru.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 50 pesos mex'],  range_,'./results/50_pesos_mex.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 20 mark'],  range_,'./results/20_mark_all.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 5 dollars'],range_,'./results/5_dol_usa.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 20 dollars'],  range_,'./results/20_dol_usa.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 10 dollars'],range_,'./results/10_dol_usa.json')
            # calculate_and_store_coin_data(session, session_id, ['or - 10 francs fr'], range_,'./results/10_fr_france.json')
            # print("--- %s seconds ---" % (time.time() - start_time))
            return  # Sortir de la fonction si la mise à jour est réussie

        except Exception as e:
            print(f"Tentative {attempt + 1} échouée")
            print(traceback.format_exc())
            time.sleep(5)  # Attendre 5 secondes avant de réessayer


scheduler = BackgroundScheduler()
try :
    fetch_and_update_data()
except Exception as e :
    print(traceback.format_exc())
# quit()
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