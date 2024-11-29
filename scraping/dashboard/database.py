import pytz
import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True, index=True)
    price_ranges = db.Column(db.String(255), nullable=True)
    sell = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    minimum = db.Column(db.Integer, nullable=True)
    buy_premiums = db.Column(db.String(2000), nullable=True)
    delivery_fees = db.Column(db.String(255), nullable=True)
    source = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.DateTime)
    session_id = db.Column(db.String(36), index=True)
    bullion_type = db.Column(db.String(2), nullable=True, index=False)

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
        db.session = db.session_factory()
        query_to_dict(
            db.session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == session_id,
                cls.minimum <= quantity,
                cls.quantity <= quantity,
            )
            .all()
        )
        db.session.close()
        return


class MetalPrice(db.Model):
    __tablename__ = 'metal_price'
    id = db.Column(db.Integer, primary_key=True)
    buy_price = db.Column(db.Float, nullable=True)
    sell_price = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime)
    session_id = db.Column(db.String(36), index=True)
    bullion_type = db.Column(db.String(2), nullable=True, index=True)

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
        db.session = db.session_factory()
        subquery = (
            db.session.query(cls.session_id)
            .group_by(cls.session_id)
            .having(db.func.max(cls.timestamp) < thirty_minutes_ago)
            .order_by(db.func.max(cls.timestamp).desc())
            .limit(1)
        ).subquery()

        query = (
            db.session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == subquery.c.session_id
            )
        )
        db.session.close()
        return query_to_dict(query.all())

class UserChoice(db.Model):
    __tablename__ = 'user_choices'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    bullion_type = db.Column(db.String(2))
    selected_coins = db.Column(db.JSON)  # Store selected coins as JSON