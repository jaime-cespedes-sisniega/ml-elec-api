from collections import Counter
import os
from typing import (Dict,
                    List,
                    Union)

import aiohttp
from app import schemas
from app.config import (DriftDetectorSettings,
                        ModelRegistrySettings)
from app.metrics import (counter_predictions,
                         histogram_features)
from app.schemas import MultipleDataInputs
from fastapi.encoders import jsonable_encoder
from loguru import logger
import mlflow
import numpy as np
import sklearn.pipeline


def load_model(settings: ModelRegistrySettings) -> sklearn.pipeline.Pipeline:
    """Load model

    :param settings: model settings
    :type settings: ModelRegistrySettings
    :return: model pipeline object
    :rtype: sklearn.pipeline.Pipeline
    """
    mlflow.set_tracking_uri(f'http://{settings.MLFLOW_HOST}'
                            f':{settings.MLFLOW_PORT}')
    os.environ['MLFLOW_TRACKING_USERNAME'] = settings.MLFLOW_USERNAME
    os.environ['MLFLOW_TRACKING_PASSWORD'] = settings.MLFLOW_PASSWORD
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = f'http://{settings.MINIO_HOST}' \
                                           f':{settings.MINIO_PORT}'
    os.environ['AWS_ACCESS_KEY_ID'] = settings.MINIO_USERNAME
    os.environ['AWS_SECRET_ACCESS_KEY'] = settings.MINIO_PASSWORD

    model = mlflow.sklearn.load_model(
        model_uri=f"models:/{settings.MODEL_NAME}/None",
    )

    return model


def make_model_prediction(model: sklearn.pipeline.Pipeline,
                          input_data: schemas.MultipleDataInputs) -> str:
    """Make single prediction

    :param model: model pipeline
    :type model: sklearn.pipeline.Pipeline
    :param input_data: data input
    :type input_data: Request
    :return: class prediction
    :rtype: str
    """
    logger.info(f'Making prediction on inputs: {input_data.inputs}')
    model_input = np.array([[*sample.values()]
                            for sample in jsonable_encoder(input_data.inputs)])
    predictions = [*model.predict(model_input)]
    logger.info(f"Prediction results: {predictions}")
    return predictions


def log_metrics(input_data: List[MultipleDataInputs],
                predictions: List[str]) -> None:
    """Log metrics to /metrics endpoint

    :param input_data: input data to log
    :type input_data: List[MultipleDataInputs]
    :param predictions: predictions to log
    :type predictions: List[str]
    :rtype: None
    """
    for input_ in input_data.inputs:
        for feature, value in input_.dict().items():
            histogram_features[feature].observe(value)

    for label, value in Counter(predictions).items():
        counter_predictions.labels(label).inc(value)


async def check_drift(settings: DriftDetectorSettings,
                      input_data: schemas.MultipleDataInputs) \
        -> List[Dict[str, Union[None, str, int, float]]]:
    """Check drift by requesting drift service

    :param settings: input data to log
    :type settings: DriftDetectorSettings
    :param input_data: input data to check drift
    :type input_data: List[str]
    :return drift service response
    :rtype: List[Dict[str, Union[None, str, int, float]]]
    """
    logger.info(f'Checking drift on inputs: {input_data.inputs}')
    drift_responses = []
    for input_data_sample in input_data.inputs:
        async with aiohttp.ClientSession() as session:
            url = f'http://{settings.SERVICE_HOST}:' \
                  f'{settings.SERVICE_PORT}/drift'
            payload = {
                'values': [*input_data_sample.dict().values()]
            }
            async with session.post(url=url,
                                    json=payload) as resp:
                response = await resp.json()
        drift_responses.append(response)
    logger.info(f"Drift results: {drift_responses}")
    return drift_responses
