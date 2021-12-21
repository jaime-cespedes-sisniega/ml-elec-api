from pathlib import Path

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


class Settings(BaseSettings):
    """Settings class

    Set variables to be used
    """

    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'Machine Learning electricity price prediction'

    DB: DBSettings = DBSettings()
    MODEL: ModelSettings = ModelSettings()


settings = Settings()
