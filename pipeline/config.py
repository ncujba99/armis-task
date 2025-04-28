import os
import logging

from pymongo import MongoClient

mongo_client = MongoClient(
    host=os.getenv("DB_HOST"),
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

api_key = os.getenv("API_TOKEN")
crowdstrike_url = os.getenv("CROWDSTRIKE_URL")
