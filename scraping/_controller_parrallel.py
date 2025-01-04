import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import random
import uuid
import traceback
from seleniumbase import Driver
from concurrent.futures import ThreadPoolExecutor
import sshtunnel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Import your website modules (e.g., bullionvault, acheterorargent, etc.)
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
import merson
import goldforex
import orobel
import monlingot
import bullionbypost
import changerichelieu
import lmp
import goldavenue
import abacor
import goldreserve
import shopcomptoirdelor

import logging_config

sshtunnel.SSH_TIMEOUT = 15.0
sshtunnel.TUNNEL_TIMEOUT = 15.0

logging_config.setup_logging()

def get_price(website_func, db_uri, session_id, buy_price_gold, buy_price_silver, driver=None):
    """Wrapper for parallel execution, creates session within each process."""
    try:
        engine = create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        if driver:
            website_func(session, session_id, buy_price_gold, buy_price_silver, driver)
        else:
            website_func(session, session_id, buy_price_gold, buy_price_silver)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error in {website_func.__module__}: {e}")
        traceback.print_exc()
        return False
    finally:
        session.close()
        engine.dispose()

def fetch_and_update_data():
        with sshtunnel.SSHTunnelForwarder(
                ('ssh.pythonanywhere.com'),
                ssh_username='Pentagruel',
                ssh_password='M1nceMaManette',
                remote_bind_address=('pentagruel.mysql.pythonanywhere-services.com', 3306),
                local_bind_address=('127.0.0.1', 3306)
        ) as tunnel:
            db_uri = f"mysql+mysqlconnector://Pentagruel:(US)ue%1(US)ue%1@127.0.0.1:{tunnel.local_bind_port}/Pentagruel$bullionsniper"
            engine_main = create_engine(db_uri)
            Session_main = sessionmaker(bind=engine_main)
            session_main = Session_main()
            driver = Driver(uc=True, headless=True) # Driver created inside the tunnel context
            time.sleep(5)
            session_id = str(uuid.uuid4())

            buy_price_gold, g_sell_price_eur, buy_price_silver, s_sell_price_eur = bullionvault.get(session_main, session_id, driver)
            session_main.close()
            engine_main.dispose()

            website_functions = [
                (abacor.get_price_for, None),
                (achatoretargent.get_price_for, None),
                (acheterorargent.get_price_for, None),
                (bdor.get_price_for, None),
                (bullionbypost.get_price_for, None),
                (capornumismatique.get_price_for, None),
                (changedelabourse.get_price_for, None),
                (changerichelieu.get_price_for, None),
                (changevivienne.get_price_for, None),
                (comptoirdestuileries.get_price_for, None),
                (gold.get_price_for, None),
                (goldavenue.get_price_for, None),
                # (goldforex.get_price_for, None),
                (goldreserve.get_price_for, None),
                (lcdor.get_price_for, None),
                (lmp.get_price_for, None),
                (merson.get_price_for, None),
                (monlingot.get_price_for, None),
                (oretchange.get_price_for, None),
                (orinvestissement.get_price_for, None),
                (orobel.get_price_for, None),
                (shopcomptoirdelor.get_price_for, None),
                (stonexbullion.get_price_for, None),
            ]

            with ThreadPoolExecutor() as executor:  # Use ThreadPoolExecutor
                futures = [
                    executor.submit(get_price, func, db_uri, session_id, buy_price_gold, buy_price_silver, driver_arg)
                    for func, driver_arg in website_functions]

                results = [future.result() for future in futures]  # Get results from futures
            if not all(results):
                print(results)
            return

fetch_and_update_data() # Run once on startup

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_update_data, CronTrigger(hour=7, minute=random.randint(0,30)), id='job_at_7am')
scheduler.add_job(fetch_and_update_data, CronTrigger(hour=9, minute=random.randint(0,30)), id='job_at_9am')
scheduler.add_job(fetch_and_update_data, CronTrigger(hour=11, minute=random.randint(0,30)), id='job_at_11am')
scheduler.add_job(fetch_and_update_data, CronTrigger(hour=13, minute=random.randint(0,30)), id='job_at_1pm')
scheduler.add_job(fetch_and_update_data, CronTrigger(hour=15, minute=random.randint(0,30)), id='job_at_3pm')
scheduler.add_job(fetch_and_update_data, CronTrigger(hour=17, minute=random.randint(0,30)), id='job_at_5pm')
scheduler.add_job(fetch_and_update_data, CronTrigger(hour=19, minute=random.randint(0,30)), id='job_at_7pm')

scheduler.start()

try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()