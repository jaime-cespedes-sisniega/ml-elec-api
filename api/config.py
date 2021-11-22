from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    model_path: Path = Path('api',
                            'model')
    model_file_name: str = 'model_pipeline.joblib'
