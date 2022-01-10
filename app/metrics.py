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

# def _set_collector_registry():
#     registry = CollectorRegistry()
#     multiprocess.MultiProcessCollector(registry,
#                                        path=settings.MONITORING.PROMETHEUS_MULTIPROC_DIR)
#     return registry


def _set_collectors(registry):
    histograms_features = {}
    for feature, field in DataInput.__dict__['__fields__'].items():
        if field.type_ in [int, float]:
            histograms_features[feature] = Histogram(
                f'{feature}_distribution',
                f'Distribution of feature {feature}',
                registry=registry)
    counters_predictions = {
        'DOWN': Counter('model_prediction_down',
                        'Number of times DOWN label has been predicted.',
                        registry=registry),
        'UP': Counter('model_prediction_up',
                      'Number of times UP label has been predicted.',
                      registry=registry)}

    return histograms_features, counters_predictions


registry = _set_collector_registry()
histograms_features, counters_predictions = _set_collectors(registry=registry)
