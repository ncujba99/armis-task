from config import mongo_client, api_key, crowdstrike_url
from crowdstrike.client import CrowdStrikeClient


def sync_crowdstrike_hosts():
    collection = mongo_client["dev"]["hosts"]
    crowdstrike_client = CrowdStrikeClient(api_key=api_key, url=crowdstrike_url)

    for host in crowdstrike_client.scroll_hosts():
        collection.update_one(
            filter={
                "$or": [
                    {"crowdstrike.id": host.id},
                    {"aws_instance_id": host.instance_id},
                ]
            },
            update={
                "$set": {
                    "aws_instance_id": host.instance_id,
                    "hostname": host.hostname,
                    "crowdstrike": {
                        "id": host.id,
                        "first_seen": host.first_seen,
                        "last_seen": host.last_seen,
                        "modified": host.modified_timestamp.date,
                        "tags": host.tags,
                        "groups": host.groups,
                        "device_id": host.device_id,
                        "cid": host.cid,
                        "agent_load_flags": host.agent_load_flags,
                        "agent_local_time": host.agent_local_time,
                        "agent_version": host.agent_version,
                        "bios_manufacturer": host.bios_manufacturer,
                        "bios_version": host.bios_version,
                        "config_id_base": host.config_id_base,
                        "config_id_build": host.config_id_build,
                        "config_id_platform": host.config_id_platform,
                        "cpu_signature": host.cpu_signature,
                        "external_ip": host.external_ip,
                        "mac_address": host.mac_address,
                        "service_provider": host.service_provider,
                        "service_provider_account_id": host.service_provider_account_id,
                        "local_ip": host.local_ip,
                        "major_version": host.major_version,
                        "minor_version": host.minor_version,
                        "os_version": host.os_version,
                        "platform_id": host.platform_id,
                        "platform_name": host.platform_name,
                        "policies": [policy.model_dump() for policy in host.policies],
                        "reduced_functionality_mode": host.reduced_functionality_mode,
                        "device_policies": host.device_policies.model_dump(),
                        "group_hash": host.group_hash,
                        "product_type_desc": host.product_type_desc,
                        "provision_status": host.provision_status,
                        "serial_number": host.serial_number,
                        "status": host.status,
                        "system_manufacturer": host.system_manufacturer,
                        "system_product_name": host.system_product_name,
                        "meta": host.meta.model_dump(),
                        "zone_group": host.zone_group,
                        "kernel_version": host.kernel_version,
                        "connection_ip": host.connection_ip,
                        "default_gateway_ip": host.default_gateway_ip,
                        "connection_mac_address": host.connection_mac_address,
                        "chassis_type": host.chassis_type,
                        "chassis_type_desc": host.chassis_type_desc,
                    },
                }
            },
            upsert=True,
        )


if __name__ == "__main__":
    sync_crowdstrike_hosts()
