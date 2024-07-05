from fastapi import FastAPI

from api import metric
from core.Grass import Grass
from core.Handler.GrassHandler import GrassHandler
from utils.Config import Config
from utils.Utility import Util

app = FastAPI()
app.include_router(metric.router)


@app.on_event("startup")
async def startup_event():
    try:
        config = Config()
        driver = Util.get_chrome_driver(config.crx_name)
        handler = GrassHandler(driver, config.extension_id)
        grass = Grass(handler, config.username, config.password)
        grass.run()
    except Exception as e:
        print(e)
        Util.shutdown()


@app.get("/")
async def get_root():
    return "grass-miner"
