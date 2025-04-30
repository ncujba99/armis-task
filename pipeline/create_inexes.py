from pymongo import ASCENDING

from config import mongo_client, logger


collection = mongo_client["dev"]["hosts"]


indexes = [
    {
        "fields": [("crowdstrike.id", ASCENDING)],
        "kwargs": {"name": "idx_crowdstrike_id", "unique": True, "sparse": True},
    },
    {
        "fields": [("qualys.id", ASCENDING)],
        "kwargs": {"name": "idx_qualys_id", "unique": True, "sparse": True},
    },
    {
        "fields": [("aws_instance_id", ASCENDING)],
        "kwargs": {"name": "idx_aws_instance_id", "unique": True, "sparse": True},
    },
]

for index in indexes:
    collection.create_index(index["fields"], **index["kwargs"])

logger.info("Indexes created successfully.")
