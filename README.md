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
| Method | URL | Description |
|--------|-----|-------------|
| **POST** | `/api/v1/books` | Add a new book *(authenticated only)* |
| **GET** | `/api/v1/books` | Get all books with pagination, sorting, filtering |
| **GET** | `/api/v1/books/{book_id}` | Get a book by ID |
| **PUT** | `/api/v1/books/{book_id}` | Update a book *(authenticated only)* |
| **DELETE** | `/api/v1/books/{book_id}` | Delete a book *(authenticated only)* |
| **POST** | `/api/v1/books/bulk-upload` | Upload books from JSON *(authenticated only)* |
| **GET** | `/api/v1/books/search?query=...` | Search by title or author (fuzzy search) |

### Auth
| Method | URL | Description |
|--------|-----|-------------|
| **POST** | `/auth/register` | User registration |
| **POST** | `/auth/login` | User login (get JWT) |

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

## 🧪 Testing
```bash
pytest
```

---

## 📜 License
MIT License
