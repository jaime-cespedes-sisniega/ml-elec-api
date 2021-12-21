from app import __version__, schemas
from app.config import settings


def test_predict_correct_output(client,
                                input_data,
                                mocker):
    fake_pred = ['DOWN']
    mock_make_prediction = mocker.patch('app.api.make_prediction',
                                        return_value=fake_pred)
    response = client.post('/api/v1/predict',
                           json=input_data)
    assert response.status_code == 200
    assert response.json()['predictions'] == fake_pred
    assert mock_make_prediction.call_args.kwargs['input_data'] == input_data


def test_predict_missing_feature(client,
                                 input_data_missing_feature):
    response = client.post('/api/v1/predict',
                           json=input_data_missing_feature)
    assert response.status_code == 422
    assert response.text == ('{"detail":[{"loc":["body","inputs",0,"period"],'
                             '"msg":"field required","type":"value_error.missing"}]}')


def test_predict_wrong_feature_type(client,
                                    input_data_wrong_feature_type):
    response = client.post('/api/v1/predict',
                           json=input_data_wrong_feature_type)
    assert response.status_code == 422
    assert response.text == ('{"detail":[{"loc":["body","inputs",0,"day"],'
                             '"msg":"value is not a valid integer","type":"type_error.integer"}]}')


def test_health(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json() == schemas.Health(name=settings.PROJECT_NAME,
                                             api_version=__version__).dict()
