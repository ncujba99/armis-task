from config import mongo_client
from qualys.cleint import QualysClient


collection = mongo_client["dev"]["hosts"]

qualys_client = QualysClient()

# Iterate over the Qualys client and update the MongoDB collection
for host in qualys_client.scroll_hosts():

    ec2_asset = None
    for source_info in reversed(host.sourceInfo.list):
        value = source_info.model_dump().get("ec2_asset_source_simple")
        if value is not None:
            ec2_asset = value
            break

    collection.update_one(
        filter={
            "$or": [
                {"qualys.id": host.id},
                {"aws_instance_id": ec2_asset.get("instanceId")}
            ]
        },
        update={
            "$set": {
                "hostname": host.dnsHostName,
                "aws_instance_id": ec2_asset.get("instanceId"),
                "agent_version": host.agentInfo.model_dump(),
                "os_version": host.os,
                "cloud_provider": host.cloudProvider,
                "qualys":{
                    "id": host.id,
                    "first_seen": host.created,
                    "last_seen": host.modified,
                    "modified": host.modified,
                    "tags": [tag.TagSimple.name for tag in host.tags.list],
                },
                "network_interface":[interface.model_dump() for interface in host.networkInterface.list],
                "open_ports": [port.HostAssetOpenPort.model_dump() for port in host.openPort.list],
                "software": [software.HostAssetSoftware.model_dump() for software in host.software.list],
                "vulns": [vuln.HostAssetVuln.model_dump() for vuln in host.vuln.list],
                "ec2_asset": ec2_asset
            }
        },
        upsert=True
    )