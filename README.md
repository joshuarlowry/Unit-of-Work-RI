# Unit-of-Work-RI
This project demonstrates the **Unit of Work** pattern in a small **Python 3.12** **FastAPI** app using:

- **Service/use-case layer** to orchestrate workflows (application logic)
- **Domain objects** to hold business rules (e.g. “no overdraft”)
- **Repositories** to abstract persistence
- **SQLAlchemy + SQLite** as the backing data store
- **Docker + Compose** to run the API

## What “Unit of Work” means here
Each use-case executes inside a `UnitOfWork` that:

- Opens a database session/transaction
- Exposes repositories bound to that session
- Commits as a single atomic unit (or rolls back on error)

In this demo:

- **Domain rules** live in `app/domain/`
- **Orchestration** lives in `app/services/use_cases.py`
- **SQLAlchemy repositories + UoW** live in `app/infra/`
- **HTTP API** lives in `app/api/`

## Run
Start the API (SQLite DB persisted in a named volume):

```bash
docker compose up --build
```

API will be on `http://localhost:8000` and docs at `http://localhost:8000/docs`.

## API quick start
- `POST /accounts` creates an account
- `GET /accounts/{id}` fetches an account
- `POST /transfers` transfers money atomically between two accounts
