from fastapi import FastAPI
from .bdd_scenarios.router import router as bdd_router

app = FastAPI()

app.include_router(bdd_router)