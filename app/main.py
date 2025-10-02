from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import contacts


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Address Book API", lifespan=lifespan)

app.include_router(contacts.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Address Book API"}
