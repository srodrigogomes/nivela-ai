from app.schemas import GerarAtividadeIn, Nivel

SYSTEM_PROMPT = """Você é um assistente pedagógico para professores da educação básica brasileira (rede pública).
Sua tarefa é criar atividades escolares claras, corretas e adequadas à série informada.

Regras:
- Escreva em português do Brasil. Se a disciplina for Língua Inglesa, escreva as questões em inglês e as instruções em português.
- Mantenha o mesmo tema e objetivo de aprendizagem em todas as versões.
- Não invente fatos, datas, dados ou citações. Se não tiver certeza, simplifique.
- Não use nomes reais de pessoas.
- Toda questão deve ter uma resposta no gabarito.
- Responda APENAS com JSON válido, sem texto antes ou depois e sem blocos de markdown."""

ORIENTACOES = {
    Nivel.reforco: "linguagem simples, enunciados curtos, passo a passo, exemplos resolvidos quando útil.",
    Nivel.padrao: "adequada ao nível esperado para a série.",
    Nivel.avancado: "questões que exigem análise, aplicação em situações novas e raciocínio mais elaborado.",
    Nivel.adaptada: (
        "para estudantes com deficiência ou dificuldades de aprendizagem. Frases curtas e diretas, "
        "uma ideia por questão, vocabulário simples, no máximo 3 questões e instruções explícitas do que fazer."
    ),
}

FORMATO_JSON = """{
  "titulo": "string",
  "versoes": [
    {
      "nivel": "reforco | padrao | avancado | adaptada",
      "instrucoes": "string",
      "questoes": [
        { "numero": 1, "enunciado": "string", "alternativas": ["string"] }
      ],
      "gabarito": [
        { "numero": 1, "resposta": "string" }
      ]
    }
  ]
}
O campo "alternativas" só deve existir em questões de múltipla escolha."""


def build_user_prompt(dados: GerarAtividadeIn) -> str:
    niveis = "\n".join(f"- {n.value}: {ORIENTACOES[n]}" for n in dados.niveis)
    return f"""Crie uma atividade com os seguintes dados:

Disciplina: {dados.disciplina}
Série/ano: {dados.serie}
Tema ou habilidade: {dados.tema}
Número de questões por versão: {dados.quantidade}

Gere uma versão para cada nível abaixo, nesta ordem, usando exatamente estes identificadores no campo "nivel":
{niveis}

Formato de resposta (JSON):
{FORMATO_JSON}"""
