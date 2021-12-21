from app.api import api_router
from app.config import settings, setup_app_logging
from fastapi import FastAPI
from loguru import logger


setup_app_logging(config=settings)

app = FastAPI(title=settings.PROJECT_NAME,
              openapi_url=f'{settings.API_V1_STR}/openapi.json')
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    logger.warning("Running in development mode. "
                   "Do not run like this in production.")
    import uvicorn

    uvicorn.run(app,
                host='0.0.0.0',
                port=5000,
                log_level='debug')
