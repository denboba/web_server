""""The initializer module for the webserver. """
import os
import logging
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

if not os.path.exists('results'):
    os.mkdir('results')

webserver = Flask(__name__)
logging.basicConfig(
    filename='webserver.log',
    filemode='w',  # Append mode
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s '
           '(LINE:%(lineno)d) FILE:%(filename)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z',
    level=logging.DEBUG
)

logger = logging.getLogger('webserver')

webserver.tasks_runner = ThreadPool()
logger.info('Thread pool initialized')
LOCAL_FILE = "./nutrition_activity_obesity_usa_subset.csv"
FALLBACK_FILE = "../nutrition_activity_obesity_usa_subset.csv"

if os.path.exists(LOCAL_FILE):
    webserver.data_ingestor = DataIngestor(LOCAL_FILE)
else:
    webserver.data_ingestor = DataIngestor(FALLBACK_FILE)
logger.info('Data ingestor initialized')

webserver.job_counter = 1

from app import routes
