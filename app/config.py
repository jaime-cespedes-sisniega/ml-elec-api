import logging
from pathlib import Path
import sys
from types import FrameType
from typing import cast

from loguru import logger
from pydantic import BaseSettings


class DBSettings(BaseSettings):
    """Database settings class

    Set database variables to be used
    """

    HOST: str
    PORT: int
    USERNAME_: str
    PASSWORD: str
    DATABASE: str

    class Config:
        """Config class

        Set env file to read
        """

        env_file = Path(__file__).parent.parent / 'env-mongodb.env'
        env_file_encoding = 'utf-8'


class ModelSettings(BaseSettings):
    """Model settings class

    Set models variables to be used
    """

    NAME: str

    class Config:
        """Config class

        Set env file to read
        """

        env_file = Path(__file__).parent.parent / 'env-model.env'
        env_file_encoding = 'utf-8'


class LoggingSettings(BaseSettings):
    """Logging settings class

    Set logging info level to be used
    """

    LEVEL: int = logging.INFO


class Settings(BaseSettings):
    """Settings class

    Set variables to be used
    """

    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'Machine Learning electricity price prediction'

    LOGGING: LoggingSettings = LoggingSettings()
    DB: DBSettings = DBSettings()
    MODEL: ModelSettings = ModelSettings()


# See: https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging  # noqa
class InterceptHandler(logging.Handler):  # noqa: D101
    def emit(self, record: logging.LogRecord) \
            -> None:  # pragma: no cover, noqa: D102
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_app_logging(config: Settings) -> None:
    """Prepare custom logging for our application."""
    loggers = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in loggers:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.LOGGING.LEVEL)]

    logger.configure(
        handlers=[{"sink": sys.stderr, "level": config.LOGGING.LEVEL}]
    )


settings = Settings()
