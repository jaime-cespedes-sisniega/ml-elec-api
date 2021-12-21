from app import schemas
from app.config import Settings
from fastapi.encoders import jsonable_encoder
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
    model_input = np.array([[*sample.values()]
                            for sample in jsonable_encoder(input_data.inputs)])
    pred = [*model.predict(model_input)]
    return pred
