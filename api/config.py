from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class

    Set variables to be used by
    the API
    """

    db_host: str = 'localhost'
    db_port: int = 27017
    db_name: str = 'model_registry'
    model_name: str = 'model_pipeline.joblib'
