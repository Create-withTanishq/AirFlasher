from fastapi import FastAPI
from . routers import upload,firmware
from . import models
from . database import engine

app = FastAPI()
app.include_router(upload.router)
app.include_router(firmware.router)
models.Base.metadata.create_all(bind = engine)

@app.get("/")
def get_home():
    return {
        "message" : "Home"
    }