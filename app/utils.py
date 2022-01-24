from collections import Counter
import os
from typing import List

from app import schemas
from app.config import Settings
from app.metrics import (counter_predictions,
                         histogram_features)
from app.schemas import MultipleDataInputs
from fastapi.encoders import jsonable_encoder
from loguru import logger
import mlflow
import numpy as np
import sklearn.pipeline


def load_model(settings: Settings) -> sklearn.pipeline.Pipeline:
    """Load model

    :param settings: model settings
    :type settings: Settings
    :return: model pipeline object
    :rtype: sklearn.pipeline.Pipeline
    """
    mlflow.set_tracking_uri(f'http://{settings.MODEL_REGISTRY.MLFLOW_HOST}'
                            f':{settings.MODEL_REGISTRY.MLFLOW_PORT}')
    os.environ['MLFLOW_TRACKING_USERNAME'] = \
        settings.MODEL_REGISTRY.MLFLOW_USERNAME
    os.environ['MLFLOW_TRACKING_PASSWORD'] = \
        settings.MODEL_REGISTRY.MLFLOW_PASSWORD
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = \
        f'http://{settings.MODEL_REGISTRY.MINIO_HOST}' \
        f':{settings.MODEL_REGISTRY.MINIO_PORT}'
    os.environ['AWS_ACCESS_KEY_ID'] = settings.MODEL_REGISTRY.MINIO_USERNAME
    os.environ['AWS_SECRET_ACCESS_KEY'] = settings.MODEL_REGISTRY.MINIO_PASSWORD

    model = mlflow.sklearn.load_model(
        model_uri=f"models:/{settings.MODEL_REGISTRY.MODEL_NAME}/None",
    )

    return model


def make_prediction(model: sklearn.pipeline.Pipeline,
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
