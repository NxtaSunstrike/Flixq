from fastapi import FastAPI
from contextlib import asynccontextmanager


from routers.ChatRouter import ChatRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan
)

app.include_router(ChatRouter)


