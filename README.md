# FastAPI Notes API

REST API quản lý ghi chú được xây dựng bằng FastAPI.

Project hỗ trợ đăng ký tài khoản, đăng nhập bằng JWT, CRUD notes, phân quyền theo người dùng, pagination, search, tags, deadline và trạng thái hoàn thành.

## Features

- User registration
- JWT authentication
- Notes CRUD
- Owner authorization
- Pagination
- Search notes by title
- Completed status
- Due date
- Tags
- CORS configuration
- Seed data
- Automated tests with Pytest
- Swagger / OpenAPI documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy 2
- SQLite
- Pydantic
- JWT
- Passlib / bcrypt
- Pytest

## Project Structure

```text
fastapi-notes-api/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   └── notes.py
│   ├── auth_dependencies.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_notes_authorized.py
│   └── test_notes_unauthorized.py
│
├── .env.example
├── .gitignore
├── create_db.py
├── pytest.ini
├── requirements.txt
├── seed.py
└── README.md
```

## Setup

### 1. Clone repository

```bash
git clone https://github.com/cancer4515-beep/fastapi-notes-api.git
cd fastapi-notes-api
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Tạo file `.env` từ `.env.example`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Ví dụ:

```env
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./day51.db
CORS_ORIGINS=["http://127.0.0.1:5500","http://localhost:5500"]
```

> Không commit file `.env` lên GitHub.

## Create Database

```bash
python create_db.py
```

## Seed Data

Tạo user demo và notes mẫu:

```bash
python seed.py
```

Tài khoản demo:

```text
username: demo
password: matkhau123
```

Tài khoản này chỉ dùng cho môi trường học tập/local development.

## Run Server

```bash
python -m uvicorn app.main:app --reload
```

API chạy tại:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Authentication

API sử dụng JWT Bearer Token.

Đăng nhập qua:

```text
POST /auth/login
```

Sau khi đăng nhập thành công, API trả về:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

Các endpoint `/notes` yêu cầu JWT authentication.

Trong Swagger có thể sử dụng nút **Authorize** để đăng nhập.

## API Endpoints

### System

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Kiểm tra API đang chạy |
| GET | `/health` | Health check |

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Đăng ký tài khoản |
| POST | `/auth/login` | Đăng nhập và nhận JWT |
| GET | `/auth/me` | Lấy thông tin user hiện tại |

### Notes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/notes/` | Tạo note |
| GET | `/notes/` | Lấy danh sách notes |
| GET | `/notes/{note_id}` | Lấy một note |
| PUT | `/notes/{note_id}` | Cập nhật note |
| DELETE | `/notes/{note_id}` | Xóa note |

User chỉ có thể đọc, sửa và xóa notes thuộc tài khoản của mình.

## Create Note

Request:

```json
{
  "title": "Học FastAPI",
  "content": "Hoàn thành Day 51",
  "completed": false,
  "due_date": "2026-09-25T20:00:00",
  "tags": [
    "python",
    "fastapi"
  ]
}
```

Response ví dụ:

```json
{
  "id": 1,
  "title": "Học FastAPI",
  "content": "Hoàn thành Day 51",
  "completed": false,
  "due_date": "2026-09-25T20:00:00",
  "tags": [
    "python",
    "fastapi"
  ],
  "owner_id": 1
}
```

## Update Note

Có thể cập nhật một hoặc nhiều field.

Ví dụ đánh dấu note đã hoàn thành:

```json
{
  "completed": true
}
```

Xóa deadline:

```json
{
  "due_date": null
}
```

## Pagination

Endpoint:

```text
GET /notes/
```

Hỗ trợ:

```text
skip
limit
```

Ví dụ:

```text
GET /notes/?skip=0&limit=10
```

Trong đó:

```text
skip  = số bản ghi bỏ qua
limit = số bản ghi tối đa trả về
```

## Search

Có thể tìm kiếm note theo title:

```text
GET /notes/?search=FastAPI
```

Có thể kết hợp search và pagination:

```text
GET /notes/?skip=0&limit=10&search=FastAPI
```

## Note Fields

Một note gồm:

```text
id
title
content
completed
due_date
tags
owner_id
```

`completed` mặc định:

