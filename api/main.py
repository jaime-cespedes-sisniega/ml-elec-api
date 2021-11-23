from datetime import datetime
from pathlib import Path
from typing import Dict

from api.config import Settings
from api.data_models import Request, Response
from api.utils import load_model, make_prediction
from fastapi import FastAPI


api = FastAPI()
settings = Settings()

# XXX: Model should be obtained from a model registry
# XXX: or repo and not from the project itself
model = load_model(path=Path(settings.model_path,
                             settings.model_file_name))


@api.post('/',
          response_model=Response,
          status_code=200)
def predict(data: Request) -> Dict[str, str]:
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
