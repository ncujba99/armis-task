from typing import Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Policy(BaseModel):
    policy_type: str
    policy_id: str
    applied: bool
    settings_hash: str
    assigned_date: datetime
    applied_date: datetime
    rule_groups: Optional[List[Any]] = []
    uninstall_protection: Optional[str] = None


class DevicePolicies(BaseModel):
    prevention: Optional[Policy] = None
    sensor_update: Optional[Policy] = None
    global_config: Optional[Policy] = None
    remote_response: Optional[Policy] = None

    class Config:
        extra = "allow"


class Meta(BaseModel):
    version: str
    version_string: str


class ModifiedTimestamp(BaseModel):
    date: datetime = Field(..., alias="$date")


class HostItem(BaseModel):

    id: str = Field(..., alias="_id")
    device_id: str
    cid: str
    agent_load_flags: str
    agent_local_time: datetime
    agent_version: str
    bios_manufacturer: Optional[str] = None
    bios_version: Optional[str] = None
    config_id_base: str
    config_id_build: str
    config_id_platform: str
    cpu_signature: str
    external_ip: str
    mac_address: str
    instance_id: Optional[str] = None
    service_provider: Optional[str] = None
    service_provider_account_id: Optional[str] = None
    hostname: str
    first_seen: datetime
    last_seen: datetime
    local_ip: str
    major_version: str
    minor_version: str
    os_version: str
    platform_id: str
    platform_name: str
    policies: List[Policy]
    reduced_functionality_mode: str
    device_policies: DevicePolicies
    groups: List[str]
    group_hash: str
    product_type_desc: str
    provision_status: str
    serial_number: str
    status: str
    system_manufacturer: str
    system_product_name: str
    tags: List[str]
    modified_timestamp: ModifiedTimestamp
    meta: Meta
    zone_group: Optional[str] = None
    kernel_version: str
    connection_ip: Optional[str] = None
    default_gateway_ip: Optional[str] = None
    connection_mac_address: Optional[str] = None
    chassis_type: Optional[str] = None
    chassis_type_desc: Optional[str] = None
