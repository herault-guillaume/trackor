
from models.model import CoinPrice, Session
from sqlalchemy import func, asc
import json
from datetime import datetime, timedelta

import bullionvault
import achatorargent
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

def calculate_and_store_coin_data(session,coin_name='20 francs or coq marianne',minutes=5,top=7):
    """
    Calcule le total (j_achete + frais_port) pour chaque pièce, trie par ordre décroissant,
    et stocke les résultats dans un fichier JSON.

    Args:
        session: Objet Session SQLAlchemy pour interagir avec la base de données.
    """

    # Requête SQLAlchemy pour calculer le total et trier
    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=minutes)

    results = (
        session.query(
            CoinPrice.nom,
            (CoinPrice.j_achete + CoinPrice.frais_port).label("total"),
            CoinPrice.source
        )
        .filter(CoinPrice.nom == coin_name)
        .filter(CoinPrice.timestamp >= five_minutes_ago)
        .order_by(asc("total"))
        .limit(top)
    )

    # Conversion des résultats en dictionnaire
    data = [{"position": i, "source": row.source} for i,row in enumerate(results)]
    print(data)
    # Stockage dans un fichier JSON
    with open("coin_data.json", "w") as f:
        json.dump(data, f)

session = Session()

buy_price,sell_price = bullionvault.get(session)
achatorargent.get(buy_price,sell_price,0,session)
achatorargent.get(buy_price,sell_price,1,session)
aucoffre.get(session)
# joubertchange.get(session)
gold.get(session)
achatoretargent.get(session)
changedelabourse.get(session)
changevivienne.get(session)
bdor.get(session)
orinvestissement.get(session)
lcdor.get(session)
oretchange.get(session)
# goldunion.get(session) arnaque?
merson.get(session)
goldforex.get(session)
orobel.get(session)
monlingot.get(session)
bullionbypost.get(session)
# pieceor.get(session)
changerichelieu.get(session)
lmp.get(session)
goldavenue.get(session)
abacor.get(session)
goldreserve.get(session)
shopcomptoirdelor.get(session)

calculate_and_store_coin_data(session)





