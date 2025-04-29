from typing import List, Optional, Union, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class HostAssetAccount(BaseModel):
    username: str


class Account(BaseModel):
    HostAssetAccount: HostAssetAccount


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
    lastCheckedIn: Dict[str, datetime]
    agentVersion: str
    manifestVersion: ManifestVersion
    activatedModule: str
    activationKey: ActivationKey
    agentConfiguration: AgentConfiguration
    status: str
    connectedFrom: str
    agentId: str
    platform: str


class HostAssetInterface(BaseModel):
    address: str
    hostname: str


class NetworkInterface(BaseModel):
    HostAssetInterface: HostAssetInterface


class HostAssetOpenPort(BaseModel):
    protocol: str
    port: int


class HostAssetProcessor(BaseModel):
    name: str
    speed: int


class HostAssetSoftware(BaseModel):
    name: str
    version: str


class TagSimple(BaseModel):
    id: int
    name: str


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
    publicIpAddress: str
    lastUpdated: datetime
    region: str
    assetId: int
    localHostname: str
    publicDnsName: str


class HostAssetVuln(BaseModel):
    hostInstanceVulnId: Union[int, Dict[str, str]]
    lastFound: datetime
    firstFound: datetime
    qid: int


class HostAssetVolume(BaseModel):
    free: Union[int, Dict[str, str]]
    name: str
    size: Union[int, Dict[str, str]]


class HostItem(BaseModel):
    _id: int
    account: List[Account]
    address: str
    agentInfo: AgentInfo
    cloudProvider: str
    created: datetime
    dnsHostName: str
    fqdn: str
    id: int
    isDockerHost: str
    lastComplianceScan: datetime
    lastSystemBoot: datetime
    manufacturer: str
    model: str
    modified: datetime
    name: str
    networkGuid: str
    networkInterface: List[NetworkInterface]
    openPort: List[HostAssetOpenPort]
    os: str
    processor: List[HostAssetProcessor]
    qwebHostId: int
    software: List[HostAssetSoftware]
    sourceInfo: List[Ec2AssetSourceSimpleModel]
    tags: List[TagSimple]
    timezone: str
    totalMemory: int
    trackingMethod: str
    type: str
    volume: List[HostAssetVolume]
    vuln: List[HostAssetVuln]
