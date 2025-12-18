"""User related models."""

from datetime import UTC, datetime
from typing import ClassVar
from uuid import UUID, uuid4

from sqlmodel import JSON, Column, Field

from src.common import UntypedDict
from src.db.database import BaseSQLModel
from src.utils import SCHEMA_NAME


class User(BaseSQLModel, table=True):
    """Represents a user of the system."""

    __table_args__: ClassVar = {"schema": SCHEMA_NAME}

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    external_id: str | None = Field(default=None, unique=True)
    username: str = Field(index=True)
    email: str | None = Field(default=None, unique=True)
    display_name: str | None = None
    is_dummy: bool = False
    settings: UntypedDict | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_login_at: datetime | None = None
