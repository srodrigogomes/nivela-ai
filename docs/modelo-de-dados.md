# Modelo de dados

O banco usa SQLModel. Em produção é um PostgreSQL hospedado (Neon); no computador, um arquivo SQLite criado automaticamente.

## Tabelas

**usuario**

| Coluna | Tipo | Observação |
|---|---|---|
| id | inteiro | chave primária |
| nome | texto (80) | |
| email | texto (120) | único, guardado em minúsculas |
| senha_hash | texto | hash PBKDF2; a senha original nunca é guardada |

**atividade**

| Coluna | Tipo | Observação |
|---|---|---|
| id | inteiro | chave primária |
| usuario_id | inteiro | chave estrangeira para usuario.id |
| titulo | texto (200) | |
| disciplina | texto (60) | |
| serie | texto (30) | |
| criada_em | data e hora | em UTC |

**versao**

| Coluna | Tipo | Observação |
|---|---|---|
| id | inteiro | chave primária |
| atividade_id | inteiro | chave estrangeira para atividade.id |
| nivel | texto | reforco, padrao, avancado ou adaptada |
| instrucoes | texto | |
| questoes | JSON | lista de questões (número, enunciado e alternativas) |
| gabarito | JSON | lista de respostas |

## Relacionamentos

- Um **usuário** tem várias **atividades** (1 para N).
- Uma **atividade** tem várias **versões**, uma por nível (1 para N).
- Excluir uma atividade apaga as suas versões (cascade).
- Um professor só acessa as atividades dele: quem não é o dono recebe 404.

## Por que questões e gabarito em JSON

As questões são geradas pela IA e sempre lidas junto com a versão. Guardá-las como JSON evita duas tabelas a mais, e o banco continua com as chaves e os relacionamentos que importam para a consulta.

## Onde está no código

- `backend/app/models.py`: as três tabelas
- `backend/app/db.py`: conexão e criação das tabelas
- `backend/app/services/store.py` e `usuarios.py`: consultas
