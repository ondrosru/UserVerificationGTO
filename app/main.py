import uvicorn
from fastapi import FastAPI
from app.api.v1 import api
from app.core.config import get_settings


settings = get_settings()
app = FastAPI(version="1.0.0")
app.include_router(api.api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(app)
