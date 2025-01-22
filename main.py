# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.user_routes import router as user_router
from app.routes.channel_routes import router as channel_router
from app.db import mongo_conn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB on startup
    await mongo_conn.connect()
    
    # Store your collections on the app's state once connected
    app.state.users_collection = mongo_conn.db["users"]
    app.state.links_collection = mongo_conn.db["links"]
    
    # Yield control back to FastAPI to run the app
    yield
    
    # Close the connection on shutdown
    await mongo_conn.close()

# Create one FastAPI instance, referencing the lifespan function
app = FastAPI(
    title="Channel Management API",
    lifespan=lifespan,
)

# Now include your routers
app.include_router(user_router, prefix="/auth", tags=["User Auth"])
app.include_router(channel_router, prefix="/api", tags=["Channels"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Channel Management API"}
