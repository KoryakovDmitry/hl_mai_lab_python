from fastapi import FastAPI
from .routers import users, services, orders
from .database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers from the 'routers' module
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
