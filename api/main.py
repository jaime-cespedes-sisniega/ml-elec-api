from datetime import datetime
from typing import Dict

from api.config import Settings
from api.data_models import (Request,
                             Response,
                             request_examples,
                             response_examples)
from api.utils import load_model, make_prediction
from fastapi import Body, FastAPI


api = FastAPI()
settings = Settings()

model = None


@api.on_event('startup')
async def startup_model() -> None:
    """Set the model

    Set the model loading it from
    the model registry
    :rtype: None
    """
    global model
    model = load_model(settings)


@api.post('/',
          response_model=Response,
          responses=response_examples,
          status_code=200)
async def predict(data: Request = Body(...,
                                       examples=request_examples)) -> Dict[str,
                                                                           str]:
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
