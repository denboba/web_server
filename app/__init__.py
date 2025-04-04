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
local_file = "./nutrition_activity_obesity_usa_subset.csv"
fallback_file = "../nutrition_activity_obesity_usa_subset.csv"
# webserver.task_runner.start()

if os.path.exists(local_file):
    webserver.data_ingestor = DataIngestor(local_file)
else:
    webserver.data_ingestor = DataIngestor(fallback_file)
logger.info('Data ingestor initialized')

webserver.job_counter = 1

from app import routes
