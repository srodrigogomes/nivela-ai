from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlmodel import Session

from app.config import settings
from app.db import criar_tabelas, engine, get_session
from app.routers import atividades, auth
from app.services import usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()  # cria as tabelas que ainda não existem
    with Session(engine) as sessao:
        usuarios.semear_demo(sessao)
    yield


app = FastAPI(
    title="nivela-ai API",
    description="API que gera atividades em diferentes níveis de aprendizagem com IA, para professores da educação básica.",
    version="0.4.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(atividades.router)


@app.get("/", tags=["Sistema"], summary="Status da API")
def raiz():
    return {"servico": "nivela-ai API", "status": "ok", "documentacao": "/docs"}


@app.get("/saude", tags=["Sistema"], summary="Confere a conexão com o banco de dados")
def saude(session: Session = Depends(get_session)):
    try:
        session.connection().execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(503, "Banco de dados indisponível.")
    return {"banco": "ok"}
