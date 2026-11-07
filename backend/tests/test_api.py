import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.prompts import build_user_prompt
from app.schemas import GerarAtividadeIn
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


def _json_ia(com_alternativas: bool) -> str:
    questao = '{"numero":1,"enunciado":"2+2?"' + (',"alternativas":["3","4","5"]' if com_alternativas else "") + "}"
    return (
        '{"titulo":"Soma","versoes":[{"nivel":"reforco","instrucoes":"Leia",'
        '"questoes":[' + questao + '],"gabarito":[{"numero":1,"resposta":"4"}]}]}'
    )


def test_tipo_aberta_sem_alternativas():
    resposta = client.post("/atividades/gerar", json={**PEDIDO, "tipo": "aberta"})
    assert resposta.status_code == 200
    for versao in resposta.json()["versoes"]:
        assert all(q["alternativas"] is None for q in versao["questoes"])


def test_tipo_multipla_escolha_com_alternativas():
    resposta = client.post("/atividades/gerar", json={**PEDIDO, "tipo": "multipla_escolha"})
    assert resposta.status_code == 200
    for versao in resposta.json()["versoes"]:
        assert all(q["alternativas"] for q in versao["questoes"])


def test_tipo_invalido():
    assert client.post("/atividades/gerar", json={**PEDIDO, "tipo": "desenho"}).status_code == 422


def test_material_muito_grande():
    assert client.post("/atividades/gerar", json={**PEDIDO, "material": "x" * 8001}).status_code == 422


def test_prompt_inclui_material_e_tipo():
    dados = GerarAtividadeIn(**{**PEDIDO, "tipo": "aberta", "material": "Texto sobre frações."})
    prompt = build_user_prompt(dados)
    assert "<material>" in prompt and "Texto sobre frações." in prompt
    assert "abertas" in prompt


def test_prompt_sem_material_nao_tem_bloco():
    assert "<material>" not in build_user_prompt(GerarAtividadeIn(**PEDIDO))


def test_ia_multipla_escolha_sem_alternativas_retorna_502(monkeypatch):
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    monkeypatch.setattr(ia, "_chamar_gemini", lambda prompt: _json_ia(False))
    pedido = {**PEDIDO, "niveis": ["reforco"], "quantidade": 1, "tipo": "multipla_escolha"}
    assert client.post("/atividades/gerar", json=pedido).status_code == 502


def test_ia_aberta_descarta_alternativas(monkeypatch):
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    monkeypatch.setattr(ia, "_chamar_gemini", lambda prompt: _json_ia(True))
    pedido = {**PEDIDO, "niveis": ["reforco"], "quantidade": 1, "tipo": "aberta"}
    resposta = client.post("/atividades/gerar", json=pedido)
    assert resposta.status_code == 200
    assert resposta.json()["versoes"][0]["questoes"][0]["alternativas"] is None
