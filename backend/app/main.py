import logging
from fastapi import FastAPI, HTTPException, WebSocket
from app.config import settings
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from app.api.api_v1.api import api_router
from app import models
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

logger.setLevel(logging.INFO)
# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=[str(origin)
    #                for origin in settings.BACKEND_CORS_ORIGINS],
    # allow_origin_regex="https://ibuild-.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    headers = exc.headers

    content = {
        'status_code': exc.status_code,
        'message': str(exc.detail)
    }
    if headers:
        content.update(headers)
    return JSONResponse(content=content, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content={
        'status_code': 422,
        'message': 'Data input is invalid !'
    }, status_code=422)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.on_event("startup")
async def startup():
    from app.db.init import init_db
    init_db()
    logger.info("app start. . .")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown Server. . .")


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)