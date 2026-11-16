# Frontend do nivela-ai

Next.js (App Router) com Tailwind CSS. O frontend conversa com a API do backend (FastAPI) por `services/api.js`, com login por token JWT.

## Como rodar

Requisitos: Node.js 20 ou superior.

```bash
cd frontend
npm install
npm run dev
```

Abra http://localhost:3000, crie uma conta na tela inicial e entre. O backend precisa estar rodando (veja o README da raiz).

## Configurar a URL da API

A URL vem da variável `NEXT_PUBLIC_API_URL`. Sem ela, o frontend usa `http://127.0.0.1:8000` (backend local).

- Local: crie o arquivo `frontend/.env.local` com `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000` (opcional).
- Vercel: em Settings, Environment Variables, defina `NEXT_PUBLIC_API_URL` com a URL do Render e faça um novo deploy (a variável é lida na hora do build).

## Versão estática

```bash
npm run build
```

O site estático é gerado na pasta `out/`.

## Estrutura

- `app/`: páginas (login, gerar atividade, minhas atividades)
- `components/`: componentes reutilizáveis (Button, Alert, FormField, LevelTabs, ActivityCard, etc.)
- `context/`: estado global (professor logado e token)
- `hooks/`: hooks personalizados (`useRequireAuth`)
- `services/`: chamadas à API (`api.js`)
- `data/`: opções do formulário
