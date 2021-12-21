from app.api import api_router
from app.config import settings
from fastapi import FastAPI


app = FastAPI(title=settings.PROJECT_NAME,
              openapi_url=f'{settings.API_V1_STR}/openapi.json')
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app,
                host='0.0.0.0',
                port=5000,
                log_level='debug')
