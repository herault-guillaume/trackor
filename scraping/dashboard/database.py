import sshtunnel
import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        remote_bind_address=REMOTE_BIND_ADDRESS,
        logger=None,
    )
    tunnel.start()  # Démarrer le tunnel manuellement

    engine = create_engine(DATABASE_URL.format(tunnel.local_bind_port), connect_args={"connect_timeout": 60})
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, tunnel

sshtunnel.SSH_TIMEOUT = 3600.0
sshtunnel.TUNNEL_TIMEOUT = 3600.0

# Database connection details
SSH_HOST = "ssh.pythonanywhere.com"
SSH_USERNAME = "Pentagruel"
SSH_PASSWORD = "(US)ue%1"
REMOTE_BIND_ADDRESS = ("pentagruel.mysql.pythonanywhere-services.com", 3306)
DATABASE_URL = "mysql+mysqlconnector://Pentagruel:(US)ue%1@127.0.0.1:{}/Pentagruel$staging-bullionsniper"