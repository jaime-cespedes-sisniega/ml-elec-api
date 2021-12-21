from datetime import datetime
from typing import Dict

from app.config import settings
from app.data_models import (Request,
                             Response,
                             request_examples,
                             response_examples)
from app.utils import load_model, make_prediction
from fastapi import APIRouter, Body


api_router = APIRouter()

model = None


@api_router.on_event('startup')
async def startup_model() -> None:
    """Set the model

    Set the model loading it from
    the model registry
    :rtype: None
    """
    global model
    model = load_model(settings)


@api_router.get('/health')
async def health() -> Dict[str, str]:
    """Health check function

    :return: Health check dict
    :rtype: Dict[str: str]
    """
    return {'Status': 'Ok!'}


@api_router.post('/predict',
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
