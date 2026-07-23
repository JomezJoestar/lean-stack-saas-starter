from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routers import auth, billing  # <-- Add billing import here

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Lean Stack SaaS API", lifespan=lifespan)

# Register the authentication endpoints
app.include_router(auth.router)
# Register the billing endpoints
app.include_router(billing.router)  # <-- Include billing router here

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "FastAPI is running!"}