# FastAPI Notes API

REST API quản lý notes sử dụng FastAPI.

## Features

- User registration
- JWT authentication
- Notes CRUD
- Owner authorization
- Pagination
- Search
- Completed status
- Due date
- Tags
- CORS
- Automated tests

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- Pytest

## Setup

```bash
python -m venv .venv
Setup
Run server
Environment variables
Run tests
Seed data

Endpoints:
POST   /auth/register
POST   /auth/login
GET    /auth/me

POST   /notes/
GET    /notes/
GET    /notes/{id}
PUT    /notes/{id}
DELETE /notes/{id}

GET    /health  