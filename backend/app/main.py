from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import atividades

app = FastAPI(
    title="nivela-ai API",
    description="API que gera atividades em diferentes níveis de aprendizagem com IA, para professores da educação básica.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(atividades.router)


@app.get("/", tags=["Sistema"], summary="Status da API")
def raiz():
    return {"servico": "nivela-ai API", "status": "ok", "documentacao": "/docs"}
