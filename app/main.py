from app.routers import products
from fastapi import FastAPI
from app.database import engine
from app import models

# Create all the database tables
# This reads the models and creates the corresponding tables in PostgreSQL
models.Base.metadata.create_all(bind=engine)


# Creat the FastAPI application
app = FastAPI(
    title="SyncStock API",
    description="Inventory and Order Management SaaS",
    version="0.1.0",
)

# Include the products router
app.include_router(products.router)

# Root endpoint
@app.get('/')
def read_root():
    return {
        "message": "Welcome to SyncStock API",
        "docs": "/docs",
        "version": "0.1.0"
    }

