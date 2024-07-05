from prometheus_client import Gauge

from core.Metrics import Metrics


class Prometheus:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.prometheus_node_name: str = ""
        self.prometheus_network_quality: Gauge = Gauge('grass_network_quality', 'Grass node network quality metrics',
                                                       labelnames=["node_name"])
        self.prometheus_node_earnings: Gauge = Gauge('grass_node_earnings', 'Grass node earnings metrics',
                                                     labelnames=["node_name"])
        self.prometheus_time_connected: Gauge = Gauge('grass_time_connected', 'Grass node time connected metrics',
                                                      labelnames=["node_name"])

    @staticmethod
    def get_instance():
        if Prometheus.instance is None:
            raise RuntimeError("Prometheus has not been initialized")
        return Prometheus.instance

    def init(self, node_name):
        self.prometheus_node_name = node_name

    def set_metrics(self, metrics: Metrics):
        self.prometheus_network_quality.labels(node_name=self.prometheus_node_name).set(
            metrics.network_quality)
        self.prometheus_node_earnings.labels(node_name=self.prometheus_node_name).set(
            metrics.node_earnings)
        self.prometheus_time_connected.labels(node_name=self.prometheus_node_name).set(
            metrics.time_connected)
