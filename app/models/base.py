from datetime import datetime
from enum import Enum
from typing import Any, Mapping, Dict, Optional

from beanie import Document
from pydantic import Field, BaseModel


class RootModel(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def random(cls, *args: Mapping[str, Any], size: int = 1):
        return cls.find_many(*args).aggregate(
            [
                {"$sample": {"size": size}},
            ],
        )


class RootEnum(Enum):
    @classmethod
    def _missing_(cls, key):
        for member in cls:
            if member.name.lower() == key.lower():
                return member

    @classmethod
    def values(cls):
        return [member.value for member in cls.__members__.values()]
    
    
class RootResponse(BaseModel):
    error_code: int = 0
    message: str = ""
    data: Optional[Dict]