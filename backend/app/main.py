from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .bdd_scenarios.router import router as bdd_router
from .test_script_generator.router import router as test_script_gen
from .requirement_handling.router import router as req_processing
from .locator_retrieval.router import router as locator_processing
from app.common.database import init_db
app = FastAPI()

#Call database init function
@app.on_event("startup")
def on_startup():
    init_db()
    
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174","http://172.18.0.2:5173"],  # Allow our frontend to access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bdd_router)
app.include_router(test_script_gen)
app.include_router(req_processing)
app.include_router(locator_processing)