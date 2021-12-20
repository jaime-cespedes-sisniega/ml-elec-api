from api.config import Settings
from api.data_models import Request
from ml_pipeline.model_pipeline import ModelPipeline
from ml_pipeline.registry import ModelPipelineRegistryClient


def load_model(settings: Settings) -> ModelPipeline:
    """Load model

    :param settings: model settings
    :type settings: Settings
    :return: model pipeline object
    :rtype: ModelPipeline
    """
    model_registry = ModelPipelineRegistryClient(
        host=settings.db.host,
        port=settings.db.port,
        username=settings.db.username_,
        password=settings.db.password,
        authSource=settings.db.database)
    model = model_registry.load_pipeline(name=settings.model.name)
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
