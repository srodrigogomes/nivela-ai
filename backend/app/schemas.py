from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Nivel(str, Enum):
    reforco = "reforco"
    padrao = "padrao"
    avancado = "avancado"
    adaptada = "adaptada"


class TipoQuestoes(str, Enum):
    multipla_escolha = "multipla_escolha"
    aberta = "aberta"
    mista = "mista"


MATERIAL_MAX = 8000  # caracteres do material de apoio


class Questao(BaseModel):
    numero: int = Field(ge=1)
    enunciado: str = Field(min_length=1)
    alternativas: list[str] | None = None


class ItemGabarito(BaseModel):
    numero: int = Field(ge=1)
    resposta: str = Field(min_length=1)


class Versao(BaseModel):
    nivel: Nivel
    instrucoes: str = Field(min_length=1)
    questoes: list[Questao] = Field(min_length=1)
    gabarito: list[ItemGabarito] = Field(min_length=1)


class GerarAtividadeIn(BaseModel):
    """Dados do formulário da tela Gerar atividade."""

    disciplina: str = Field(min_length=2, max_length=60)
    serie: str = Field(min_length=1, max_length=30)
    tema: str = Field(min_length=3, max_length=200)
    quantidade: int = Field(ge=1, le=10)
    niveis: list[Nivel] = Field(min_length=1)
    tipo: TipoQuestoes = TipoQuestoes.mista
    material: str | None = Field(default=None, max_length=MATERIAL_MAX)

    @field_validator("material")
    @classmethod
    def limpar_material(cls, material: str | None) -> str | None:
        if material is None:
            return None
        return material.strip() or None

    @field_validator("niveis")
    @classmethod
    def remover_repetidos(cls, niveis: list[Nivel]) -> list[Nivel]:
        return list(dict.fromkeys(niveis))


class AtividadeIn(BaseModel):
    """Atividade gerada ou enviada para salvar (mesmo formato usado no frontend)."""

    titulo: str = Field(min_length=1, max_length=200)
    disciplina: str = Field(min_length=1, max_length=60)
    serie: str = Field(min_length=1, max_length=30)
    versoes: list[Versao] = Field(min_length=1)


class Atividade(AtividadeIn):
    id: int
    criadaEm: datetime
