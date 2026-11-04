from datetime import datetime, timezone
from itertools import count

from app.schemas import Atividade, AtividadeIn

# Armazenamento em memória (Sprint 2). Na Sprint 4 será substituído pelo banco via SQLModel.
_atividades: dict[int, Atividade] = {}
_proximo_id = count(1)


def listar() -> list[Atividade]:
    return sorted(_atividades.values(), key=lambda a: a.criadaEm, reverse=True)


def criar(dados: AtividadeIn) -> Atividade:
    atividade = Atividade(id=next(_proximo_id), criadaEm=datetime.now(timezone.utc), **dados.model_dump())
    _atividades[atividade.id] = atividade
    return atividade


def obter(atividade_id: int) -> Atividade | None:
    return _atividades.get(atividade_id)


def remover(atividade_id: int) -> bool:
    return _atividades.pop(atividade_id, None) is not None


def limpar() -> None:
    _atividades.clear()
