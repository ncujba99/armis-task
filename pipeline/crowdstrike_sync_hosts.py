from config import mongo_client
from services.crowdstrike import scroll_hosts


for host in scroll_hosts():
    mongo_client["test"]["crowdstrike"].insert_one(host)