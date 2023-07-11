from fastapi import FastAPI

from app import database
from app.routers import routers
from app.helpers.asynchronous import async_wrap
from app.middlewares.cors import apply_cors
from app.settings import AppSettings

app = FastAPI(title="Clustering")

@app.on_event("startup")
async def app_init():
    # Common settings
    app_settings = AppSettings()

    # middleware
    apply_cors(app, app_settings.allowed_origins)

    # INIT DATABASE
    await database.initialize()

    # ADD ROUTES
    for router in routers:
        app.include_router(**router)
