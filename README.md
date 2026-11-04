# nivela-ai

Sistema web com IA que gera atividades em diferentes níveis de aprendizagem para professores da educação básica.

## O problema

Uma mesma turma reúne estudantes com defasagens, estudantes com deficiência e estudantes que já dominam o conteúdo. Produzir atividades adequadas a todos esses perfis exige tempo, planejamento e recursos que o professor nem sempre tem.

> Origem: ideia 10 da lista do cliente (professor Ricardo), "Dificuldade de produzir atividades para diferentes níveis de aprendizagem".

## A solução

O professor informa **disciplina, série e tema**, e o **nivela-ai** gera a mesma atividade em quatro versões, com gabarito:

| Nível | Descrição |
|---|---|
| Reforço | Linguagem mais simples, com passo a passo |
| Padrão | Adequada ao nível da série |
| Avançado | Desafios para quem já domina o conteúdo |
| Adaptada | Frases curtas, mais apoio no texto e menos itens, para estudantes com deficiência |

O professor sempre **revisa e edita** o resultado antes de salvar ou imprimir.

## Funcionalidades (MVP)

- Cadastro e login do professor
- Geração de atividades por nível com IA
- Edição manual das versões geradas
- Salvar, listar e excluir atividades
- Exportar em PDF / imprimir

## Fora do escopo (trabalhos futuros)

- Correção automática de respostas
- Integração com o RCO
- Banco de questões
- Perfis de turma ou aluno

## Tecnologias

- **Front-end:** _(definir: React ou HTML/JS)_
- **Back-end:** _(definir: Node ou Python)_
- **IA:** API de modelo de linguagem
- **Banco de dados:** _(definir: SQLite ou Firebase)_

## Como rodar o projeto

> Preencher quando houver código.

```bash
# 1. Clonar o repositório
git clone https://github.com/<usuario>/nivela-ai.git
cd nivela-ai

# 2. Criar o arquivo .env com a chave da API (nunca versionar)
cp .env.example .env

# 3. Instalar dependências e executar
# (comandos a definir conforme a tecnologia escolhida)
```

## Documentação

Os artefatos de cada sprint ficam na pasta [`docs/`](docs/).

- [Backlog do produto](docs/backlog.md)

## Equipe

- Rodrigo Gomes 
- Plinio Koiama
- Gavriel Takeshi

**Cliente:** professor Ricardo
