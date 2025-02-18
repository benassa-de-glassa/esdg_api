from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from routers import api

app = FastAPI()


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(
    api.router,
    prefix='/api')

