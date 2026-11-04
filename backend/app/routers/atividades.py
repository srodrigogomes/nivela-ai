from fastapi import APIRouter, HTTPException, status

from app.schemas import Atividade, AtividadeIn, GerarAtividadeIn
from app.services import ia, store

router = APIRouter(prefix="/atividades", tags=["Atividades"])


@router.post(
    "/gerar",
    response_model=AtividadeIn,
    summary="Gerar atividade com IA",
    description="Recebe disciplina, série, tema, quantidade e níveis, e devolve a atividade em cada nível, com gabarito. Não salva.",
)
def gerar_atividade(dados: GerarAtividadeIn):
    try:
        return ia.gerar_atividade(dados)
    except ia.IANaoConfiguradaError as erro:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(erro))
    except ia.IAError as erro:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, str(erro))


@router.get("", response_model=list[Atividade], summary="Listar atividades salvas")
def listar_atividades():
    return store.listar()


@router.post("", response_model=Atividade, status_code=status.HTTP_201_CREATED, summary="Salvar atividade")
def salvar_atividade(dados: AtividadeIn):
    return store.criar(dados)


@router.get("/{atividade_id}", response_model=Atividade, summary="Buscar atividade por id")
def buscar_atividade(atividade_id: int):
    atividade = store.obter(atividade_id)
    if atividade is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Atividade não encontrada.")
    return atividade


@router.delete("/{atividade_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir atividade")
def excluir_atividade(atividade_id: int):
    if not store.remover(atividade_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Atividade não encontrada.")
