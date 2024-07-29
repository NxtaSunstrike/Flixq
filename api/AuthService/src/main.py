import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from routers.JWTAuth import JWTRouter #main router
from routers.QRAuth import  QRrouter

from db.Postgres.Base import init_models #function for inti models
from db.Postgres.models.UserModel import * #import all models to init 


LOGGER = logging.getLogger(__name__)



#init lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    LOGGER.info('Starting application')
    await init_models()
    yield
    LOGGER.info('Shutting down application')

#create app
app = FastAPI(
    title='Registration',
    description='Registration API microservice',
    version='1.0.0',
    lifespan=lifespan
)

#including routers
app.include_router(JWTRouter, prefix='/JWTauth', tags=['JWTAuth'])
app.include_router(QRrouter, prefix='/qr', tags=['QR'])

    
