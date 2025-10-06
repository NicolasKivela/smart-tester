from fastapi import FastAPI
from .bdd_scenarios.router import router as bdd_router
from .test_script_generator.router import router as test_script_gen
app = FastAPI()

app.include_router(bdd_router)
app.include_router(test_script_gen)