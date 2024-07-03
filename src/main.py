from fastapi import FastAPI

import api
from grass import Grass

app = FastAPI()
app.include_router(api.router)


@app.on_event("startup")
async def startup_event():
    grass = Grass()
    grass.start()
