import copy

from fastapi.testclient import TestClient
import pytest


# Patch model registry connection to avoid having a
# database running to run the tests
@pytest.fixture(scope='module')
def client(module_mocker):
    module_mocker.patch('app.config.Settings')
    module_mocker.patch('app.utils.load_model')
    from app.main import app
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='module')
def input_data():
    return {
        "inputs": [
            {
                "day": 3,
                "period": 0.02,
                "nswprice": 0.05,
                "nswdemand": 0.43,
                "vicprice": 0.003,
                "vicdemand": 0.42,
                "transfer": 0.41
            }
        ]
    }


@pytest.fixture()
def input_data_missing_feature(input_data):
    input_data_missing = copy.deepcopy(input_data)
    input_data_missing['inputs'][0].pop('period')

    return input_data_missing


@pytest.fixture()
def input_data_wrong_feature_type(input_data):
    input_data_wrong = copy.deepcopy(input_data)
    input_data_wrong['inputs'][0]['day'] = 'wrong_type'

    return input_data_wrong