```text
false
```

`due_date` có thể là:

```text
null
```

`tags` là danh sách string, tối đa 10 tags.

## Run Tests

Chạy toàn bộ test:

```bash
python -m pytest
```

Chạy chi tiết hơn:

```bash
python -m pytest -v
```

Các test bao gồm:

- Register / Login
- JWT authentication
- Authorized notes CRUD
- Unauthorized access
- Owner authorization
- completed
- due_date
- tags validation
- Health check

## Security

- Password không được lưu trực tiếp trong database.
- Password được hash bằng bcrypt.
- Authentication sử dụng JWT.
- User chỉ được truy cập notes của chính mình.
- Secret configuration được lưu trong `.env`.
- `.env` và database local không được commit lên GitHub.

## API Documentation

FastAPI tự động tạo OpenAPI documentation.

Sau khi chạy server:

```text
Swagger UI: http://127.0.0.1:8000/docs
ReDoc:      http://127.0.0.1:8000/redoc
```

## Current Version

```text
v1.1.0
```

Day 51 features:

```text
Notes CRUD
JWT Authentication
Owner Authorization
Pagination
Search
Completed
Due Date
Tags
Seed Data
Automated Tests
OpenAPI Documentation
```
## Docker

Project hỗ trợ chạy bằng Docker và Docker Compose.

### Build và chạy project

Chạy:

```bash
docker compose up -d --build
```

Lệnh này sẽ:

- Build Docker image từ `Dockerfile`
- Tạo container FastAPI
- Mở port `8000`
- Đọc biến môi trường từ `.env`
- Gắn Docker Volume để lưu database
- Khởi động API

### Kiểm tra container

```bash
docker compose ps
```

Nếu hoạt động đúng, trạng thái container sẽ gần giống:

```text
Up ... (healthy)
```

### Tạo database trong container

Lần đầu chạy project bằng Docker:

```bash
docker compose exec api python create_db.py
```

### Seed dữ liệu mẫu

```bash
docker compose exec api python seed.py
```

Tài khoản demo:

```text
username: demo
password: matkhau123
```

### Mở API

API:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

### Xem logs

```bash
docker compose logs api
```

Xem logs liên tục:

```bash
docker compose logs -f api
```

Nhấn:

```text
Ctrl + C
```

để thoát khỏi chế độ xem logs.

### Chạy test trong Docker

```bash
docker compose exec api python -m pytest
```

### Chạy lệnh bên trong container

Ví dụ kiểm tra phiên bản Python:

```bash
docker compose exec api python --version
```

Xem file bên trong container:

```bash
docker compose exec api ls
```

### Dừng project

```bash
docker compose down
```

Lệnh này dừng và xóa container nhưng vẫn giữ Docker Volume.

Database vẫn được giữ lại.

### Chạy lại project

```bash
docker compose up -d
```

Database cũ vẫn còn nhờ Docker Volume.

### Docker Volume

Project sử dụng volume:

```text
fastapi-notes-data
```

Database SQLite được lưu tại:

```text
/data/day51.db
```

bên trong container.

Volume giúp dữ liệu không bị mất khi container bị xóa và tạo lại.

Kiểm tra volume:

```bash
docker volume ls
```

> Không dùng `docker compose down -v` nếu muốn giữ lại database.

### Docker Files

Project sử dụng:

```text
Dockerfile
.dockerignore
compose.yaml
```

`Dockerfile` dùng để build Docker image.

`.dockerignore` loại bỏ các file không cần thiết khỏi image như:

```text
.venv
.env
*.db
.git
__pycache__
```

`compose.yaml` cấu hình:

```text
FastAPI container
Port 8000
Environment variables
Docker Volume
Healthcheck
```

### Docker workflow

```text
Dockerfile
    ↓
Docker Image
    ↓
Docker Container
    ↓
FastAPI
    ↓
Docker Volume
    ↓
SQLite Database
```

## Day 52 - Docker

Nội dung đã hoàn thành:

```text
Docker installation
Dockerfile
Docker Image
Docker Container
Docker Volume
Docker Compose
Environment variables
Healthcheck
Logs
Docker exec
Pytest inside Docker
Persistent SQLite database
```