from pathlib import Path

from api.data_models import Request
import joblib
from ml_pipeline.model_pipeline import ModelPipeline


def load_model(path: Path) -> ModelPipeline:
    """Load model

    :param path: model pipeline location
    :type path: Path
    :return: model pipeline object
    :rtype: ModelPipeline
    """
    model = joblib.load(path)
    return model


def make_prediction(model: ModelPipeline,
                    data: Request) -> str:
    """Make single prediction

    :param model: model pipeline
    :type model: ModelPipeline
    :param data: data input
    :type data: Request
    :return: class prediction
    :rtype: str
    """
    pred = model.predict([[*data.dict().values()]])[0]
    return pred
