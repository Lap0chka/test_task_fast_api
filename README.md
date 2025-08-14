# 📚 Book Management System

**Goal** — Develop a scalable and robust book management system using **FastAPI** and **PostgreSQL**.  
This project goes beyond basic CRUD operations, focusing on architecture, optimization, and testing skills.

---

## 🚀 Tech Stack
- **FastAPI** — modern Python framework for building APIs
- **PostgreSQL** — primary database
- **SQLAlchemy 2.0 ORM (async)** — database interaction
- **Pydantic v2** — data validation
- **Alembic** — database migrations
- **asyncpg** — async PostgreSQL driver
- **Bcrypt** — password hashing
- **JWT (OAuth2)** — authentication & authorization

---

## 📂 Project Structure
```
backend/
├── alembic/              # Database migrations
├── books/                # Models, schemas, services, and routes for books
├── authors/              # Models, schemas, services, and routes for authors
├── auth/                 # Registration, login, JWT
├── core/                 # Config, DB, DI setup
├── tests/                # Tests
└── main.py               # Entry point
```

---

## 🗄️ Database Schema

- **books**
  - `id` (PK)
  - `title`
  - `published_year`
  - `genres` (ARRAY)
  - timestamps

- **authors**
  - `id` (PK)
  - `name`
  - timestamps

- **book_authors** (many-to-many)
  - `book_id` (FK → books)
  - `author_id` (FK → authors)

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/book-management-system.git
cd book-management-system
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables in `.env`
```env
DEBUG=True
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/books_db
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Start PostgreSQL (locally or via Docker)
```bash
docker run --name books-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=books_db -p 5432:5432 -d postgres:15
```

### 6. Run database migrations
```bash
alembic upgrade head
```

### 7. Start the application
```bash
uvicorn main:app --reload
```

---

## 🔑 Authentication
JWT tokens are issued after logging in.  
Uses **OAuth2PasswordBearer**.  

Endpoints:
- `POST /auth/register` — create a new user
- `POST /auth/login` — get JWT token

---

## 📌 API Endpoints

### Books
| Method | URL                              | Description                                       |
|--------|----------------------------------|---------------------------------------------------|
| **POST** | `/api/v1/books`                  | Add a new book *(authenticated only)*             |
| **POST** | `/api/v1/author`                 | Add a new author *(authenticated only)*           |
| **GET** | `/api/v1/books`                  | Get all books with pagination, sorting, filtering |
| **GET** | `/api/v1/books/{book_id}`        | Get a book by ID                                  |
| **PUT** | `/api/v1/books/{book_id}`        | Update a book *(authenticated only)*              |
| **DELETE** | `/api/v1/books/{book_id}`        | Delete a book *(authenticated only)*              |
| **POST** | `/api/v1/books/bulk-upload`      | Upload books from JSON *(authenticated only)*     |
| **GET** | `/api/v1/books/search?query=...` | Search by title or author (fuzzy search)          |

### Auth
| Method | URL              | Description          |
|--------|------------------|----------------------|
| **POST** | `/auth/register` | User registration    |
| **POST** | `/auth/login`    | User login (get JWT) |
| **POST** | `/auth/logout`   | User kogout (get JWT) |
| **POST** | `/auth/refres`   | Refresh JWT          |

---

## 🔍 Fuzzy Search
Example:
```http
GET /api/v1/books/search?query=Harry%20Potter
```
Matches:
- "Harry Potter and the Sorcerer's Stone"
- "Harry Potter and the Chamber of Secrets"

---

## ✅ Data Validation
- **title**, **author_names** — non-empty strings
- **published_year** — 1800 ≤ year ≤ current year
- **genres** — from predefined list (`Fiction`, `Non-Fiction`, `Science`, ...)

---

## 🛡️ Authorization
- All POST, PUT, DELETE endpoints are protected with JWT.
- Permission check example:
```python
class CanReadBooks(AbstractPermissionService):
    async def validate_permission(self):
        if not self.user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        if not self.user.is_active:
            raise HTTPException(status_code=403, detail="Inactive user")
```

---


---

## 📜 License
MIT License


📚 Books API

FastAPI application for a book catalog with:
	•	Search by title and authors (case-insensitive, fuzzy search)
	•	CRUD for books and authors (many-to-many relationship)
	•	Bulk book upload from JSON
	•	PostgreSQL + SQLAlchemy (async)
	•	Docker / docker-compose support

⸻

🚀 Quick Start

1) Clone and set up environment

git clone <repo-url>
cd <repo-folder>
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

2) Create .env file

DEBUG=False
SECRET_KEY_JWT=my-secret-key
ALGORITHM_JWT=HS256

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=books_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432


⸻

🐳 Run with Docker

Option A: docker-compose (recommended for local dev)

docker-compose up -d --build

Option B: plain Docker

docker build -t books-api .
docker run --env-file .env -p 8000:8000 books-api


⸻

🧪 Run locally without Docker

uvicorn app.main:app --reload

	•	Swagger UI: http://localhost:8000/docs
	•	ReDoc: http://localhost:8000/redoc

⸻

🗄️ Database & Migrations

Using Alembic:

alembic revision -m "init tables"
alembic upgrade head

For fuzzy search:

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;


⸻

🔌 API Examples

Create a book

POST /api/v1/books/

{
  "title": "Good Omens",
  "author_names": ["Neil Gaiman", "Terry Pratchett"],
  "genres": ["Fiction"],
  "published_year": 1990
}

Search books

GET /api/v1/books/search?query=Harry%20Potter&limit=10&offset=0

Bulk upload

POST /api/v1/books/bulk-upload with JSON file:

[
  {"title": "Harry Potter", "authors": ["J.K. Rowling"], "published_year": 1997},
  {"title": "Good Omens", "authors": ["Neil Gaiman", "Terry Pratchett"], "published_year": 1990}
]


⸻

🧹 pre-commit Hooks

pip install pre-commit
pre-commit install
pre-commit run --all-files


⸻


📄 License

Specify your license here.