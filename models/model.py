from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import sshtunnel
import pytz
import datetime
from sqlalchemy import create_engine
import logging
sshtunnel.SSH_TIMEOUT = 30.0
sshtunnel.TUNNEL_TIMEOUT = 30.0
# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG for detailed output
sshtunnel.create_logger(loglevel=1)
from flask_login import UserMixin




# with sshtunnel.SSHTunnelForwarder(
#     ('ssh.pythonanywhere.com',22),
#     ssh_username='Pentagruel',
#     ssh_password='(US)ue%1',
#     remote_bind_address=('Pentagruel.mysql.pythonanywhere-services.com', 3306)
# ) as tunnel:


Base = declarative_base()
class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True, index=True)
    price_ranges = Column(String(255), nullable=True)
    sell = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    minimum = Column(Integer, nullable=True)
    buy_premiums = Column(String(2000), nullable=True)
    delivery_fees = Column(String(255), nullable=True)
    source = Column(String(1024),nullable=False)
    timestamp = Column(DateTime)
    session_id = Column(String(36), index=True)
    bullion_type = Column(String(2),nullable=True, index=False)

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
        return (
            session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == session_id,
                cls.minimum <= quantity,
                cls.quantity <= quantity,
            )
            .all()
        )

class MetalPrice(Base):
    __tablename__ = 'metal_price'
    id = Column(Integer, primary_key=True)
    buy_price = Column(Float,nullable=True)
    sell_price = Column(Float,nullable=True)
    timestamp = Column(DateTime)
    session_id = Column(String(36), index=True)
    bullion_type = Column(String(2),nullable=True, index=True)

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

        return query.all()

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True,nullable=False)
    password = Column(String(255), nullable=False)
    def __repr__(self):  # Add a __repr__ method
        return f"<User(id={self.id}, username='{self.username}')>"

    @classmethod
    def get_user_by_username(cls, session, username):
        """
        Fetches a user from the database by their username, case-insensitively.

        Args:
            session: SQLAlchemy session object.
            username: The username of the user to fetch.

        Returns:
            The User object if found, otherwise None.
        """
        return session.query(cls).filter(func.lower(cls.username) == func.lower(cls.username) == func.lower(username)).first()
    # engine = create_engine(
    #     f"mysql+mysqlconnector://Pentagruel:(US)ue%251@127.0.0.1:{tunnel.local_bind_port}/Pentagruel$staging-bullionsniper?connect_timeout=10"
    # )
    #
    # Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)