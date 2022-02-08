from datetime import datetime
import json
from typing import Dict

from app import schemas, __version__
from app.config import settings
from app.utils import (check_drift,
                       load_model,
                       log_metrics,
                       make_model_prediction)
from fastapi import APIRouter
from loguru import logger


api_router = APIRouter(tags=['API'])

model = None


@api_router.on_event('startup')
async def startup_model() -> None:
    """Set the model

    Set the model loading it from
    the model registry
    :rtype: None
    """
    global model
    logger.info('Loading model.')
    model = load_model(settings=settings.MODEL_REGISTRY)
    logger.info(f'Model successfully loaded: {model}')


@api_router.on_event('startup')
async def startup_drift_detector() -> None:
    """Set drift detector

    Set the drift detector loading it from
    the model registry
    :rtype: None
    """
    from mlflow.tracking import MlflowClient
    import requests

    client = MlflowClient()
    mlflow_run = client.get_registered_model(
        name=settings.MODEL_REGISTRY.MODEL_NAME).latest_versions[0].run_id

    payload = json.dumps({
        "mlflow_host": settings.MODEL_REGISTRY.MLFLOW_HOST,
        "mlflow_port": settings.MODEL_REGISTRY.MLFLOW_PORT,
        "mlflow_username": settings.MODEL_REGISTRY.MLFLOW_USERNAME,
        "mlflow_password": settings.MODEL_REGISTRY.MLFLOW_PASSWORD,
        "minio_host": settings.MODEL_REGISTRY.MINIO_HOST,
        "minio_port": settings.MODEL_REGISTRY.MINIO_PORT,
        "minio_username": settings.MODEL_REGISTRY.MINIO_USERNAME,
        "minio_password": settings.MODEL_REGISTRY.MINIO_PASSWORD,
        "mlflow_run": mlflow_run,
        "detector_file_name": settings.DRIFT_DETECTOR.DETECTOR_FILE_NAME
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    logger.info('Loading drift detector.')
    response = requests.post(url=f'http://'
                                 f'{settings.DRIFT_DETECTOR.SERVICE_HOST}:'
                                 f'{settings.DRIFT_DETECTOR.SERVICE_PORT}'
                                 f'/detector',
                             data=payload,
                             headers=headers)
    response.raise_for_status()
    logger.info(f'Drift detector successfully loaded: {response.text}')


@api_router.get('/health',
                response_model=schemas.Health,
                status_code=200)
async def health() -> Dict[str, str]:
    """Health check function

    :return: Health check dict
    :rtype: Dict[str: str]
    """
    health_response = schemas.Health(name=settings.PROJECT_NAME,
                                     api_version=__version__)
    return health_response.dict()


@api_router.post('/predict',
                 response_model=schemas.PredictionResponse,
                 status_code=200)
async def predict(input_data: schemas.MultipleDataInputs) -> Dict[str,
                                                                  str]:
    """Predict endpoint

    :param input_data: body request data
    :type input_data: Request
    :return: Predict response dict
    :rtype: Dict[str: str]
    """
    timestamp = datetime.today().isoformat()
    predictions = make_model_prediction(model=model,
                                        input_data=input_data)

    log_metrics(input_data=input_data,
                predictions=predictions)

    drift = await check_drift(settings=settings.DRIFT_DETECTOR,
                              input_data=input_data)

    logger.info(f'Drift check: {drift}')

    response = {'timestamp': timestamp,
                'predictions': predictions,
                'drift': drift}

    return response
