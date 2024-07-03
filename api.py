from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from grass import Grass
from prometheus import Prometheus

router = APIRouter()
grass = Grass()
prometheus = Prometheus()


@router.get("/metrics")
async def get_metrics():
    metrics = grass.get_metrics()
    prometheus.set_metrics(metrics)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.get("/status")
async def get_status():
    return grass.get_metrics()
