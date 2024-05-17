"""Configuration module for the ctk_functions package."""

import functools
import logging

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """App settings."""

    AZURE_STORAGE_ACCOUNT_NAME: pydantic.SecretStr = pydantic.Field(
        ...,
        json_schema_extra={"env": "AZURE_STORAGE_ACCOUNT_NAME"},
    )
    AZURE_STORAGE_SAS: pydantic.SecretStr = pydantic.Field(
        ...,
        json_schema_extra={"env": "AZURE_STORAGE_SAS"},
    )

    LOGGER_VERBOSITY: int = 20
    VALID_FILE_EXTENSIONS: list[str] = ["docx"]


@functools.lru_cache
def get_settings() -> Settings:
    """Gets the app settings."""
    return Settings()  # type: ignore[call-arg]


def get_logger() -> logging.Logger:
    """Gets the ctk-functions logger."""
    logger = logging.getLogger("ctk-functions")
    logger.setLevel(get_settings().LOGGER_VERBOSITY)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s",  # noqa: E501
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
