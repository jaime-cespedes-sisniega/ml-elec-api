from pathlib import Path

from pydantic import BaseSettings


class DBSettings(BaseSettings):
    """Database settings class

    Set database variables to be used
    """

    host: str
    port: int
    username_: str
    password: str
    database: str

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

    name: str = 'model_pipeline.joblib'

    class Config:
        """Config class

        Set env file to read
        """

        env_file = Path(__file__).parent.parent / 'env-model.env'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    """Settings class

    Set variables to be used
    """

    db: DBSettings = DBSettings()
    model: ModelSettings = ModelSettings()
