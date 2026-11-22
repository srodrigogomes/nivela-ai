# Autenticação com JWT

## Como funciona (em linguagem simples)

1. O professor cria uma conta (`POST /auth/cadastro`). A senha vira um hash (PBKDF2 com sal), e a senha original nunca é guardada.
2. Ele entra (`POST /auth/login`). Se e-mail e senha conferem, a API entrega um **token JWT**, que funciona como um crachá digital assinado com um segredo que só o servidor conhece.
3. O frontend guarda o token e o envia em cada pedido, no cabeçalho `Authorization: Bearer <token>`.
4. A API confere a assinatura e a validade do token. Se estiver certo, descobre quem é o professor e responde só com os dados dele. Se não, responde **401**.

## Rotas

| Rota | Precisa de token? | O que faz |
|---|---|---|
| `POST /auth/cadastro` | Não | Cria a conta |
| `POST /auth/login` | Não | Devolve o token |
| `GET /auth/eu` | Sim | Mostra o usuário logado |
| `POST /atividades/gerar` | Sim | Gera a atividade com IA |
| `GET`, `POST` e `DELETE /atividades` | Sim | Listar, salvar e excluir as atividades do professor |

## Decisões de segurança

- **Hash de senha:** `hashlib.pbkdf2_hmac` (SHA-256, sal aleatório, 310 mil iterações), com comparação em tempo constante.
- **Segredo do token:** variável de ambiente `JWT_SECRET`, fora do repositório. Sem ela, o login responde 503.
- **Validade:** o token expira em 480 minutos (8 horas), configurável por `JWT_EXPIRE_MINUTES`.
- **Isolamento:** cada atividade pertence a um usuário, e quem não é o dono recebe 404.
- **Token no navegador:** fica no `localStorage`. É simples, mas um ataque de XSS poderia lê-lo. Em um sistema real, um cookie `HttpOnly` seria mais seguro.

## Limitação desta sprint

Contas e atividades ficam na **memória da API**. Quando a API reinicia (o plano gratuito do Render faz isso), elas se perdem e é preciso criar a conta de novo. Para a demonstração, existe o usuário opcional configurado por `DEMO_EMAIL` e `DEMO_SENHA`, recriado a cada reinício. O banco de dados (SQLModel) entra na Sprint 4 e resolve isso.
