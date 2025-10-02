# Address Book API

A simple address book REST API built with FastAPI, SQLModel, and SQLite.

## Setup

Install dependencies:
```bash
uv sync
```

## Run

```bash
uv run main.py
```

API will be available at `http://localhost:8000`

## Test

```bash
uv run pytest
```

## API Endpoints

- `GET /` - Welcome message
- `POST /contacts/` - Create contact
- `GET /contacts/` - List all contacts
- `GET /contacts/{id}` - Get contact by ID
- `PATCH /contacts/{id}` - Update contact
- `DELETE /contacts/{id}` - Delete contact

Interactive docs: `http://localhost:8000/docs`
