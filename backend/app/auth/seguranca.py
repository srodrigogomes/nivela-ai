import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from app.config import settings

ALGORITMO = "HS256"
ITERACOES = 310_000  # custo do PBKDF2 (os testes usam um valor menor)


def hash_senha(senha: str) -> str:
    """Gera o hash da senha com PBKDF2 e um sal aleatório. A senha original nunca é guardada."""
    sal = secrets.token_bytes(16)
    resumo = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, ITERACOES)
    return "pbkdf2_sha256${}${}${}".format(
        ITERACOES,
        base64.b64encode(sal).decode(),
        base64.b64encode(resumo).decode(),
    )


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        _, iteracoes, sal, resumo = senha_hash.split("$")
        calculado = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), base64.b64decode(sal), int(iteracoes)
        )
        return hmac.compare_digest(calculado, base64.b64decode(resumo))
    except (ValueError, TypeError):
        return False


def _segredo() -> str:
    if not settings.jwt_secret:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "JWT_SECRET não está configurado no servidor."
        )
    return settings.jwt_secret


def criar_token(usuario_id: int, expira_minutos: int | None = None) -> str:
    minutos = settings.jwt_expire_minutes if expira_minutos is None else expira_minutos
    agora = datetime.now(timezone.utc)
    payload = {"sub": str(usuario_id), "iat": agora, "exp": agora + timedelta(minutes=minutos)}
    return jwt.encode(payload, _segredo(), algorithm=ALGORITMO)


def decodificar_token(token: str) -> int | None:
    """Devolve o id do usuário se o token for válido; senão, None."""
    try:
        payload = jwt.decode(token, _segredo(), algorithms=[ALGORITMO])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None
