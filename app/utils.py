from app.config import Settings
from app.data_models import Request
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
        host=settings.DB.HOST,
        port=settings.DB.PORT,
        username=settings.DB.USERNAME_,
        password=settings.DB.PASSWORD,
        authSource=settings.DB.DATABASE)
    model = model_registry.load_pipeline(name=settings.MODEL.NAME)
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
