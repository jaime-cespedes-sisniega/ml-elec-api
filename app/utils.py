from collections import Counter
from typing import List

from app import schemas
from app.config import Settings
from app.metrics import (counter_predictions,
                         histogram_features)
from app.schemas import MultipleDataInputs
from fastapi.encoders import jsonable_encoder
from loguru import logger
from ml_pipeline.model_pipeline import ModelPipeline
from ml_pipeline.registry import ModelPipelineRegistryClient
import numpy as np


def load_model(settings: Settings) -> ModelPipeline:
    """Load model

    :param settings: model settings
    :type settings: Settings
    :return: model pipeline object
    :rtype: ModelPipeline
    """
    model_registry = ModelPipelineRegistryClient(
        host=settings.DB.HOST,
        port=settings.DB.PORT,
        username=settings.DB.USERNAME_,
        password=settings.DB.PASSWORD,
        authSource=settings.DB.DATABASE)
    model = model_registry.load_pipeline(name=settings.MODEL.NAME)
    return model


def make_prediction(model: ModelPipeline,
                    input_data: schemas.MultipleDataInputs) -> str:
    """Make single prediction

    :param model: model pipeline
    :type model: ModelPipeline
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
