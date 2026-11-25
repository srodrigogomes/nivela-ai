from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.auth.dependencias import get_usuario_atual
from app.db import get_session
from app.models import Usuario
from app.schemas import Atividade, AtividadeIn, GerarAtividadeIn
from app.services import ia, store

# Todas as rotas de atividades exigem login (token JWT no cabeçalho Authorization).
router = APIRouter(prefix="/atividades", tags=["Atividades"], dependencies=[Depends(get_usuario_atual)])


@router.post(
    "/gerar",
    response_model=AtividadeIn,
    summary="Gerar atividade com IA",
    description="Recebe disciplina, série, tema, quantidade, níveis, tipo de questão e material de apoio opcional, e devolve a atividade em cada nível, com gabarito. Não salva.",
)
def gerar_atividade(dados: GerarAtividadeIn):
    try:
        return ia.gerar_atividade(dados)
    except ia.IANaoConfiguradaError as erro:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(erro))
    except ia.IAError as erro:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, str(erro))


@router.get("", response_model=list[Atividade], summary="Listar minhas atividades salvas")
def listar_atividades(usuario: Usuario = Depends(get_usuario_atual), session: Session = Depends(get_session)):
    return store.listar(session, usuario.id)


@router.post("", response_model=Atividade, status_code=status.HTTP_201_CREATED, summary="Salvar atividade")
def salvar_atividade(
    dados: AtividadeIn,
    usuario: Usuario = Depends(get_usuario_atual),
    session: Session = Depends(get_session),
):
    return store.criar(session, usuario.id, dados)


@router.get("/{atividade_id}", response_model=Atividade, summary="Buscar atividade por id")
def buscar_atividade(
    atividade_id: int,
    usuario: Usuario = Depends(get_usuario_atual),
    session: Session = Depends(get_session),
):
    atividade = store.obter(session, usuario.id, atividade_id)
    if atividade is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Atividade não encontrada.")
    return atividade


@router.delete("/{atividade_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir atividade")
def excluir_atividade(
    atividade_id: int,
    usuario: Usuario = Depends(get_usuario_atual),
    session: Session = Depends(get_session),
):
    if not store.remover(session, usuario.id, atividade_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Atividade não encontrada.")
