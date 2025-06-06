from datetime import datetime, timezone
from typing import Optional, Dict
from enum import Enum
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


class JSONUpdatesMixing:
    updates_metadata: Mapped[dict] = mapped_column(JSONB, server_default="{}")


class OrmBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def list(cls):
        return [c.value for c in cls]


class TimestampOrmBaseModel(OrmBaseModel):
    created_at: datetime
    updated_at: datetime


class JsonOrmBaseModel(OrmBaseModel):
    updates_metadata: Dict[str, datetime] = {}
