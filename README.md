# Machine Learning API
This repository contains the implementation of a REST API which serves a machine learning model generated in https://github.com/jaime-cespedes-sisniega/ml-elec.

## Usage
The API is intended to load a model from a models registry, in this case using MongoDB.

Modify `env-mongodb.env` file to set your MongoDB configuration parameters:
```bash
HOST=localhost
PORT=27017
USERNAME_=username
PASSWORD=password
DATABASE=database
```

Also, `env-model.env` file has to be modified to include model´s name:
```bash
NAME=model.joblib
```

> **_NOTE_**: It is assumed that the model has been generated using code implemented in the https://github.com/jaime-cespedes-sisniega/ml-elec/tree/feature-save-model-db repository.


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
curl --location --request POST 'http://0.0.0.0:5000/api/v1/predict' \
--header 'Content-Type: application/json' \
--data-raw '{
    "day": 7,
    "period": 0.978723,
    "nswprice": 0.066651,
    "nswdemand": 0.329366,
    "vicprice": 0.00463,
    "vicdemand": 0.345417,
    "transfer": 0.206579
}'
```
Request output containing a timestamp and the predicted class by the model.
```bash
{
    "timestamp": "2021-11-30T08:01:32.415845",
    "class_pred": "UP"
}
```

More examples can be executed in an interactive way using http://0.0.0.0:5000/docs.

