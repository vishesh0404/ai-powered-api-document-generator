"""Common utilities for the API."""

import logging
import os
import re
from pathlib import Path
from types import FrameType
from typing import override

from loguru import logger

HOME_DIR = Path.home()
DB_DIR = HOME_DIR / ".db"
DB_DIR.mkdir(parents=True, exist_ok=True)
SCHEMA_NAME = "api_schema"

# Support both ${VAR:-default} and ${VAR??default} syntaxes
ENV_PATTERN = r"\${([^{}:??]+)(?::-([^}]+))?(?:\?\?([^}]+))?}"


def _replace_env_vars(match: re.Match[str]) -> str:
    """Replace environment variables with their values or defaults.

    Args:
        match: Regex match object containing variable and default.

    Returns:
        Replaced value from environment or default.
    """
    env_var = match.group(1)
    default_val = match.group(2) or match.group(3) or ""

    # Get value from environment, or use default
    value = os.environ.get(env_var)
    if value is None:
        # Remove quotes if present
        return default_val.strip("\"'")
    return value


def replace_from_env(source: str, pattern: str = ENV_PATTERN) -> str:
    """Replace environment variables with their values or defaults.

    By default, supports both ${VAR:-default} and ${VAR??default} syntaxes.

    Args:
        source: String containing environment variables.
        pattern: Regex pattern for matching environment variables.
        Defaults to ENV_PATTERN.

    Returns:
        String with environment variables replaced.
    """
    return re.sub(pattern, _replace_env_vars, source)


class LoggerHandler(logging.Handler):
    """Custom logging handler for Loguru."""

    @override
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record."""
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame: FrameType = logging.currentframe()
        depth: int = 2
        while frame.f_code.co_filename == logging.__file__:
            _ = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
