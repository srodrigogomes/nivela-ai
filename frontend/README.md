# Frontend do nivela-ai

Next.js (App Router) com Tailwind CSS. Nesta sprint os dados são simulados (mock): a geração de atividades fica em `services/mockApi.js` e a lista inicial em `data/mockActivities.js`.

## Como rodar

Requisitos: Node.js 20 ou superior.

```bash
cd frontend
npm install
npm run dev
```

Abra http://localhost:3000. Use qualquer e-mail válido e uma senha com 6 ou mais caracteres.

## Versão estática

```bash
npm run build
```

O site estático é gerado na pasta `out/`.

## Estrutura

- `app/`: páginas (login, gerar atividade, minhas atividades)
- `components/`: componentes reutilizáveis (Button, Alert, FormField, LevelTabs, ActivityCard, etc.)
- `context/`: estado global (professor logado e atividades)
- `hooks/`: hooks personalizados (`useRequireAuth`)
- `services/`: acesso a dados (hoje simulado)
- `data/`: dados mockados e opções do formulário
