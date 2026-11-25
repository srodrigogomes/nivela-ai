from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select

from app.db import get_session
from app.main import app
from app.models import Usuario, Versao

client = TestClient(app)

DADOS = {"nome": "Professora Ana", "email": "ana@escola.com", "senha": "segredo123"}
PEDIDO = {"disciplina": "Matemática", "serie": "6º ano", "tema": "soma de frações", "quantidade": 2, "niveis": ["reforco"]}


def _entrar() -> dict:
    client.post("/auth/cadastro", json=DADOS)
    token = client.post("/auth/login", json={"email": DADOS["email"], "senha": DADOS["senha"]}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _salvar(cabecalho: dict) -> int:
    gerada = client.post("/atividades/gerar", json=PEDIDO, headers=cabecalho).json()
    return client.post("/atividades", json=gerada, headers=cabecalho).json()["id"]


def _banco_em_arquivo(caminho):
    motor = create_engine(f"sqlite:///{caminho.as_posix()}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(motor)

    def sessao():
        with Session(motor) as s:
            yield s

    app.dependency_overrides[get_session] = sessao
    return motor


def test_dados_continuam_depois_de_reiniciar(tmp_path):
    arquivo = tmp_path / "teste.db"
    primeiro = _banco_em_arquivo(arquivo)
    cabecalho = _entrar()
    id_ = _salvar(cabecalho)
    primeiro.dispose()  # a API "reinicia": conexão nova, mesmo arquivo de banco

    segundo = _banco_em_arquivo(arquivo)
    login = client.post("/auth/login", json={"email": DADOS["email"], "senha": DADOS["senha"]})
    assert login.status_code == 200  # a conta continua existindo
    lista = client.get("/atividades", headers=cabecalho).json()
    assert [a["id"] for a in lista] == [id_]  # e a atividade também
    segundo.dispose()


def test_relacionamentos_usuario_atividade_versao(banco):
    _salvar(_entrar())
    with Session(banco) as sessao:
        usuario = sessao.exec(select(Usuario)).first()
        assert len(usuario.atividades) == 1
        assert usuario.atividades[0].versoes[0].nivel == "reforco"


def test_excluir_atividade_apaga_as_versoes(banco):
    cabecalho = _entrar()
    id_ = _salvar(cabecalho)
    with Session(banco) as sessao:
        assert len(sessao.exec(select(Versao)).all()) == 1
    assert client.delete(f"/atividades/{id_}", headers=cabecalho).status_code == 204
    with Session(banco) as sessao:
        assert sessao.exec(select(Versao)).all() == []


def test_saude_confere_o_banco():
    assert client.get("/saude").json() == {"banco": "ok"}
