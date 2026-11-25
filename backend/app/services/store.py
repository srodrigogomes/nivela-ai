from datetime import datetime, timezone

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models import Atividade as AtividadeDB
from app.models import Versao as VersaoDB
from app.schemas import Atividade, AtividadeIn


def _em_utc(momento: datetime) -> datetime:
    """Garante data e hora em UTC, com fuso, venha o valor com ou sem fuso do banco."""
    if momento.tzinfo is None:
        return momento.replace(tzinfo=timezone.utc)
    return momento.astimezone(timezone.utc)


def _para_schema(atividade: AtividadeDB) -> Atividade:
    """Converte as linhas do banco para o formato que a API devolve (o mesmo do frontend)."""
    return Atividade(
        id=atividade.id,
        titulo=atividade.titulo,
        disciplina=atividade.disciplina,
        serie=atividade.serie,
        criadaEm=_em_utc(atividade.criada_em),
        versoes=[
            {"nivel": v.nivel, "instrucoes": v.instrucoes, "questoes": v.questoes, "gabarito": v.gabarito}
            for v in atividade.versoes
        ],
    )


def _buscar(session: Session, usuario_id: int, atividade_id: int) -> AtividadeDB | None:
    atividade = session.get(AtividadeDB, atividade_id)
    if atividade is None or atividade.usuario_id != usuario_id:
        return None  # inexistente ou de outro professor: tratado do mesmo jeito
    return atividade


def listar(session: Session, usuario_id: int) -> list[Atividade]:
    consulta = (
        select(AtividadeDB)
        .where(AtividadeDB.usuario_id == usuario_id)
        .order_by(AtividadeDB.criada_em.desc(), AtividadeDB.id.desc())
        .options(selectinload(AtividadeDB.versoes))
    )
    return [_para_schema(a) for a in session.exec(consulta).all()]


def criar(session: Session, usuario_id: int, dados: AtividadeIn) -> Atividade:
    corpo = dados.model_dump(mode="json")
    atividade = AtividadeDB(
        usuario_id=usuario_id,
        titulo=corpo["titulo"],
        disciplina=corpo["disciplina"],
        serie=corpo["serie"],
        versoes=[
            VersaoDB(
                nivel=v["nivel"],
                instrucoes=v["instrucoes"],
                questoes=v["questoes"],
                gabarito=v["gabarito"],
            )
            for v in corpo["versoes"]
        ],
    )
    session.add(atividade)
    session.commit()
    session.refresh(atividade)
    return _para_schema(atividade)


def obter(session: Session, usuario_id: int, atividade_id: int) -> Atividade | None:
    atividade = _buscar(session, usuario_id, atividade_id)
    return _para_schema(atividade) if atividade else None


def remover(session: Session, usuario_id: int, atividade_id: int) -> bool:
    atividade = _buscar(session, usuario_id, atividade_id)
    if atividade is None:
        return False
    session.delete(atividade)  # as versões saem junto (cascade)
    session.commit()
    return True
