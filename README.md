# Customer Management API

A RESTful API built with FastAPI and PostgreSQL to manage customer records. This project implements full CRUD operations, secure API key authentication, pagination, and database migrations using Alembic.

## 🚀 Features
- **CRUD Operations:** Create, Read, Update, and Delete customer records.
- **Authentication:** Protected endpoints using `X-API-Key` header validation.
- **Pagination:** Efficient data retrieval using `page` and `per_page` query parameters.
- **Error Handling:** Proper HTTP status codes (401 Unauthorized, 404 Not Found, 409 Conflict).
- **Database Migrations:** Managed via Alembic.
- **Bonus Challenge:** 
  - Search by customer name using a query parameter.
  - Database index added to the `email` column for optimized querying.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Validation:** Pydantic

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd customer-management-api
   git checkout feature/customer-api
