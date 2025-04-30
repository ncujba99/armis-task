from config import mongo_client, api_key, qualys_url
from qualys.cleint import QualysClient


def sync_qualys_hosts():
    collection = mongo_client["dev"]["hosts"]
    qualys_client = QualysClient(api_key=api_key, url=qualys_url)

    for host in qualys_client.scroll_hosts():
        ec2_asset = {}
        for source_info in reversed(host.sourceInfo.list):
            value = source_info.model_dump().get("ec2_asset_source_simple")
            if value is not None:
                ec2_asset = value
                break
        aws_instance_id = ec2_asset.get("instanceId")

        filter_conditions = [{"qualys.id": host.id}]
        if aws_instance_id:
            filter_conditions.append({"aws_instance_id": aws_instance_id})

        collection.update_one(
            filter={"$or": filter_conditions},
            update={
                "$set": {
                    "aws_instance_id": aws_instance_id,
                    "hostname": host.dnsHostName,
                    "os_version": host.os,
                    "qualys": {
                        "id": host.id,
                        "first_seen": host.created,
                        "modified": host.modified,
                        "address": host.address,
                        "fqdn": host.fqdn,
                        "name": host.name,
                        "network_guid": host.networkGuid,
                        "cloud_provider": host.cloudProvider,
                        "bios_description": host.biosDescription,
                        "is_docker_host": host.isDockerHost,
                        "last_compliance_scan": host.lastComplianceScan,
                        "last_logged_on_user": host.lastLoggedOnUser,
                        "last_system_boot": host.lastSystemBoot,
                        "last_vuln_scan": host.lastVulnScan.date,
                        "manufacturer": host.manufacturer,
                        "model": host.model,
                        "timezone": host.timezone,
                        "total_memory": host.totalMemory,
                        "tracking_method": host.trackingMethod,
                        "type": host.type,
                        "qweb_host_id": host.qwebHostId,
                        "os_version": host.os,
                        "agent_info": host.agentInfo.model_dump(),
                        "network_interface": [interface.model_dump().get("HostAssetInterface") for interface in host.networkInterface.list],
                        "open_ports": [port.model_dump().get("HostAssetOpenPort") for port in host.openPort.list],
                        "processor": [processor.model_dump().get("HostAssetProcessor") for processor in host.processor.list],
                        "software": [software.model_dump().get("HostAssetSoftware") for software in host.software.list],
                        "volumes": [volume.model_dump().get("HostAssetVolume") for volume in host.volume.list],
                        "vulns": [vuln.model_dump().get("HostAssetVuln") for vuln in host.vuln.list],
                        "ec2_asset": ec2_asset,
                        "accounts": [account.model_dump().get("HostAssetAccount") for account in host.account.list],
                        "tags": [tag.TagSimple.name for tag in host.tags.list],
                    }
                }
            },
            upsert=True
        )


if __name__ == "__main__":
    sync_qualys_hosts()
