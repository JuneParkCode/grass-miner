from typing import Optional

from core.Handler.Exception import HandlerException
from core.Handler.GrassHandler import GrassHandler
from core.Metrics import Metrics
from prometheus import Prometheus
from utils.Utility import Util


class Grass:
    # Singleton class
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self, handler: GrassHandler, username: str, password: str):
        self.handler: GrassHandler = handler
        self.username: str = username
        self.password: str = password
        self.metrics: Optional[Metrics] = None
        self.prometheus: Prometheus = Prometheus()

    @staticmethod
    def get_instance():
        if Grass.instance is None:
            raise RuntimeError("Grass is not initialized")
        return Grass.instance

    def run(self):
        try:
            self.handler.connect(self.username, self.password)
        except HandlerException as e:
            print(f"An error occurred during startup. : {e}")
            self.shutdown()

        if not self.__set_prometheus_metric():
            print(f"An error occurred while setting up Prometheus")
            self.shutdown()

    def shutdown(self):
        self.handler.quit()
        Util.shutdown()

    def get_metrics(self) -> Metrics:
        self.metrics = self.handler.get_metrics() or self.metrics
        return self.metrics

    def __set_prometheus_metric(self):
        # get node table
        self.metrics = self.handler.get_metrics()
        if self.metrics is None:
            return False

        self.prometheus.init(self.metrics.node_name)
        return True
