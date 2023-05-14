from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import database
from app.controllers import clustering_server
from app.helpers.nlp_preload import nlp_service
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
    app.include_router(clustering_server, prefix="/api")

    # Load nlp model
    await async_wrap(nlp_service.initialize)()


@app.get("/ping", summary="Health check usage only")
def ping():
    return "PONG!"
