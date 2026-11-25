from sqlmodel import Session, select

from app.auth.seguranca import hash_senha
from app.config import settings
from app.models import Usuario


def criar(session: Session, nome: str, email: str, senha_hash: str) -> Usuario:
    usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def buscar_por_email(session: Session, email: str) -> Usuario | None:
    consulta = select(Usuario).where(Usuario.email == email.strip().lower())
    return session.exec(consulta).first()


def buscar_por_id(session: Session, usuario_id: int) -> Usuario | None:
    return session.get(Usuario, usuario_id)


def semear_demo(session: Session) -> None:
    """Cria o usuário de demonstração, se DEMO_EMAIL e DEMO_SENHA estiverem configurados."""
    if not (settings.demo_email and settings.demo_senha):
        return
    email = settings.demo_email.strip().lower()
    if buscar_por_email(session, email) is None:
        criar(session, settings.demo_nome, email, hash_senha(settings.demo_senha))
