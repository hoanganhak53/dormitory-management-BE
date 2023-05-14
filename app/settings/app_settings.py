from typing import Any

from dynaconf import Validator
from pydantic import BaseSettings

from config.config import settings


def must_be_list(value):
    return isinstance(value, list)


def must_be_str(value):
    return isinstance(value, str)


class AppSettings(BaseSettings):
    def __init__(self, **values: Any):
        super().__init__(**values)

        # Register validators
        settings.validators.register(
            Validator("ALLOWED_ORIGINS", condition=must_be_list, must_exist=True),
            Validator("MONGO_DSN", must_exist=True),
        )
        # Fire the validator
        settings.validators.validate()

    @property
    def allowed_origins(self):
        return settings.get("ALLOWED_ORIGINS")

    @property
    def mongo_dsn(self):
        return settings.get("MONGO_DSN")
