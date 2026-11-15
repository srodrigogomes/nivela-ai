from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencias import get_usuario_atual
from app.schemas import Atividade, AtividadeIn, GerarAtividadeIn
from app.services import ia, store
from app.services.usuarios import Usuario

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
def listar_atividades(usuario: Usuario = Depends(get_usuario_atual)):
    return store.listar(usuario.id)


@router.post("", response_model=Atividade, status_code=status.HTTP_201_CREATED, summary="Salvar atividade")
def salvar_atividade(dados: AtividadeIn, usuario: Usuario = Depends(get_usuario_atual)):
    return store.criar(usuario.id, dados)


@router.get("/{atividade_id}", response_model=Atividade, summary="Buscar atividade por id")
def buscar_atividade(atividade_id: int, usuario: Usuario = Depends(get_usuario_atual)):
    atividade = store.obter(usuario.id, atividade_id)
    if atividade is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Atividade não encontrada.")
    return atividade


@router.delete("/{atividade_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir atividade")
def excluir_atividade(atividade_id: int, usuario: Usuario = Depends(get_usuario_atual)):
    if not store.remover(usuario.id, atividade_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Atividade não encontrada.")
