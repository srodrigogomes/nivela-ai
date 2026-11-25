from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from app import models  # noqa: F401  (registra as tabelas no SQLModel)
from app.config import settings


def _normalizar_url(url: str) -> str:
    # Alguns provedores entregam "postgres://", que o SQLAlchemy não aceita.
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://"):]
    return url


def criar_motor(url: str):
    url = _normalizar_url(url)
    argumentos = {"check_same_thread": False} if url.startswith("sqlite") else {}
    # pool_pre_ping e pool_recycle evitam erros quando o banco hospedado fecha conexões ociosas
    return create_engine(url, pool_pre_ping=True, pool_recycle=300, connect_args=argumentos)


engine = criar_motor(settings.database_url)


def criar_tabelas() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
