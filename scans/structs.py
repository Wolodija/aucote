from utils.database import DbObject
from enum import Enum

class Node:
    name = None
    ip = None
    id = None

class TransportProtocol(Enum):
    TCP = 'TCP',
    UDP = 'UDP',
    ICMP = 'ICMP'

    @classmethod
    def from_nmap_name(cls, name):
        return cls((name.upper(),))

class RiskLevel(Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class Port(DbObject):
    TABLE = 'ports'
    def __init__(self):
        self.vulnerabilities = []

    node = None
    number = None
    transport_protocol = None
    service_name = None
    service_version = None
    banner = None

class Vulnerability(DbObject):
    title = None
    description = None
    risk_level = None
    port = None



