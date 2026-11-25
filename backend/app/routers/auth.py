from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.auth.dependencias import get_usuario_atual
from app.auth.seguranca import criar_token, hash_senha, verificar_senha
from app.db import get_session
from app.models import Usuario
from app.schemas import CadastroIn, LoginIn, Token, UsuarioOut
from app.services import usuarios

router = APIRouter(prefix="/auth", tags=["Autenticação"])


def _publico(usuario: Usuario) -> UsuarioOut:
    return UsuarioOut(id=usuario.id, nome=usuario.nome, email=usuario.email)


@router.post("/cadastro", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED, summary="Criar conta")
def cadastrar(dados: CadastroIn, session: Session = Depends(get_session)):
    if usuarios.buscar_por_email(session, dados.email) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe uma conta com este e-mail.")
    try:
        usuario = usuarios.criar(session, dados.nome, dados.email, hash_senha(dados.senha))
    except IntegrityError:
        session.rollback()  # dois cadastros ao mesmo tempo com o mesmo e-mail
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe uma conta com este e-mail.")
    return _publico(usuario)


@router.post("/login", response_model=Token, summary="Entrar e receber o token JWT")
def entrar(dados: LoginIn, session: Session = Depends(get_session)):
    usuario = usuarios.buscar_por_email(session, dados.email)
    if usuario is None or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-mail ou senha incorretos.")
    return Token(access_token=criar_token(usuario.id))


@router.get("/eu", response_model=UsuarioOut, summary="Dados do usuário logado")
def usuario_logado(usuario: Usuario = Depends(get_usuario_atual)):
    return _publico(usuario)
