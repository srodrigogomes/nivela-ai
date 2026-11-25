from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.auth.seguranca import decodificar_token
from app.db import get_session
from app.models import Usuario
from app.services import usuarios

esquema = HTTPBearer(auto_error=False, description="Token JWT recebido no login")


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(esquema),
    session: Session = Depends(get_session),
) -> Usuario:
    """Exige um token JWT válido e devolve o usuário dono dele."""
    erro = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Token ausente ou inválido. Faça login novamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credenciais is None:
        raise erro
    usuario_id = decodificar_token(credenciais.credentials)
    if usuario_id is None:
        raise erro
    usuario = usuarios.buscar_por_id(session, usuario_id)
    if usuario is None:
        raise erro
    return usuario
