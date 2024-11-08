# logging_config.py
import logging

def setup_logging():
    logging.basicConfig(
        filename='_scraping_logs.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )