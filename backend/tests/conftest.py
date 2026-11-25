import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app import models  # noqa: F401  (registra as tabelas)
from app.auth import seguranca
from app.config import settings
from app.db import get_session
from app.main import app


@pytest.fixture(autouse=True)
def banco(monkeypatch):
    """Banco SQLite em memória, novo a cada teste (o banco de produção nunca é tocado)."""
    motor = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(motor)

    def sessao():
        with Session(motor) as s:
            yield s

    app.dependency_overrides[get_session] = sessao
    monkeypatch.setattr(settings, "ai_provider", "mock")
    monkeypatch.setattr(settings, "jwt_secret", "segredo-de-teste")
    monkeypatch.setattr(seguranca, "ITERACOES", 1000)  # deixa os testes rápidos
    yield motor
    app.dependency_overrides.clear()
    motor.dispose()
