from fastapi import FastAPI

from .core import models
from .core.database import engine
from .routers import sites

app = FastAPI()
app.include_router(sites.router)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    pass
