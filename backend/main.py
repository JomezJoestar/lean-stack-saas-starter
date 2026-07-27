from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routers import auth, billing  # <-- Add billing import here
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Lean Stack SaaS API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the authentication endpoints
app.include_router(auth.router)
# Register the billing endpoints
app.include_router(billing.router)  # <-- Include billing router here

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "FastAPI is running!"}