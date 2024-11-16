from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz
import sshtunnel
from sqlalchemy import create_engine
import logging
sshtunnel.SSH_TIMEOUT = 30.0
sshtunnel.TUNNEL_TIMEOUT = 30.0
# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG for detailed output
sshtunnel.create_logger(loglevel=1)

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

class MetalPrice(Base):
    __tablename__ = 'metal_price'
    id = Column(Integer, primary_key=True)
    buy_price = Column(Float,nullable=True)
    sell_price = Column(Float,nullable=True)
    timestamp = Column(DateTime)
    session_id = Column(String(36), index=True)
    bullion_type = Column(String(2),nullable=True, index=True)


    # engine = create_engine(
    #     f"mysql+mysqlconnector://Pentagruel:(US)ue%251@127.0.0.1:{tunnel.local_bind_port}/Pentagruel$bullionsniper?connect_timeout=10"
    # )
    #
    # Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)