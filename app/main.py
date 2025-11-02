import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import create_db_and_tables
from app.routers import contacts, households, lists

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Address Book API", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(contacts.router)
app.include_router(households.router)
app.include_router(lists.router)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/lists", response_class=HTMLResponse)
def read_lists(request: Request):
    return templates.TemplateResponse(request, "lists.html")


@app.get("/api/config")
def get_config():
    return {"google_api_key": os.getenv("GOOGLE_API_KEY")}
