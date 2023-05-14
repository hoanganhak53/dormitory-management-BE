from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def apply_cors(app: FastAPI, origins=None):
    if origins is None:
        origins = []

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )