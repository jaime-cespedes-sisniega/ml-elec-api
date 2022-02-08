# Machine Learning API
This repository contains the implementation of a REST API which serves a machine learning model generated in https://github.com/jaime-cespedes-sisniega/ml-elec and stored in MLflow´s Model Registry.

## Usage
The API is intended to load a model from a models registry, in this case using MLflow´s Model Registry and MinIO as artifacts storage.

Rename `.env.example` to `.env`.

```bash
mv .env.example .env
```

Modify `.env` file to set your models' registry configuration parameters:
```bash
MODEL_REGISTRY__MLFLOW_HOST=mlflow_host
MODEL_REGISTRY__MLFLOW_PORT=80
MODEL_REGISTRY__MLFLOW_USERNAME=username
MODEL_REGISTRY__MLFLOW_PASSWORD=password
MODEL_REGISTRY__MODEL_NAME=model_name
MODEL_REGISTRY__MINIO_HOST=minio_host
MODEL_REGISTRY__MINIO_PORT=9000
MODEL_REGISTRY__MINIO_USERNAME=username
MODEL_REGISTRY__MINIO_PASSWORD=password

DRIFT_DETECTOR__SERVICE_HOST=service_host
DRIFT_DETECTOR__SERVICE_PORT=5001
DRIFT_DETECTOR__DETECTOR_FILE_NAME=detector_name
```

The following command allows to create a virtualenv and install the requirements.
```bash
make install
```

API can be used in local using uvicorn:
```bash
make serve-dev
```

Or combining gunicorn with uvicorn workers:
```bash
make serve-prod
```

## Docker

To build the Docker image that allows the API to be used as a container, it can be built as follows:
```bash
make build
```
Finally, it can be run as a container.
```bash
make run
```

## Request example
The following curl command shows an example of a request sent to the Docker container in which features used by the machine learning model are also sent.

```bash
curl -X 'POST' \
  'http://0.0.0.0:5000/api/v1/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "inputs": [
    {
      "day": 7,
      "period": 0.978723,
      "nswprice": 0.066651,
      "nswdemand": 0.329366,
      "vicprice": 0.00463,
      "vicdemand": 0.345417,
      "transfer": 0.206579
    }
  ]
}'
```
Request output containing a timestamp and the predicted class by the model.
```bash
{
    "timestamp": "2021-11-30T08:01:32.415845",
    "predictions": ["UP"]
}
```

More examples can be executed in an interactive way using http://0.0.0.0:5000/api/v1/docs.

