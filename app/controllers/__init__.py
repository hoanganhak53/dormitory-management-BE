from fastapi import APIRouter, Depends

from .cluster_object import cluster_object_controller
from .clustering import clustering_controller

clustering_server = APIRouter(
    dependencies=[
    ],
)

clustering_server.include_router(
    cluster_object_controller,
    tags=['cluster_object']
)
clustering_server.include_router(
    clustering_controller,
    tags=['clustering']
)