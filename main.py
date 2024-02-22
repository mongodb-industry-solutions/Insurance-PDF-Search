from fastapi import FastAPI
from routes.route import router

app = FastAPI()

app.include_router(router)