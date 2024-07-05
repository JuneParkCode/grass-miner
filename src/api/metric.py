from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from core.Grass import Grass
from prometheus import Prometheus

router = APIRouter()


@router.get("/metrics")
async def get_metrics():
    grass = Grass.get_instance()
    prometheus = Prometheus.get_instance()
    metrics = grass.get_metrics()
    prometheus.set_metrics(metrics)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.get("/status")
async def get_status():
    grass = Grass.get_instance()
    return grass.get_metrics()
