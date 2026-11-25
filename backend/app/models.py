from datetime import datetime, timezone

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel


def _agora() -> datetime:
    """Data e hora atuais em UTC, com fuso (o SQLModel mais novo exige isso)."""
    return datetime.now(timezone.utc)


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=80)
    email: str = Field(max_length=120, unique=True, index=True)
    senha_hash: str

    atividades: list["Atividade"] = Relationship(back_populates="usuario")


class Atividade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    titulo: str = Field(max_length=200)
    disciplina: str = Field(max_length=60)
    serie: str = Field(max_length=30)
    criada_em: datetime = Field(default_factory=_agora)

    usuario: Usuario | None = Relationship(back_populates="atividades")
    versoes: list["Versao"] = Relationship(
        back_populates="atividade",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "order_by": "Versao.id"},
    )


class Versao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    atividade_id: int = Field(foreign_key="atividade.id", index=True)
    nivel: str = Field(max_length=20)
    instrucoes: str
    questoes: list[dict] = Field(default_factory=list, sa_column=Column(JSON))
    gabarito: list[dict] = Field(default_factory=list, sa_column=Column(JSON))

    atividade: Atividade | None = Relationship(back_populates="versoes")
