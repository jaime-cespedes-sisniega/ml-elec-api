# Machine Learning API
This repository contains the implementation of a REST API which serves a machine learning model generated in https://github.com/jaime-cespedes-sisniega/ml-elec.

> **_NOTE_**: At the moment, the serialized model is included in the current API repository. This mode of operation should be replaced by obtaining the model from a model registry or a repository where models are stored.

## Usage

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
