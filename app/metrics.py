import os

from app.schemas.predict import DataInput
from fastapi import APIRouter
from prometheus_client import (CONTENT_TYPE_LATEST,
                               REGISTRY,
                               CollectorRegistry,
                               Counter,
                               Histogram,
                               generate_latest,
                               multiprocess)
from starlette.responses import Response

metrics_router = APIRouter(include_in_schema=False)


@metrics_router.get("/metrics")
async def metrics() -> Response:
    """Metrics endpoint

    :return: Metrics response
    :rtype: starlette.responses.Response
    """
    data = generate_latest(registry)
    return Response(data,
                    media_type=CONTENT_TYPE_LATEST)


def _set_collector_registry():
    if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
        pmd = os.environ["PROMETHEUS_MULTIPROC_DIR"]
        if os.path.isdir(pmd):
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry)
        else:
            raise ValueError(
                f"Env var PROMETHEUS_MULTIPROC_DIR='{pmd}' not a directory."
            )
    else:
        registry = REGISTRY
    return registry


def _set_collectors(registry):
    histogram_features = {}
    for feature, field in DataInput.__dict__['__fields__'].items():
        if field.type_ in [int, float]:
            histogram_features[feature] = Histogram(
                f'{feature}_distribution',
                f'Distribution of feature {feature}',
                registry=registry)

    counter_predictions = Counter(
        'model_prediction',
        'Number of times a certain label has been predicted',
        ['class'],
        registry=registry)
    counter_predictions.labels('DOWN')
    counter_predictions.labels('UP')

    return histogram_features, counter_predictions


registry = _set_collector_registry()
histogram_features, counter_predictions = _set_collectors(registry=registry)
