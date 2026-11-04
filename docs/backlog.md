# Backlog do Produto: nivela-ai

**Persona:** professor da educação básica da rede pública, com pouco tempo para planejamento e turmas com níveis muito diferentes.

**Prioridade:** Alta / Média / Baixa

## Épico 1: Geração de atividades

| ID | História de usuário | Prioridade |
|---|---|---|
| US01 | Como professor, quero informar disciplina, série e tema para que o sistema gere uma atividade. | Alta |
| US02 | Como professor, quero escolher a quantidade de questões e os níveis desejados para controlar o que será gerado. | Alta |
| US03 | Como professor, quero receber a atividade em versões de reforço, padrão, avançada e adaptada para atender toda a turma. | Alta |
| US04 | Como professor, quero receber o gabarito de cada versão para corrigir com rapidez. | Alta |
| US05 | Como professor, quero regenerar uma versão específica caso não goste do resultado. | Média |

**Critérios de aceite (US03):**
- O sistema exibe uma versão por nível selecionado
- A versão adaptada usa frases curtas e menos itens
- Cada versão mantém o mesmo tema da atividade original

## Épico 2: Revisão e edição

| ID | História de usuário | Prioridade |
|---|---|---|
| US06 | Como professor, quero editar o texto gerado antes de salvar para ajustar à minha turma. | Alta |
| US07 | Como professor, quero copiar o conteúdo de uma versão para usar em outros materiais. | Média |

## Épico 3: Atividades salvas

| ID | História de usuário | Prioridade |
|---|---|---|
| US08 | Como professor, quero salvar a atividade para reutilizar depois. | Alta |
| US09 | Como professor, quero ver a lista das minhas atividades salvas. | Alta |
| US10 | Como professor, quero abrir uma atividade salva para consultar ou editar. | Média |
| US11 | Como professor, quero excluir atividades que não preciso mais. | Média |

## Épico 4: Exportação

| ID | História de usuário | Prioridade |
|---|---|---|
| US12 | Como professor, quero exportar a atividade em PDF para imprimir e reduzir o uso de telas pelos alunos. | Média |

## Épico 5: Acesso

| ID | História de usuário | Prioridade |
|---|---|---|
| US13 | Como professor, quero criar uma conta para ter minhas atividades guardadas. | Média |
| US14 | Como professor, quero entrar com e-mail e senha para acessar minhas atividades. | Média |

## Requisitos não funcionais

- **RNF01:** a chave da API de IA não pode ficar exposta no front-end nem no repositório
- **RNF02:** a geração deve responder em tempo razoável, com indicador de carregamento
- **RNF03:** a interface deve funcionar em celular e computador
- **RNF04:** nenhum dado pessoal de estudantes é armazenado

## Sugestão de divisão por sprint

| Sprint | Entregas |
|---|---|
| Sprint 1 | Documentação, README, backlog, protótipo das telas |
| Sprint 2 | US01 a US04 (formulário, chamada à IA, resultado) |
| Sprint 3 | US06 a US11, US13 e US14 (edição, salvar, login) |
| Sprint 4 | US05, US12 e polimento para a apresentação |
