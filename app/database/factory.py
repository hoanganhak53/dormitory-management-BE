import json
from pathlib import Path
from typing import Type, Union
from beanie import init_beanie, Document
from motor import motor_asyncio

from app.settings.app_settings import AppSettings
from app.models.user import UserData
from app.models.apartment import ApartmentData
from app.models.form import FormData
from app.models.post import PostData
from app.models.registration import RegistrationData
from app.models.room_type import RoomTypeData
from app.models.room import RoomData
from app.models.student_room import StudentRoomData


async def init_collection(col: Type[Document], file_path: Union[str, Path]):
    existing_items = await col.find_all(limit=5).to_list()
    if not existing_items:
        fileVar = open(file_path, encoding="utf-8")
        default_items = json.load(fileVar)
        fileVar.close()
        for default_item in default_items:
            item_id = default_item.get("_id")
            if item_id and item_id.get("$oid"):
                default_item.update({"_id": item_id.get("$oid")})
            item_created_at = default_item.get("created_at")
            if item_created_at and item_created_at.get("$date"):
                default_item.update({"created_at": item_created_at.get("$date")})
            item = col(**default_item)
            await item.create()
        print(f"Successfully init data for collection {col.__name__}")


async def init_collections():
    # Implement later
    pass


async def initialize():
    app_settings = AppSettings()

    # CREATE MOTOR CLIENT
    client = motor_asyncio.AsyncIOMotorClient(app_settings.mongo_dsn, maxPoolSize=5)

    # INIT BEANIE
    await init_beanie(
        client.get_database(),
        document_models=[
            UserData,
            ApartmentData,
            FormData,
            PostData,
            RegistrationData,
            RoomData,
            RoomTypeData,
            StudentRoomData
        ],
    )

    # CREATE DATA
    # await init_collections()

    print("Database is successfully initialized.")