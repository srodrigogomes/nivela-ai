# Backend do nivela-ai

API em Python com FastAPI. Gera atividades em quatro níveis (reforço, padrão, avançado e adaptada) com IA. Nesta sprint os dados ficam em memória; o banco entra na Sprint 4.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Status da API |
| POST | `/atividades/gerar` | Gera a atividade com IA (não salva) |
| GET | `/atividades` | Lista as atividades salvas |
| POST | `/atividades` | Salva uma atividade |
| GET | `/atividades/{id}` | Busca uma atividade |
| DELETE | `/atividades/{id}` | Exclui uma atividade |

A documentação interativa fica em `/docs`.

## Banco de dados

Os dados ficam em um banco, via SQLModel (tabelas `usuario`, `atividade` e `versao`; veja [`docs/modelo-de-dados.md`](../docs/modelo-de-dados.md)). Sem `DATABASE_URL`, a API usa um arquivo SQLite local (`nivela.db`, ignorado pelo Git). Em produção, aponte `DATABASE_URL` para um PostgreSQL hospedado. As tabelas são criadas sozinhas quando a API inicia, e `GET /saude` confere a conexão.

## Autenticação

As rotas `/atividades` exigem login. Fluxo: `POST /auth/cadastro`, depois `POST /auth/login`, que devolve o token; envie-o no cabeçalho `Authorization: Bearer <token>`. No `/docs`, o botão **Authorize** faz isso. Detalhes em [`docs/autenticacao.md`](../docs/autenticacao.md).

Para gerar um segredo:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## Parâmetros do POST /atividades/gerar

| Campo | Tipo | Descrição |
|---|---|---|
| `disciplina` | texto | Disciplina da atividade |
| `serie` | texto | Série ou ano |
| `tema` | texto | Tema ou habilidade (mínimo de 3 caracteres) |
| `quantidade` | inteiro de 1 a 10 | Questões por versão (a versão adaptada tem no máximo 3) |
| `niveis` | lista | `reforco`, `padrao`, `avancado` e/ou `adaptada` |
| `tipo` | texto | `multipla_escolha`, `aberta` ou `mista` (padrão) |
| `material` | texto, opcional | Material de apoio do professor (até 8000 caracteres); a IA baseia as questões nele |

## Estrutura

- `app/main.py`: criação da aplicação e CORS
- `app/config.py`: configurações via variáveis de ambiente
- `app/schemas.py`: schemas Pydantic (mesmo formato dos dados do frontend)
- `app/prompts.py`: prompts enviados à IA
- `app/routers/atividades.py`: rotas
- `app/services/ia.py`: integração com a IA (Gemini) e validação da resposta
- `app/services/store.py`: armazenamento em memória
- `tests/`: testes automatizados

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `AI_PROVIDER` | `gemini` (padrão) ou `mock` (respostas simuladas, sem chave) |
| `GEMINI_API_KEY` | Chave da API do Google AI Studio |
| `GEMINI_MODEL` | Modelo usado (padrão `gemini-3.1-flash-lite`) |
| `CORS_ORIGINS` | Origens permitidas, separadas por vírgula (inclua a URL do frontend na Vercel) |
| `DATABASE_URL` | Endereço do banco. Local: `sqlite:///./nivela.db` (padrão). Produção: URL do PostgreSQL (Neon) |
| `JWT_SECRET` | Segredo que assina os tokens de login (obrigatório) |
| `JWT_EXPIRE_MINUTES` | Validade do token em minutos (padrão 480) |
| `DEMO_EMAIL`, `DEMO_SENHA`, `DEMO_NOME` | Usuário de demonstração opcional, recriado a cada reinício |

A chave fica só no `.env` (local) ou nas variáveis de ambiente da hospedagem. O `.env` não vai para o repositório.

## Rodar localmente (Windows, PowerShell)

Requisito: Python 3.11 ou superior.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edite o `.env` e coloque a chave em `GEMINI_API_KEY`. Para testar sem chave, use `AI_PROVIDER=mock`.

```powershell
uvicorn app.main:app --reload
```

Abra http://127.0.0.1:8000/docs.

## Testes

```powershell
pip install -r requirements-dev.txt
pytest
```

## Hospedagem (Render, plano gratuito)

1. Crie um **Web Service** a partir do repositório no GitHub.
2. **Root Directory:** `backend`
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Em **Environment**, adicione `GEMINI_API_KEY`, `AI_PROVIDER=gemini` e `CORS_ORIGINS` (com a URL do frontend na Vercel).

No plano gratuito a API "dorme" após alguns minutos sem uso e a primeira requisição demora. Abra a URL antes de apresentar.
