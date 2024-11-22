import os
import sshtunnel
import pytz
import datetime
import logging

from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

# Database connection details
SSH_HOST = os.environ['SSH_HOST']
SSH_USERNAME = os.environ['SSH_USERNAME']
SSH_PASSWORD = os.environ['SSH_PASSWORD']
REMOTE_BIND_ADDRESS = os.environ['REMOTE_BIND_ADDRESS']
REMOTE_PORT_ADDRESS = int(os.environ['REMOTE_PORT_ADDRESS'])
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

db = SQLAlchemy()
def create_session(app):
    """
    Establishes an SSH tunnel and creates a Flask-SQLAlchemy session.
    The tunnel needs to be closed manually after usage.

    Returns:
        A SQLAlchemy session object and the SSH tunnel object.
    """

    tunnel = sshtunnel.SSHTunnelForwarder(
        SSH_HOST,
        ssh_username=SSH_USERNAME,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(REMOTE_BIND_ADDRESS, REMOTE_PORT_ADDRESS),
        logger=None,
    )
    tunnel.start()

    # Use the existing SQLAlchemy instance to create a session
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI.format(tunnel.local_bind_port)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"connect_timeout": 60}, "echo": True}
    db.init_app(app)  # Initialize the SQLAlchemy instance with the app
    with app.app_context():
        session = db.session  # Get the session from the SQLAlchemy instance
        return session, tunnel

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
    def get_items_by_bullion_type_and_quantity(cls, session, bullion_type, session_id, quantity):
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
        return query_to_dict(
            session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == session_id,
                cls.minimum <= quantity,
                cls.quantity <= quantity,
            )
            .all()
        )


class MetalPrice(db.Model):
    __tablename__ = 'metal_price'
    id = db.Column(db.Integer, primary_key=True)
    buy_price = db.Column(db.Float, nullable=True)
    sell_price = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime)
    session_id = db.Column(db.String(36), index=True)
    bullion_type = db.Column(db.String(2), nullable=True, index=True)

    @classmethod
    def get_previous_price(cls, session, bullion_type):
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
            .having(db.func.max(cls.timestamp) < thirty_minutes_ago)
            .order_by(db.func.max(cls.timestamp).desc())
            .limit(1)
        ).subquery()

        query = (
            session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == subquery.c.session_id
            )
        )

        return query_to_dict(query.all())

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users',backref=db.backref('users', lazy='dynamic'))

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)