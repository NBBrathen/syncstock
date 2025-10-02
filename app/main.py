from app.routers import products
from fastapi import FastAPI

# from sqlalchemy import create_engine
#
# engine = create_engine('')

app = FastAPI(
    title="SyncStock API",
    description="Inventory and Order Management SaaS",
    version="0.1.0",
)

app.include_router((products.router))

# Root endpoint
@app.get('/')
def read_root():
    return {
        "message": "Welcome to SyncStock API",
        "docs": "/docs",
        "version": "0.1.0"
    }

