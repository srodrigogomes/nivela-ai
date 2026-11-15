from datetime import datetime, timezone
from itertools import count

from app.schemas import Atividade, AtividadeIn

# Armazenamento em memória (Sprint 3). Cada atividade pertence a um usuário.
# Na Sprint 4 será substituído pelo banco via SQLModel.
_atividades: dict[int, tuple[int, Atividade]] = {}
_proximo_id = count(1)


def listar(usuario_id: int) -> list[Atividade]:
    minhas = [atividade for dono, atividade in _atividades.values() if dono == usuario_id]
    return sorted(minhas, key=lambda a: a.criadaEm, reverse=True)


def criar(usuario_id: int, dados: AtividadeIn) -> Atividade:
    atividade = Atividade(id=next(_proximo_id), criadaEm=datetime.now(timezone.utc), **dados.model_dump())
    _atividades[atividade.id] = (usuario_id, atividade)
    return atividade


def obter(usuario_id: int, atividade_id: int) -> Atividade | None:
    item = _atividades.get(atividade_id)
    if item is None or item[0] != usuario_id:
        return None
    return item[1]


def remover(usuario_id: int, atividade_id: int) -> bool:
    if obter(usuario_id, atividade_id) is None:
        return False
    del _atividades[atividade_id]
    return True


def limpar() -> None:
    _atividades.clear()
