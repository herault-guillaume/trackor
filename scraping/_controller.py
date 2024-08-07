
from models.model import CoinPrice, Session
from sqlalchemy import func, asc
import json
from datetime import datetime, timedelta
from google.cloud import storage
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import random

import traceback

import bullionvault
import achaterorargent
import aucoffre
# import joubertchange_5minimum
import gold
import achatoretargent
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


def update_json_file(new_data,
                     bucket_name='prixlouisdor',
                     file_name='site_data.json'):
    """Updates a JSON file in Google Cloud Storage.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        file_name: The name of the JSON file within the bucket.
        new_data: The new JSON data (Python dictionary or list) to write to the file.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\herau\PycharmProjects\trackor\trackor-431010-a4f698825e45.json"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_string(json.dumps(new_data,indent=0))
    # Set ACL to make the file publicly accessible
    blob.acl.all().grant_read()
    blob.acl.save()
    # Convert to JSON string with formatting

    print(f"File '{file_name}' updated in bucket '{bucket_name}'")


def calculate_and_store_coin_data(session,coin_name='20 francs or coq marianne',minutes=3,top=23):
    """
    Calcule le total (j_achete + frais_port) pour chaque pièce, trie par ordre décroissant,
    et stocke les résultats dans un fichier JSON.

    Args:
        session: Objet Session SQLAlchemy pour interagir avec la base de données.
    """

    # Requête SQLAlchemy pour calculer le total et trier
    now = datetime.utcnow()
    n_minutes_ago = now - timedelta(minutes=minutes)

    results = (
        session.query(
            CoinPrice.nom,
            (CoinPrice.j_achete + CoinPrice.frais_port).label("total"),
            CoinPrice.source
        )
        .filter(CoinPrice.nom == coin_name)
        .filter(CoinPrice.timestamp >= n_minutes_ago)
        .order_by(asc("total"))
        .limit(top)
    )

    # Conversion des résultats en dictionnaire
    data = [{"position": i,
             "source": row.source,
             "diff" : "{:.1f}%".format((row.total - list(results)[-1].total) * 100 / list(results)[-1].total)}
            for i,row in enumerate(results)]
    print(data)
    # Stockage dans un fichier JSON
    with open("coin_data.json", "w") as f:
        json.dump(data, f)

    return data
def fetch_and_update_data():
    for attempt in range(5):  # Retry up to 3 times
        try:
            session = Session()
            buy_price,sell_price = bullionvault.get(session)

            abacor.get_price_for(session)
            achaterorargent.get_price_for(buy_price, sell_price, 0, session)
            achaterorargent.get_price_for(buy_price, sell_price, 1, session)
            achatoretargent.get_price_for(session)
            aucoffre.get_price_for(session)
            bdor.get_price_for(session)
            bullionbypost.get_price_for(session)
            changedelabourse.get_price_for(session)
            changerichelieu.get_price_for(session)
            changevivienne.get_price_for(session)
            gold.get_price_for(session)
            goldavenue.get_price_delivery_for(session)
            goldforex.get_price_for(session)
            goldreserve.get_price_for(session)
            lmp.get_price_for(session)
            lcdor.get_price_for(session)
            merson.get_price_for(session)
            monlingot.get_price_for(session)
            oretchange.get_price_for(session)
            orinvestissement.get_price_for(session)
            orobel.get_price_for(session)
            shopcomptoirdelor.get_price_for(session)
            # goldunion.get(session)  # arnaque?
            # joubertchange.get(session)
            # pieceor.get(session)

            site_data = calculate_and_store_coin_data(session)

            update_json_file(site_data)
            return  # Sortir de la fonction si la mise à jour est réussie

        except Exception as e:
            print(f"Tentative {attempt + 1} échouée")
            print(traceback.format_exc())
            time.sleep(5)  # Attendre 5 secondes avant de réessayer

# scheduler = BackgroundScheduler()
#
# # Schedule the jobs at 11 AM and 7 PM with randomization
# scheduler.add_job(
#     fetch_and_update_data,
#     CronTrigger(hour=11, minute=random.randint(0,15)),  # Adjust for minutes
#     id='job_at_11am'
# )
#
# scheduler.add_job(
#     fetch_and_update_data,
#     CronTrigger(hour=18, minute=random.randint(0,15)),  # Adjust for minutes
#     id='job_at_7pm'
# )
#
# scheduler.add_job(
#     fetch_and_update_data,
#     CronTrigger(hour=19, minute=52),  # Adjust for minutes
#     id='job_at_8pm'
# )
#
# scheduler.start()
#
# try:
#     while True:
#         time.sleep(2)  # Keep the main thread alive
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()


fetch_and_update_data()