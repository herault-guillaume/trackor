import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import random
import uuid
import traceback
from seleniumbase import Driver

import bullionvault
import acheterorargent
import aucoffre
import gold
import achatoretargent
import capornumismatique
import changedelabourse
import changevivienne
import comptoirdestuileries
import bdor
import orinvestissement
import lcdor
import oretchange
import stonexbullion
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
import logging_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import sshtunnel

sshtunnel.SSH_TIMEOUT = 15.0
sshtunnel.TUNNEL_TIMEOUT = 15.0

logging_config.setup_logging()

def fetch_and_update_data():
    for attempt in range(1):
        with sshtunnel.SSHTunnelForwarder(
                ('ssh.pythonanywhere.com'),
                ssh_username='Pentagruel',
                ssh_password='M1nceMaManette',
                remote_bind_address=('pentagruel.mysql.pythonanywhere-services.com', 3306),
                local_bind_address=('127.0.0.1', 3306)
                # Your database hostname
        ) as tunnel:

            engine_prod = create_engine(
                f"mysql+mysqlconnector://Pentagruel:(US)ue%1(US)ue%1@127.0.0.1:{tunnel.local_bind_port}/Pentagruel$bullionsniper"
            )
            engine_staging = create_engine(
                f"mysql+mysqlconnector://Pentagruel:(US)ue%1(US)ue%1@127.0.0.1:{tunnel.local_bind_port}/Pentagruel$staging-bullionsniper"
            )

            driver = Driver(uc=True, headless=True)
            time.sleep(5)
            try:
                start_time = time.time()
                session_id = str(uuid.uuid4())

                Session_prod = sessionmaker(bind=engine_prod)
                Session_staging = sessionmaker(bind=engine_staging)

                session_prod = Session_prod()
                session_staging = Session_staging()

                buy_price_gold,g_sell_price_eur,buy_price_silver,s_sell_price_eur = bullionvault.get(session_prod,session_id,driver)
                #buy_price_gold,g_sell_price_eur,buy_price_silver,s_sell_price_eur = 81.57, 81.42, 1.022, 1.019

                abacor.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                achatoretargent.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver)
                acheterorargent.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                bdor.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver)
                bullionbypost.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver)
                capornumismatique.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                changedelabourse.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                changerichelieu.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                changevivienne.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                comptoirdestuileries.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                gold.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                goldavenue.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver)
                # goldforex.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                goldreserve.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                lcdor.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                lmp.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                merson.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                monlingot.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                oretchange.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                orinvestissement.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                orobel.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver)
                shopcomptoirdelor.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver)
                stonexbullion.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver,driver)

                #aucoffre.get_price_for(session_prod,session_id,buy_price_gold,buy_price_silver)
                # goldunion.get(session,session_id)  # arnaque?
                # joubertchange.get(session,session_id)
                # pieceor.get(session,session_id)

                return  # Sortir de la fonction si la mise à jour est réussie

            except Exception as e:
                print(f"Tentative {attempt + 1} échouée")
                print(traceback.format_exc())
                time.sleep(5)  # Attendre 5 secondes avant de réessayer
            finally:
                # Always close the session in a finally block
                session_prod.close()
                session_staging.close()

scheduler = BackgroundScheduler()
try :
    fetch_and_update_data()
except Exception as e :
    print(traceback.format_exc())
# quit()
# Schedule the jobs at 11 AM and 7 PM with randomization
scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=7, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_7am'
)

scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=9, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_9pm'
)

scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=11, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_11am'
)

scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=13, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_1_pm'
)

scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=15, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_3pm'
)

scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=17, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_5pm'
)

scheduler.add_job(
    fetch_and_update_data,
    CronTrigger(hour=19, minute=random.randint(0,30)),  # Adjust for minutes
    id='job_at_7pm'
)

scheduler.start()

try:
    while True:
        time.sleep(2)  # Keep the main thread alive
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()