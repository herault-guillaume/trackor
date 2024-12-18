from dotenv import load_dotenv
load_dotenv()

import os
import sshtunnel
import pandas as pd
import datetime
from sqlalchemy import create_engine, func, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
from apscheduler.schedulers.background import BackgroundScheduler

import pytz
from pieces import weights

# Database and SSH Configuration
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
SSH_HOST = os.getenv('SSH_HOST')
SSH_USERNAME = os.getenv('SSH_USERNAME')
SSH_PASSWORD = os.getenv('SSH_PASSWORD')
REMOTE_BIND_ADDRESS = os.getenv('REMOTE_BIND_ADDRESS')
REMOTE_PORT_ADDRESS = int(os.getenv('REMOTE_PORT_ADDRESS'))
sshtunnel.SSH_TIMEOUT = float(os.getenv('SSH_TIMEOUT', 3600.0))
sshtunnel.TUNNEL_TIMEOUT = float(os.getenv('TUNNEL_TIMEOUT', 3600.0))

def create_tunnel():
    return sshtunnel.SSHTunnelForwarder(
        (os.getenv('SSH_HOST')),
        ssh_username=os.getenv('SSH_USERNAME'),
        ssh_password=os.getenv('SSH_PASSWORD'),
        remote_bind_address=(os.getenv('REMOTE_BIND_ADDRESS'), int(os.getenv('REMOTE_PORT_ADDRESS', 3306)))
    )

tunnel = create_tunnel()
tunnel.start()

# Create a SQLAlchemy engine
engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI').format(tunnel.local_bind_port))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def get_price(ranges, quantity):
    """
    Calculates the price based on the quantity and given ranges.

    Args:
    ranges: A string of ranges in the format '1-9;10-48;49-98;99-9999999999.9'.
    quantity: The quantity of the item.

    Returns:
    The price as a float.
    """
    ranges = ranges.split(';')
    for r in ranges:
        try :
            lower, upper, price = map(float, r.split('-'))
        except ValueError as e:
            print(ranges)
            print(r,lower, upper, price)
            raise Exception
        if lower <= quantity < upper:
            return price  # Return the price directly
    return None  # Or handle the case where quantity is outside all ranges

def query_to_dict(rset):
    """
    Converts a SQLAlchemy query result set to a pandas.Dataframe compatible dictionary .

    Args:
        rset: The result set from a SQLAlchemy query.

    Returns:
        A dictionary where keys are column names and values are lists of column values.
    """
    if not rset:
        return {}  # Return an empty dictionary if the result set is empty

    # Get column names from the first result object
    column_names = [column.name for column in rset[0].__table__.columns]

    # Construct the dictionary using list comprehensions
    return {
        column_name: [getattr(row, column_name) for row in rset]
        for column_name in column_names
    }

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True, index=True)
    price_ranges = Column(String(255), nullable=True)
    sell = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    minimum = Column(Integer, nullable=True)
    buy_premiums = Column(String(2000), nullable=True)
    delivery_fees = Column(String(2000), nullable=True)
    source = Column(String(1024), nullable=False)
    timestamp = Column(DateTime)
    session_id = Column(String(36), index=True)
    bullion_type = Column(String(2), nullable=True, index=False)

    @classmethod
    def get_items_by_bullion_type_and_quantity(cls, bullion_type, session_id, quantity):
        """
        Fetches items from the database that match the given bullion type, session_id and quantity.

        Args:
            session: SQLAlchemy session object.
            bullion_type: The type of bullion.
            session_id: The session ID.
            quantity: The desired quantity.

        Returns:
            A list of Item objects that match the criteria.
        """
        res = query_to_dict(
            session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == session_id,
                cls.minimum <= quantity,
                cls.quantity <= quantity,
            )
            .all()
        )
        session.close()
        return res

class MetalPrice(Base):
    __tablename__ = 'metal_price'
    id = Column(Integer, primary_key=True)
    buy_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)
    timestamp = Column(DateTime)
    session_id = Column(String(36), index=True)
    bullion_type = Column(String(2), nullable=True, index=True)

    @classmethod
    def get_previous_price(cls, bullion_type):
        """
        Fetches the metal price for the specified bullion type from the previous session.

        Args:
            session: SQLAlchemy session object.
            bullion_type: The type of bullion.

        Returns:
            The result of the query.
        """

        france_timezone = pytz.timezone('Europe/Paris')
        now_france = datetime.datetime.now(france_timezone)
        thirty_minutes_ago = now_france - datetime.timedelta(minutes=30)

        subquery = (
            session.query(cls.session_id)
            .group_by(cls.session_id)
            .having(func.max(cls.timestamp) < thirty_minutes_ago)
            .order_by(func.max(cls.timestamp).desc())
            .limit(1)
        ).subquery()

        query = (
            session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == subquery.c.session_id
            )
        )
        session.close()
        return query_to_dict(query.all())

