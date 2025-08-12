# Math Microservice

A simple FastAPI-based microservice that exposes three endpoints for common math operations and logs every request/response pair into PostgreSQL.

## 📦 Features

- **`POST /api/v1/power`** — raise a base to an exponent  
- **`POST /api/v1/fibonacci`** — compute the _n_th Fibonacci number  
- **`POST /api/v1/factorial`** — compute _n_!  
- **Request logging** in a `request_logs` table (path, payload, response, timestamp) via background tasks  
- **Async** database access with SQLAlchemy + AsyncPG  
- **Alembic** migrations to version your schema  
- **Pytest**-based unit & integration tests  

---

## 🚀 Getting Started

### Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)  
- [Docker](https://docs.docker.com/get-docker/) (for Postgres)  

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd math-microservice
python -m venv .venv
# Windows PowerShell
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
