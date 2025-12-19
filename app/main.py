from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.routes import router as api_router
from app.domain.exceptions import AccountNotFound, DomainError, InsufficientFunds, InvalidTransferAmount
from app.infra.db import ENGINE
from app.infra.orm import Base


def create_app() -> FastAPI:
    app = FastAPI(title="Unit of Work demo", version="0.1.0")

    @app.on_event("startup")
    def _startup() -> None:
        # Simple demo approach (no migrations): create tables if missing.
        Base.metadata.create_all(bind=ENGINE)

    @app.exception_handler(AccountNotFound)
    def _account_not_found_handler(_, exc: AccountNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InsufficientFunds)
    def _insufficient_funds_handler(_, exc: InsufficientFunds):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidTransferAmount)
    def _invalid_amount_handler(_, exc: InvalidTransferAmount):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(DomainError)
    def _domain_error_handler(_, exc: DomainError):
        # fallback for other domain errors
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    app.include_router(api_router)
    return app


app = create_app()

