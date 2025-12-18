"""Common types for the API."""

from typing import Any, ClassVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

type AnyVal = Any  # pyright: ignore [reportExplicitAny]
type UntypedDict = dict[str, AnyVal]


class BaseModel(PydanticBaseModel):
    """Base model for other models."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        arbitrary_types_allowed=True,
        extra="ignore",
        str_strip_whitespace=True,
        use_attribute_docstrings=True,
        validate_by_name=True,
        validate_by_alias=True,
    )
