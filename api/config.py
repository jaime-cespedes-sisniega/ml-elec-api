from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class

    Set variables to be used by
    the API
    """

    db_host: str
    db_port: int
    db_name: str
    model_name: str

    class Config:
        """Config class

        Set env file to read
        """

        env_file = '.env'
        env_file_encoding = 'utf-8'