class PrecalculatedOffer(Item):  # Inherit from Item Base
    __tablename__ = 'precalculated_offer'
    id = Column(Integer, primary_key=True)  # Own primary key
    timestamp = Column(DateTime)
    budget_min = Column(Float)
    budget_max = Column(Float)
    quantity = Column(Integer)
    bullion_type = Column(String(2))
    name = Column(String(255))
    source = Column(String(1024))
    premium = Column(Float)  # Assuming premium is a single float value
    price_per_coin = Column(Float)
    delivery_fees = Column(Float)
    total_cost = Column(Float)
    # Add a foreign key to the Item table
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship("Item")  # Establish the relationship

Base.metadata.create_all(engine)  # Add this line to create the tables

def pre_calculate_and_store_offers():
    """
    Pre-calculates offer data with standard values and stores it in the database.
    """

    # 1. Define standard values
    standard_budget_range = [0, 2000]
    standard_quantity = 3
    standard_bullion_type = 'or'
    standard_selected_coins = None

    # 2. Fetch the latest metal price
    results = session.query(MetalPrice).order_by(MetalPrice.timestamp.desc()).first()
    metal_price = results.buy_price
    session_id = results.session_id

    # 3. Fetch items from the database
    results = Item.get_items_by_bullion_type_and_quantity(standard_bullion_type, session_id, standard_quantity)
    items_df = pd.DataFrame(results).copy()


    # 4. Calculate cheapest offers
    cheapest_offers = []
    seen_offers = set()

    if standard_selected_coins:
        filtered_df = pd.DataFrame()
        for coin in standard_selected_coins:
            filtered_df = pd.concat([filtered_df, items_df[items_df['name'].str.contains(coin, regex=True)]])
        items_df = filtered_df

    items_df['buy_premiums'] = items_df['buy_premiums'].apply(lambda x: [float(i) for i in x.split(';')])

    budget_min, budget_max = standard_budget_range

    total_count = len(items_df)
    total_processed_count = 0

    for q_max in reversed(range(1, standard_quantity + 1)):
        if total_count <= total_processed_count:
            break
        df_copy = items_df.copy()

        def calculate_premiums(x, q_max):
            min_premium = min(x[:q_max])
            premium_index = x.index(min_premium)
            return pd.Series({'buy_premiums': min_premium, 'premium_index': premium_index})

        df_copy[['buy_premiums', 'premium_index']] = df_copy['buy_premiums'].apply(
            lambda x: calculate_premiums(x, q_max))

        results = df_copy.sort_values(by='buy_premiums')
        print('i')
        for i, row in results.iterrows():
            spot_cost = weights[row['name']] * metal_price
            total_quantity = row['quantity'] * int(row['premium_index'] + 1) if row['minimum'] == 1 else int(
                row['premium_index'] + 1) * standard_quantity
            total_cost = (spot_cost + (row['buy_premiums'] / 100.0) * spot_cost) * total_quantity
            if row['id'] not in seen_offers and budget_min <= total_cost <= budget_max and standard_quantity >= \
                    row['minimum']:
                ppc = (spot_cost + (row['buy_premiums'] / 100.0) * spot_cost)
                print(ppc,row['name'])
                cheapest_offers.append({
                    'name': row['name'].upper(),
                    'source': row['source'],
                    'premium': row['buy_premiums'],
                    'price_per_coin': f"{ppc:.2f} €",
                    'quantity': str(int(row['premium_index'] + 1)) if row['quantity'] == 1 and row[
                        'minimum'] == 1 else str(int(row['premium_index'] + 1)) + ' x ' + str(
                        row['quantity']) + ' ({total_quantity})'.format(
                        total_quantity=str(total_quantity)) if row['quantity'] > 1 else standard_quantity,
                    'delivery_fees': get_price(row['delivery_fees'], total_cost),
                    'total_cost': total_cost
                })
                seen_offers.add(row['id'])
                total_count += 1

    cheapest_offers.sort(key=lambda x: x['premium'])

    # Delete existing pre-calculated offers
    session.query(PrecalculatedOffer).delete()

    # Create PrecalculatedOffer entries
    for offer in cheapest_offers[:40]:
        print(offer)
        new_offer = PrecalculatedOffer(
            timestamp=datetime.datetime.now(),
            budget_min=standard_budget_range[0],
            budget_max=standard_budget_range[1],
            quantity=standard_quantity,
            bullion_type=standard_bullion_type,
            name=offer['name'],
            source=offer['source'],
            premium=offer['premium'],
            price_per_coin=offer['price_per_coin'],
            delivery_fees=offer['delivery_fees'],
            total_cost=offer['total_cost']
        )
        session.add(new_offer)
        session.commit()

if __name__ == "__main__":
    pre_calculate_and_store_offers()
    scheduler = BackgroundScheduler()
    scheduler.add_job(pre_calculate_and_store_offers, 'interval', minutes=10)
    scheduler.start()