from typing import List, Optional, Dict, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class HostAssetAccount(BaseModel):
    username: str


class Account(BaseModel):
    HostAssetAccount: HostAssetAccount


class AccountList(BaseModel):
    list: List[Account]


class ManifestVersion(BaseModel):
    sca: str
    vm: str


class ActivationKey(BaseModel):
    title: str
    activationId: str


class AgentConfiguration(BaseModel):
    id: int
    name: str


class AgentInfo(BaseModel):
    location: str
    locationGeoLatitude: str
    lastCheckedIn: Dict[str, datetime]
    locationGeoLongtitude: str
    agentVersion: str
    manifestVersion: ManifestVersion
    activatedModule: str
    activationKey: ActivationKey
    agentConfiguration: AgentConfiguration
    status: str
    chirpStatus: str
    connectedFrom: str
    agentId: str
    platform: str


class HostAssetInterface(BaseModel):
    interfaceName: Optional[str] = None
    macAddress: Optional[str] = None
    gatewayAddress: Optional[str] = None
    address: str
    hostname: str


class NetworkInterface(BaseModel):
    HostAssetInterface: HostAssetInterface


class NetworkInterfaceList(BaseModel):
    list: List[NetworkInterface]


class HostAssetOpenPort(BaseModel):
    serviceName: Optional[str] = None
    protocol: str
    port: int


class OpenPort(BaseModel):
    HostAssetOpenPort: HostAssetOpenPort


class OpenPortList(BaseModel):
    list: List[OpenPort]


class HostAssetProcessor(BaseModel):
    name: str
    speed: int


class Processor(BaseModel):
    HostAssetProcessor: HostAssetProcessor


class ProcessorList(BaseModel):
    list: List[Processor]


class HostAssetSoftware(BaseModel):
    name: str
    version: str


class Software(BaseModel):
    HostAssetSoftware: HostAssetSoftware


class SoftwareList(BaseModel):
    list: List[Software]


class TagSimple(BaseModel):
    id: int
    name: str


class Tag(BaseModel):
    TagSimple: TagSimple


class TagList(BaseModel):
    list: List[Tag]


class TagsList(BaseModel):
    tags: TagList


class Ec2AssetSourceSimpleModel(BaseModel):
    instanceType: str
    subnetId: str
    imageId: str
    groupName: str
    accountId: str
    macAddress: str
    reservationId: str
    instanceId: str
    monitoringEnabled: str
    spotInstance: str
    zone: str
    instanceState: str
    privateDnsName: str
    vpcId: str
    type: str
    availabilityZone: str
    privateIpAddress: str
    firstDiscovered: datetime
    ec2InstanceTags: TagsList
    publicIpAddress: str
    lastUpdated: datetime
    region: str
    assetId: int
    groupId: Optional[str]=None
    localHostname: str
    publicDnsName: str


class AssetSourceModel(BaseModel):
    pass  # Placeholder for any additional fields later


class SourceInfoModel(BaseModel):
    ec2_asset_source_simple: Optional[Ec2AssetSourceSimpleModel] = Field(default=None, alias="Ec2AssetSourceSimple")
    asset_source: Optional[AssetSourceModel] = Field(default=None, alias="AssetSource")


class SourceInfoList(BaseModel):
    list: List[SourceInfoModel]


class HostAssetVuln(BaseModel):
    hostInstanceVulnId: Union[int, Dict[str, str]]
    lastFound: datetime
    firstFound: datetime
    qid: int


class Vuln(BaseModel):
    HostAssetVuln: HostAssetVuln


class VulnList(BaseModel):
    list: List[Vuln]

    @field_validator("list")
    @classmethod
    def normalize_vuln_ids(cls, v):
        for item in v:
            vuln_id = item.HostAssetVuln.hostInstanceVulnId
            if isinstance(vuln_id, dict):
                item.HostAssetVuln.hostInstanceVulnId = int(vuln_id.get("$numberLong", 0))
        return v


class HostAssetVolume(BaseModel):
    free: Union[int, Dict[str, str]]
    name: str
    size: Union[int, Dict[str, str]]


class Volume(BaseModel):
    HostAssetVolume: HostAssetVolume


class VolumeList(BaseModel):
    list: List[Volume]

    @field_validator("list")
    @classmethod
    def normalize_volume_sizes(cls, v):
        for item in v:
            volume = item.HostAssetVolume
            if isinstance(volume.free, dict):
                volume.free = int(volume.free.get("$numberLong", 0))
            if isinstance(volume.size, dict):
                volume.size = int(volume.size.get("$numberLong", 0))
        return v


class LastVulnScan(BaseModel):
    date: datetime = Field(..., alias="$date")

class HostItem(BaseModel):

    id: int
    account: AccountList
    address: str
    agentInfo: AgentInfo
    biosDescription: str
    cloudProvider: str
    created: datetime
    dnsHostName: str
    fqdn: str
    isDockerHost: str
    lastComplianceScan: datetime
    lastLoggedOnUser: Optional[str] = None
    lastSystemBoot: datetime
    lastVulnScan: LastVulnScan
    manufacturer: str
    model: str
    modified: datetime
    name: str
    networkGuid: str
    networkInterface: NetworkInterfaceList
    openPort: OpenPortList
    os: str
    processor: ProcessorList
    qwebHostId: int
    software: SoftwareList
    sourceInfo: SourceInfoList
    tags: TagList
    timezone: str
    totalMemory: int
    trackingMethod: str
    type: str
    volume: VolumeList
    vuln: VulnList
