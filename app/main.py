from fastapi import FastAPI


from app.routers import auth, orders, products

# Creat the FastAPI application
app = FastAPI(
    title="SyncStock API",
    description="Inventory and Order Management SaaS",
    version="0.1.0",
)

# Include the product, auth, and order routers
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to SyncStock API", "docs": "/docs", "version": "0.1.0"}
