from collections import Counter
from datetime import datetime
from typing import Dict

from app import schemas, __version__
from app.config import settings
from app.metrics import (counters_predictions,
                         histograms_features)
from app.utils import load_model, make_prediction
from fastapi import APIRouter


api_router = APIRouter(tags=['API'])

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


@api_router.get('/health',
                response_model=schemas.Health,
                status_code=200)
async def health() -> Dict[str, str]:
    """Health check function

    :return: Health check dict
    :rtype: Dict[str: str]
    """
    health_response = schemas.Health(name=settings.PROJECT_NAME,
                                     api_version=__version__)
    return health_response.dict()


class LabelError(Exception):
    """Label error exception"""

    pass


@api_router.post('/predict',
                 response_model=schemas.PredictionResponse,
                 status_code=200)
async def predict(input_data: schemas.MultipleDataInputs) -> Dict[str,
                                                                  str]:
    """Predict endpoint

    :param input_data: body request data
    :type input_data: Request
    :return: Predict response dict
    :rtype: Dict[str: str]
    """
    timestamp = datetime.today().isoformat()
    predictions = make_prediction(model=model,
                                  input_data=input_data)
    response = {'timestamp': timestamp,
                'predictions': predictions}

    for input_ in input_data.inputs:
        for feature, value in input_.dict().items():
            histograms_features[feature].observe(value)

    for label, value in Counter(predictions).items():
        try:
            counters_predictions[label].inc(value)
        except KeyError:
            raise LabelError(f'label {label} not existing')

    return response
