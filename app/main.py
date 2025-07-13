from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import accounts, airports, classes, info, bookings, flights, login

Base.metadata.create_all(bind=engine)
print("Tables successfully created")
print("Database connected successfully")

app = FastAPI()

app.include_router(login.router)
app.include_router(accounts.router)
app.include_router(info.router)
app.include_router(airports.router)
app.include_router(classes.router)
app.include_router(bookings.router)
app.include_router(flights.router)

