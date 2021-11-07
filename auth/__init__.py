import motor.motor_asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from beanie import init_beanie

from .config import settings
from .apps.users.documents import Post, User, Comment
from auth.apps import router
from auth.apps.server.server import sio, secondapp


def create_app() -> FastAPI:
    app = FastAPI()
    secondapp = FastAPI()

    @secondapp.get("/sub")
    async def read_sub():
        message = {"message": "Hello World from sub API"}
        return message

    app.mount("/sa", secondapp)

    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def startup_event():
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
        await init_beanie(database=client[settings.MONGODB_DATABASE_NAME], document_models=[Post, User, Comment])

    return app
