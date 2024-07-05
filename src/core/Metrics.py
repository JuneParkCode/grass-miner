from dataclasses import dataclass


@dataclass
class Metrics:
    node_name: str
    time_connected: float
    network_quality: float
    node_earnings: float
