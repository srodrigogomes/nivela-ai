import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.services import ia, store

client = TestClient(app)

PEDIDO = {
    "disciplina": "Matemática",
    "serie": "6º ano",
    "tema": "soma de frações",
    "quantidade": 3,
    "niveis": ["reforco", "adaptada"],
}


@pytest.fixture(autouse=True)
def ambiente(monkeypatch):
    monkeypatch.setattr(settings, "ai_provider", "mock")
    store.limpar()


def test_status():
    assert client.get("/").json()["status"] == "ok"


def test_gerar_atividade():
    resposta = client.post("/atividades/gerar", json=PEDIDO)
    assert resposta.status_code == 200
    versoes = resposta.json()["versoes"]
    assert [v["nivel"] for v in versoes] == ["reforco", "adaptada"]
    assert len(versoes[0]["questoes"]) == 3


def test_gerar_com_dados_invalidos():
    resposta = client.post("/atividades/gerar", json={**PEDIDO, "quantidade": 0, "niveis": []})
    assert resposta.status_code == 422


def test_salvar_listar_buscar_excluir():
    gerada = client.post("/atividades/gerar", json=PEDIDO).json()
    salva = client.post("/atividades", json=gerada)
    assert salva.status_code == 201
    id_ = salva.json()["id"]

    assert len(client.get("/atividades").json()) == 1
    assert client.get(f"/atividades/{id_}").status_code == 200
    assert client.delete(f"/atividades/{id_}").status_code == 204
    assert client.get(f"/atividades/{id_}").status_code == 404


def test_excluir_inexistente():
    assert client.delete("/atividades/999").status_code == 404


def test_sem_chave_retorna_503(monkeypatch):
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    monkeypatch.setattr(settings, "gemini_api_key", "")
    assert client.post("/atividades/gerar", json=PEDIDO).status_code == 503


def test_resposta_invalida_da_ia_retorna_502(monkeypatch):
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    monkeypatch.setattr(ia, "_chamar_gemini", lambda prompt: "isto não é json")
    assert client.post("/atividades/gerar", json=PEDIDO).status_code == 502


def test_resposta_valida_da_ia(monkeypatch):
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    texto = (
        '```json\n{"titulo":"Frações","versoes":['
        '{"nivel":"reforco","instrucoes":"Leia","questoes":[{"numero":1,"enunciado":"1/4+2/4"},'
        '{"numero":2,"enunciado":"3/8+2/8"},{"numero":3,"enunciado":"1/5+1/5"}],'
        '"gabarito":[{"numero":1,"resposta":"3/4"},{"numero":2,"resposta":"5/8"},{"numero":3,"resposta":"2/5"}]},'
        '{"nivel":"adaptada","instrucoes":"Leia","questoes":[{"numero":1,"enunciado":"2/5+1/5"}],'
        '"gabarito":[{"numero":1,"resposta":"3/5"}]}]}\n```'
    )
    monkeypatch.setattr(ia, "_chamar_gemini", lambda prompt: texto)
    resposta = client.post("/atividades/gerar", json=PEDIDO)
    assert resposta.status_code == 200
    assert resposta.json()["versoes"][0]["gabarito"][0]["resposta"] == "3/4"
