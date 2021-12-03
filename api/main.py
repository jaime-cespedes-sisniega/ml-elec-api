from datetime import datetime
import logging
from typing import Dict

from api.config import Settings
from api.data_models import (Request,
                             Response,
                             request_examples,
                             response_examples)
from api.utils import make_prediction
from fastapi import Body, FastAPI
from ml_pipeline.registry import ModelPipelineRegistryClient


logging.basicConfig(level=logging.INFO)

api = FastAPI()
settings = Settings()

model_registry = ModelPipelineRegistryClient(host=settings.db_host,
                                             port=settings.db_port,
                                             db_name=settings.db_name)
model = model_registry.load_pipeline(name=settings.model_name)


@api.post('/',
          response_model=Response,
          responses=response_examples,
          status_code=200)
def predict(data: Request = Body(...,
                                 examples=request_examples)) -> Dict[str, str]:
    """Predict endpoint

    :param data: body request data
    :type data: Request
    :return: Predict response dict
    :rtype: Dict[str: str]
    """
    timestamp = datetime.today().isoformat()
    pred = make_prediction(model=model,
                           data=data)
    response = {'timestamp': timestamp,
                'class_pred': pred}
    return response


@api.get('/health')
async def health() -> Dict[str, str]:
    """Health check function

    :return: Health check dict
    :rtype: Dict[str: str]
    """
    return {'Status': 'Ok!'}
