from dataclasses import dataclass
from itertools import count

from app.auth.seguranca import hash_senha
from app.config import settings


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha_hash: str


# Armazenamento em memória (Sprint 3). Na Sprint 4 será substituído pelo banco via SQLModel.
_por_email: dict[str, Usuario] = {}
_por_id: dict[int, Usuario] = {}
_proximo_id = count(1)


def criar(nome: str, email: str, senha_hash: str) -> Usuario:
    usuario = Usuario(id=next(_proximo_id), nome=nome, email=email, senha_hash=senha_hash)
    _por_email[usuario.email] = usuario
    _por_id[usuario.id] = usuario
    return usuario


def buscar_por_email(email: str) -> Usuario | None:
    return _por_email.get(email.strip().lower())


def buscar_por_id(usuario_id: int) -> Usuario | None:
    return _por_id.get(usuario_id)


def limpar() -> None:
    _por_email.clear()
    _por_id.clear()


def semear_demo() -> None:
    """Cria o usuário de demonstração, se DEMO_EMAIL e DEMO_SENHA estiverem configurados."""
    if not (settings.demo_email and settings.demo_senha):
        return
    email = settings.demo_email.strip().lower()
    if buscar_por_email(email) is None:
        criar(settings.demo_nome, email, hash_senha(settings.demo_senha))
