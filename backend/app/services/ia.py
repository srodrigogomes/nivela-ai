import json

import httpx

from app.config import settings
from app.prompts import SYSTEM_PROMPT, build_user_prompt
from app.schemas import (
    AtividadeIn,
    GerarAtividadeIn,
    ItemGabarito,
    Nivel,
    Questao,
    Versao,
)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"


class IAError(Exception):
    """Falha ao obter uma resposta utilizável da IA."""


class IANaoConfiguradaError(IAError):
    """A chave da IA não foi configurada no servidor."""


def _chamar_gemini(prompt_usuario: str) -> str:
    if not settings.gemini_api_key:
        raise IANaoConfiguradaError("A chave GEMINI_API_KEY não está configurada no servidor.")

    corpo = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": prompt_usuario}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7},
    }
    try:
        resposta = httpx.post(
            GEMINI_URL.format(modelo=settings.gemini_model),
            headers={"x-goog-api-key": settings.gemini_api_key},
            json=corpo,
            timeout=settings.ai_timeout_seconds,
        )
    except httpx.HTTPError as erro:
        raise IAError("Não foi possível conectar ao serviço de IA.") from erro

    if resposta.status_code != 200:
        raise IAError(f"O serviço de IA respondeu com erro {resposta.status_code}.")

    try:
        return resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, ValueError) as erro:
        raise IAError("Resposta inesperada do serviço de IA.") from erro


def _extrair_json(texto: str) -> dict:
    inicio, fim = texto.find("{"), texto.rfind("}")
    if inicio == -1 or fim == -1:
        raise ValueError("A resposta não contém JSON.")
    return json.loads(texto[inicio : fim + 1])


def _normalizar(atividade: AtividadeIn, dados: GerarAtividadeIn) -> AtividadeIn:
    """Garante que a resposta da IA respeita o que o professor pediu."""
    por_nivel = {v.nivel: v for v in atividade.versoes}
    faltando = [n.value for n in dados.niveis if n not in por_nivel]
    if faltando:
        raise ValueError(f"Níveis ausentes na resposta: {faltando}")

    versoes = []
    for nivel in dados.niveis:
        versao = por_nivel[nivel]
        limite = min(3, dados.quantidade) if nivel == Nivel.adaptada else dados.quantidade
        questoes = versao.questoes[:limite]
        numeros = {q.numero for q in questoes}
        gabarito = [g for g in versao.gabarito if g.numero in numeros]
        if len(gabarito) < len(questoes):
            raise ValueError("Gabarito incompleto.")
        versoes.append(versao.model_copy(update={"questoes": questoes, "gabarito": gabarito}))
    return atividade.model_copy(update={"versoes": versoes})


def _gerar_simulada(dados: GerarAtividadeIn) -> AtividadeIn:
    versoes = []
    for nivel in dados.niveis:
        total = min(3, dados.quantidade) if nivel == Nivel.adaptada else dados.quantidade
        questoes = [
            Questao(numero=i, enunciado=f"[Simulado] Questão {i} sobre {dados.tema} ({nivel.value}).")
            for i in range(1, total + 1)
        ]
        versoes.append(
            Versao(
                nivel=nivel,
                instrucoes="[Simulado] Leia com atenção e responda.",
                questoes=questoes,
                gabarito=[ItemGabarito(numero=q.numero, resposta="[Simulado] Resposta de exemplo.") for q in questoes],
            )
        )
    return AtividadeIn(titulo=dados.tema, disciplina=dados.disciplina, serie=dados.serie, versoes=versoes)


def gerar_atividade(dados: GerarAtividadeIn) -> AtividadeIn:
    if settings.ai_provider == "mock":
        return _gerar_simulada(dados)

    prompt = build_user_prompt(dados)
    for _ in range(2):  # uma nova tentativa se a IA devolver algo inválido
        texto = _chamar_gemini(prompt)
        try:
            bruto = _extrair_json(texto)
            atividade = AtividadeIn.model_validate(
                {**bruto, "disciplina": dados.disciplina, "serie": dados.serie}
            )
            return _normalizar(atividade, dados)
        except ValueError:
            continue
    raise IAError("A IA devolveu uma resposta inválida. Tente gerar novamente.")
