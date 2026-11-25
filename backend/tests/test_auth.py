import pytest
from fastapi.testclient import TestClient

from sqlmodel import Session, select

from app.auth import seguranca
from app.config import settings
from app.main import app
from app.models import Usuario

client = TestClient(app)

DADOS = {"nome": "Professora Ana", "email": "ana@escola.com", "senha": "segredo123"}
PEDIDO = {
    "disciplina": "Matemática",
    "serie": "6º ano",
    "tema": "soma de frações",
    "quantidade": 2,
    "niveis": ["reforco"],
}


def _entrar(dados=DADOS) -> dict:
    client.post("/auth/cadastro", json=dados)
    token = client.post("/auth/login", json={"email": dados["email"], "senha": dados["senha"]}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_cadastro_e_login():
    cadastro = client.post("/auth/cadastro", json=DADOS)
    assert cadastro.status_code == 201
    corpo = cadastro.json()
    assert corpo["email"] == "ana@escola.com" and "senha" not in corpo

    login = client.post("/auth/login", json={"email": DADOS["email"], "senha": DADOS["senha"]})
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer" and login.json()["access_token"]


def test_senha_nao_e_guardada_em_texto(banco):
    client.post("/auth/cadastro", json=DADOS)
    with Session(banco) as sessao:
        guardada = sessao.exec(select(Usuario).where(Usuario.email == "ana@escola.com")).first().senha_hash
    assert guardada != DADOS["senha"] and guardada.startswith("pbkdf2_sha256$")


def test_email_repetido_retorna_409():
    client.post("/auth/cadastro", json=DADOS)
    repetido = client.post("/auth/cadastro", json={**DADOS, "email": "ANA@escola.com"})
    assert repetido.status_code == 409


def test_dados_de_cadastro_invalidos():
    assert client.post("/auth/cadastro", json={**DADOS, "senha": "123"}).status_code == 422
    assert client.post("/auth/cadastro", json={**DADOS, "email": "sem-arroba"}).status_code == 422


def test_login_com_senha_errada():
    client.post("/auth/cadastro", json=DADOS)
    resposta = client.post("/auth/login", json={"email": DADOS["email"], "senha": "errada123"})
    assert resposta.status_code == 401


def test_login_com_email_inexistente():
    resposta = client.post("/auth/login", json={"email": "ninguem@escola.com", "senha": "segredo123"})
    assert resposta.status_code == 401


def test_rotas_exigem_token():
    assert client.get("/atividades").status_code == 401
    assert client.post("/atividades/gerar", json=PEDIDO).status_code == 401
    assert client.get("/atividades/1").status_code == 401
    assert client.delete("/atividades/1").status_code == 401


def test_token_invalido_retorna_401():
    resposta = client.get("/atividades", headers={"Authorization": "Bearer token-falso"})
    assert resposta.status_code == 401


def test_token_expirado_retorna_401():
    client.post("/auth/cadastro", json=DADOS)
    expirado = seguranca.criar_token(1, expira_minutos=-1)
    resposta = client.get("/auth/eu", headers={"Authorization": f"Bearer {expirado}"})
    assert resposta.status_code == 401


def test_usuario_logado():
    cabecalho = _entrar()
    resposta = client.get("/auth/eu", headers=cabecalho)
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Professora Ana"


def test_atividades_sao_privadas_por_usuario():
    ana = _entrar()
    bruno = _entrar({"nome": "Professor Bruno", "email": "bruno@escola.com", "senha": "segredo456"})

    gerada = client.post("/atividades/gerar", json=PEDIDO, headers=ana).json()
    salva = client.post("/atividades", json=gerada, headers=ana)
    assert salva.status_code == 201
    id_ = salva.json()["id"]

    assert len(client.get("/atividades", headers=ana).json()) == 1
    assert client.get("/atividades", headers=bruno).json() == []
    assert client.get(f"/atividades/{id_}", headers=bruno).status_code == 404
    assert client.delete(f"/atividades/{id_}", headers=bruno).status_code == 404
    assert client.delete(f"/atividades/{id_}", headers=ana).status_code == 204


def test_sem_segredo_jwt_retorna_503(monkeypatch):
    client.post("/auth/cadastro", json=DADOS)
    monkeypatch.setattr(settings, "jwt_secret", "")
    resposta = client.post("/auth/login", json={"email": DADOS["email"], "senha": DADOS["senha"]})
    assert resposta.status_code == 503
