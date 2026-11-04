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
| `CORS_ORIGINS` | Origens permitidas, separadas por vírgula |

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
