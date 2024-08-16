
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
import uuid

import traceback

import bullionvault
import acheterorargent
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


def calculate_and_store_coin_data(session,session_id,coin_name='20 francs or coq marianne'):
    """
    Calcule le total (j_achete + frais_port) pour chaque pièce, trie par ordre décroissant,
    et stocke les résultats dans un fichier JSON.

    Args:
        session: Objet Session SQLAlchemy pour interagir avec la base de données.
    """

    results = (
        session.query(
            CoinPrice.nom,
            (CoinPrice.j_achete + CoinPrice.frais_port).label("total"),
            CoinPrice.source
        )
        .filter(CoinPrice.nom == coin_name)
        .filter(CoinPrice.session_id == session_id)
        .order_by(asc("total"))
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
    for attempt in range(1):  # Retry up to 3 times
        try:
            session_id = uuid.uuid4()
            session = Session()

            #buy_price,sell_price = bullionvault.get(session)

            #abacor.get_price_for(session,session_id)
            #acheterorargent.get_price_for(buy_price, sell_price, 0, session,session_id)
            #acheterorargent.get_price_for(buy_price, sell_price, 1, session,session_id)
            #achatoretargent.get_price_for(session,session_id)
            #aucoffre.get_price_for(session,session_id)
            #bdor.get_price_for(session,session_id)
            # bullionbypost.get_price_for(session,session_id)
            # changedelabourse.get_price_for(session,session_id)
            # changerichelieu.get_price_for(session,session_id)
            # changevivienne.get_price_for(session,session_id)
            # gold.get_price_for(session,session_id)
            # goldavenue.get_price_delivery_for(session,session_id)
            # goldforex.get_price_for(session,session_id)
            # goldreserve.get_price_for(session,session_id)
            # lmp.get_price_for(session,session_id)
            # lcdor.get_price_for(session,session_id)
            # merson.get_price_for(session,session_id)
            # monlingot.get_price_for(session,session_id)
            # oretchange.get_price_for(session,session_id)
            # orinvestissement.get_price_for(session,session_id)
            orobel.get_price_for(session,session_id)
            # shopcomptoirdelor.get_price_for(session,session_id)


            # goldunion.get(session,session_id)  # arnaque?
            # joubertchange.get(session,session_id)
            # pieceor.get(session,session_id)

            site_data = calculate_and_store_coin_data(session,session_id)

            # update_json_file(site_data)
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