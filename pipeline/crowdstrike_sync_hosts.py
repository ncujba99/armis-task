from config import mongo_client
from crowdstrike.client import CrowdStrikeClient


collection = mongo_client["dev"]["hosts"]

crowdstrike_client = CrowdStrikeClient()

# Iterate over the CrowdStrike client and update the MongoDB collection
for host in crowdstrike_client.scroll_hosts():
    collection.update_one(
        filter={
            "$or": [
                {"crowdstrike.id": host.id},
                {"aws_instance_id": host.instance_id}
            ]
        },
        update={
            "$set": {
                "aws_instance_id":host.instance_id,
                "crowdstrike":{
                    "id":host.id,
                    "first_seen": host.first_seen,
                    "last_seen": host.last_seen,
                    "modified": host.modified_timestamp.date,
                    "tags": host.tags,
                },
                "external_ip": host.external_ip,
                "mac_address": host.mac_address,
                "hostname": host.hostname,
                "device_id": host.device_id,
                "cid": host.cid,
                "agent_version": host.agent_version,
                "os_version": host.os_version,
                "platform_name": host.platform_name,
                "cpu_signature": host.cpu_signature,
                "policies": [policy.model_dump() for policy in host.policies],
                
            }
        },
        upsert=True
    )
