"""Main server class for the API."""

import logging
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, ClassVar, Self

import uvicorn
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import StrictBool, StrictInt, StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.api import base_router, openapi_router
from src.api.v1.routers import router as v1_routers
from src.common import AnyVal, BaseModel, UntypedDict
from src.db.database import DatabaseConfig, init_engine
from src.utils import LoggerHandler, replace_from_env


class CORSConfig(BaseModel):
    """CORS configuration settings."""

    allow_origins: ClassVar[list[str]] = ["*"]
    """List of allowed origins"""

    allow_methods: ClassVar[list[str]] = ["GET", "POST", "PUT", "DELETE"]
    """List of allowed methods"""

    allow_headers: ClassVar[list[str]] = ["*"]
    """List of allowed headers"""

    allow_credentials: bool = True
    """Allow credentials"""


class APIServerConfig(BaseSettings):
    """API Server configuration settings."""

    host: StrictStr = "127.0.0.1"
    """Host"""

    port: StrictInt = 1506
    """Port"""

    enable_openapi: StrictBool = False
    """This is a boolean flag to enable or disable the OpenAPI documentation"""

    cors: CORSConfig = CORSConfig()
    """CORS configuration"""

    database: DatabaseConfig = DatabaseConfig()
    """Database configuration"""

    def as_dict(self, **kwargs: AnyVal) -> UntypedDict:
        """Serialize the config to a dictionary, including all subclass fields."""
        return self.model_dump(**kwargs)

    def as_json(self, **kwargs: AnyVal) -> str:
        """Serialize the config to JSON, including all subclass fields."""
        return self.model_dump_json(**kwargs)

    @classmethod
    def from_yaml(cls, file_path: Path | str) -> Self:
        """Load YAML with environment variable interpolation supporting defaults.

        This function loads a YAML file and processes environment variable references
        with support for default values using either ${VAR:-default} or ${VAR??default}
        syntax.

        Args:
            file_path: Path to the YAML file.

        Returns:
            API Server Config with environment variables interpolated.
        """
        # Load environment variables from .env file if it exists
        _ = load_dotenv(override=True)

        # Load the YAML template
        with Path(file_path).open(encoding="utf-8") as file:
            yaml_template = file.read()

        # Replace variables with their values
        subs_yaml_content = replace_from_env(yaml_template)

        # Parse the YAML with environment variables replaced
        return cls.model_validate(yaml.safe_load(subs_yaml_content))

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        arbitrary_types_allowed=True,
        env_ignore_empty=True,
        env_nested_delimiter="__",
        extra="ignore",
        str_strip_whitespace=True,
        use_attribute_docstrings=True,
    )


class Server:
    """Main server class for the API."""

    def register_routers(self, app: FastAPI) -> None:
        """Register all routers."""
        app.include_router(v1_routers)
        app.include_router(base_router.router)

    def setup_cors_middleware(self, app: FastAPI, cors_config: CORSConfig) -> None:
        """Setup CORS middleware."""
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_config.allow_origins,
            allow_credentials=cors_config.allow_credentials,
            allow_methods=cors_config.allow_methods,
            allow_headers=cors_config.allow_headers,
        )

    def _init_logging(self) -> None:
        logging.getLogger().handlers = []
        logger.remove()
        _ = logger.add(
            sys.stdout,
            level="INFO",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )
        logging.basicConfig(handlers=[LoggerHandler()], level=0, force=True)

    def run(self, api_server_config: APIServerConfig) -> None:
        """Run the API server."""
        self._init_logging()

        logger.info("Starting the API Server...")

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
            # Initialize singleton DB engine and store in app state
            engine = init_engine(api_server_config.database)
            app.state.engine = engine
            yield

        app: FastAPI = FastAPI(
            # docs_url=None,
            # redoc_url=None,
            title="ai-powered-api-document-generator",
            lifespan=lifespan,
        )
        self.register_routers(app)
        self.setup_cors_middleware(app, api_server_config.cors)

        if api_server_config.enable_openapi:
            app.include_router(openapi_router.router)

        uvicorn.run(
            app,
            host=api_server_config.host,
            port=api_server_config.port,
            log_config=None,
        )
