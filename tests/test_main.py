from app import __version__, schemas
from app.config import settings
import pytest
from fastapi.testclient import TestClient


# Patch model registry connection to avoid having a
# database running to run the tests
@pytest.fixture(scope='module')
def client(module_mocker):
    module_mocker.patch('app.config.Settings')
    module_mocker.patch('app.utils.load_model')
    from app.main import app
    with TestClient(app) as test_client:
        yield test_client


data_input = {"day": 3,
              "period": 0.02,
              "nswprice": 0.05,
              "nswdemand": 0.43,
              "vicprice": 0.003,
              "vicdemand": 0.42,
              "transfer": 0.41}


def test_predict_correct_output(client, mocker):
    fake_pred = 'DOWN'
    mock_make_prediction = mocker.patch('app.api.make_prediction',
                                        return_value=fake_pred)
    response = client.post('/api/v1/predict',
                           json=data_input)
    assert response.status_code == 200
    assert response.json()['class_pred'] == fake_pred
    assert mock_make_prediction.call_args.kwargs['data'] == data_input


def test_predict_missing_feature(client):
    data_input_missing = data_input.copy()
    data_input_missing.pop('period')
    response = client.post('/api/v1/predict',
                           json=data_input_missing)
    assert response.status_code == 422


def test_health(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json() == schemas.Health(name=settings.PROJECT_NAME,
                                             api_version=__version__).dict()
