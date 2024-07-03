from fastapi import FastAPI

import api
from grass import Grass

grass = Grass()
grass.start()

app = FastAPI()
app.include_router(api.router)
