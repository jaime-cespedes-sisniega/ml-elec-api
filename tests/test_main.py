from fastapi.testclient import TestClient

from api.main import api

client = TestClient(api)

data_input = {"day": 3,
              "period": 0.02,
              "nswprice": 0.05,
              "nswdemand": 0.43,
              "vicprice": 0.003,
              "vicdemand": 0.42,
              "transfer": 0.41}


def test_predict_correct():
    response = client.post('/',
                           json=data_input)
    assert response.status_code == 200
    assert response.json()['class_pred'] in ['DOWN', 'UP']


def test_predict_missing_feature():
    data_input_missing = data_input.copy()
    data_input_missing.pop('period')
    response = client.post('/',
                           json=data_input_missing)
    assert response.status_code == 422


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'Status': 'Ok!'}
