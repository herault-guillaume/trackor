import sshtunnel
import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def create_session():
    """
    Establishes an SSH tunnel and creates a SQLAlchemy session.
    The tunnel needs to be closed manually after usage.

    Returns:
        A SQLAlchemy session object and the SSH tunnel object.
    """

    tunnel = sshtunnel.SSHTunnelForwarder(
        SSH_HOST,
        ssh_username=SSH_USERNAME,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(REMOTE_BIND_ADDRESS,REMOTE_PORT_ADDRESS),
    )
    tunnel.start()  # Démarrer le tunnel manuellement

    engine = create_engine(DATABASE_URL.format(tunnel.local_bind_port), connect_args={"connect_timeout": 60},echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, tunnel

sshtunnel.SSH_TIMEOUT = float(os.environ['SSH_TIMEOUT'])
sshtunnel.TUNNEL_TIMEOUT = float(os.environ['TUNNEL_TIMEOUT'])

# Database connection details
SSH_HOST = os.environ['SSH_HOST']
SSH_USERNAME = os.environ['SSH_USERNAME']
SSH_PASSWORD = os.environ['SSH_PASSWORD']
REMOTE_BIND_ADDRESS = os.environ['REMOTE_BIND_ADDRESS']
REMOTE_PORT_ADDRESS = int(os.environ['REMOTE_PORT_ADDRESS'])
DATABASE_URL = os.environ['DATABASE_URL']