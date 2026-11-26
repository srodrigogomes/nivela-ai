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

## Épico 6: Personalização da geração

| ID | História de usuário | Prioridade |
|---|---|---|
| US15 | Como professor, quero escolher se as questões serão de alternativas, abertas ou mistas para adequar a atividade à minha aula. | Alta |
| US16 | Como professor, quero colar um material de apoio para que a IA crie as questões com base no que ensinei. | Alta |
| US17 | Como professor, quero anexar um arquivo de texto (.txt ou .md) como material de apoio para não precisar copiar e colar. | Média |
| US18 | Como professor, quero definir quantas questões serão geradas por versão (de 1 a 10). | Alta (já existia no formulário) |

**Critérios de aceite (US15 e US16):**
- Com "só abertas", nenhuma questão tem alternativas; com "só alternativas", todas têm
- O material de apoio é opcional e limitado a 8000 caracteres
- A API devolve erro 422 para tipo inválido ou material acima do limite

## Épico 7: Segurança e integração com a API

| ID | História de usuário | Prioridade |
|---|---|---|
| US19 | Como professor, quero que minhas atividades fiquem acessíveis só para mim, protegidas por login. | Alta |
| US20 | Como professor, quero continuar logado ao recarregar a página e poder sair quando eu quiser. | Média |
| US21 | Como professor, quero ver um aviso de carregamento e mensagens de erro claras quando a API demorar ou falhar. | Alta |
| US22 | Como equipe, queremos que o frontend use a API publicada, com a URL e o CORS configurados por variáveis de ambiente. | Alta |

**Critérios de aceite:**
- Sem token, as rotas de atividades respondem 401
- Um professor não vê nem exclui atividades de outro
- A senha é guardada somente como hash
- O frontend não usa mais dados mockados

## Épico 8: Persistência e ajuda ao usuário

| ID | História de usuário | Prioridade |
|---|---|---|
| US23 | Como professor, quero que minha conta e minhas atividades continuem existindo depois que o sistema reinicia. | Alta |
| US24 | Como professor, quero uma central de ajuda dentro do sistema para tirar dúvidas sem sair da tela. | Média |
| US25 | Como professor, quero um manual do usuário para aprender os fluxos principais. | Alta |
| US26 | Como equipe, queremos que a API tente de novo sozinha quando o serviço de IA estiver sobrecarregado. | Média |

**Critérios de aceite (US23):**
- Contas e atividades ficam em um banco de dados hospedado (PostgreSQL)
- Depois de reiniciar a API, o login e a lista de atividades continuam funcionando
- Excluir uma atividade apaga também as suas versões

## Requisitos não funcionais

- **RNF01:** a chave da API de IA não pode ficar exposta no front-end nem no repositório
- **RNF02:** a geração deve responder em tempo razoável, com indicador de carregamento
- **RNF03:** a interface deve funcionar em celular e computador
- **RNF04:** nenhum dado pessoal de estudantes é armazenado

## Sugestão de divisão por sprint

| Sprint | Entregas |
|---|---|
| Sprint 1 | Documentação, README, backlog, protótipo das telas |
| Sprint 2 | US01 a US04 (formulário, chamada à IA, resultado) e US15 a US18 (tipo de questão e material de apoio) |
| Sprint 3 | US13 e US14 (cadastro e login com JWT), US19 a US22 (rotas protegidas, integração com a API, carregamento e erro) e US08 a US11 (salvar, listar, abrir e excluir pela API) |
| Sprint 4 | US23 a US26 (banco de dados, central de ajuda, manual do usuário e tentativas automáticas da IA) e a entrega final |
