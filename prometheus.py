from prometheus_client import Gauge


class Prometheus:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.prometheus_node_name: str = ""
        self.prometheus_node_ip: str = ""
        self.prometheus_network_quality: Gauge = None
        self.prometheus_node_earnings: Gauge = None
        self.prometheus_time_connected: Gauge = None

    def init(self, node_name, ip):
        self.prometheus_node_name = node_name
        self.prometheus_node_ip = ip
        self.prometheus_network_quality = Gauge('grass_network_quality', 'Grass node network quality metrics',
                                                labelnames=["node_name", "ip"])
        self.prometheus_node_earnings = Gauge('grass_node_earnings', 'Grass node earnings metrics',
                                              labelnames=["node_name", "ip"])
        self.prometheus_time_connected = Gauge('grass_time_connected', 'Grass node time connected metrics',
                                               labelnames=["node_name", "ip"])

    def set_metrics(self, metrics):
        self.prometheus_network_quality.labels(node_name=self.prometheus_node_name, ip=self.prometheus_node_ip).set(
            metrics["network_quality"])
        self.prometheus_node_earnings.labels(node_name=self.prometheus_node_name, ip=self.prometheus_node_ip).set(
            metrics["node_earnings"])
        self.prometheus_time_connected.labels(node_name=self.prometheus_node_name, ip=self.prometheus_node_ip).set(
            metrics["time_connected"])
