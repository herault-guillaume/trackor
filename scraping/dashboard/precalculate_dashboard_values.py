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
from scipy.optimize import minimize

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


# Objective function (negative number of coins to minimize)
def objective_function(x):
    return -x[0]  # Access the first element of the array x

def constraint(x, budget, price_ranges, delivery_fee_ranges):

    price_per_coin_ = lambda x: get_price(price_ranges, x)
    delivery_fees_ = lambda x: get_price(delivery_fee_ranges, x * price_per_coin_(x))

    price = price_per_coin_(x[0])

    delivery_fee = delivery_fees_(x[0])  # Calculate delivery_fee only after checking price

    if delivery_fee is None:
        return 0  # Return 0 if delivery_fee is None

    return budget - (x[0] * price + delivery_fee)

# Function to find the maximum coins
def find_max_coins(max_quantity, max_budget, price_ranges, delivery_fee_ranges,minimum):
    # Initial guess for x (can be improved)
    x0 = pd.Series(max([1,minimum]))

    constraint_dict = [
        {'type': 'ineq', 'fun': lambda x: constraint(x, max_budget, price_ranges, delivery_fee_ranges)},
    ]
    # Perform numerical optimization using minimize
    result = minimize(
        objective_function,
        x0,
        bounds=[(minimum, max_quantity)],  # Set the lower bound to the minimum
        constraints=constraint_dict,
        method='SLSQP'
    )

    max_coins = int(round(result.x[0]))  # Access the solution from result.x[0]
    return max_coins

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

class PrecalculatedOffer(Base):  # Inherit from Item Base
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

Base.metadata.create_all(engine)  # Add this line to create the tables


def pre_calculate_and_store_offers():
    """
    Pre-calculates offer data with standard values and stores it in the database.
    """

    # 1. Define standard values
    standard_budget_range = [0, 2000]
    standard_quantity = 2000
    standard_bullion_type = 'or'
    standard_selected_coins = None

    france_timezone = pytz.timezone('Europe/Paris')
    now_france = datetime.datetime.now(france_timezone)
    thirty_minutes_ago = now_france - datetime.timedelta(minutes=30)

    # 2. Fetch the latest metal price
    results = MetalPrice.get_previous_price(standard_bullion_type)
    metal_prices_df = pd.DataFrame(results)

    metal_price = metal_prices_df['buy_price'].iloc[0]
    session_id = metal_prices_df['session_id'].iloc[0]
    latest_timestamp = metal_prices_df['timestamp'].iloc[0]
    formatted_timestamp = latest_timestamp.strftime('%d/%m/%Y à %Hh%M.')

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

    budget_min, budget_max = standard_budget_range

    for i, row in items_df.iterrows():

        total_quantity = find_max_coins(standard_quantity, budget_max, row['price_ranges'], row['delivery_fees'], row['minimum'])

        # obligé de retirer les offres inferieur a la quantité, le solveur doit pouvoir descendre en dessous du minimum de pièce pour calculer.
        if total_quantity < row['minimum']:
            continue

        price_per_coin = get_price(row['price_ranges'], total_quantity) / row['quantity']
        delivery_cost = get_price(row['delivery_fees'], total_quantity)
        ppc_ipc = price_per_coin + (delivery_cost / total_quantity)
        spot_cost = weights[row['name']] * metal_price
        premium = ppc_ipc - spot_cost
        premium_percentage = (premium / spot_cost) * 100
        total_cost = ppc_ipc * total_quantity * row['quantity']

        if total_cost > budget_max or total_quantity > standard_quantity:
            continue

        cheapest_offers.append({
            'name': row['name'].upper(),
            'source': row['source'],
            'premium': premium_percentage,
            'price_per_coin': ppc_ipc,
            'quantity': total_quantity if row['quantity'] == 1 else str(total_quantity) + ' x ' + str(
                row['quantity']) + ' ({total_quantity})'.format(total_quantity=str(total_quantity * row['quantity'])),
            'delivery_fees': 0 if get_price(row['delivery_fees'], total_cost) == 0.01 else get_price(
                row['delivery_fees'], total_cost),
            'total_cost': total_cost
        })

    cheapest_offers.sort(key=lambda x: x['premium'])

    # Delete existing pre-calculated offers
    session.query(PrecalculatedOffer).delete()

    # Create PrecalculatedOffer entries
    for offer in cheapest_offers[:40]:
        france_timezone = pytz.timezone('Europe/Paris')
        now_france = datetime.datetime.now(france_timezone)
        new_offer = PrecalculatedOffer(
            timestamp=now_france,
            budget_min=standard_budget_range[0],
            budget_max=standard_budget_range[1],
            quantity=offer['quantity'],
            bullion_type=standard_bullion_type,
            name=offer['name'],
            source=offer['source'],
            premium=float(offer['premium']),
            price_per_coin=offer['price_per_coin'],
            delivery_fees=offer['delivery_fees'],
            total_cost=offer['total_cost']
        )
        session.add(new_offer)
        session.commit()

if __name__ == "__main__":
    pre_calculate_and_store_offers()
    scheduler = BackgroundScheduler()
    scheduler.add_job(pre_calculate_and_store_offers, 'interval', minutes=5)
    scheduler.start()