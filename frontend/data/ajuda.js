// Conteúdo da Central de ajuda. O manual do usuário em PDF usa o mesmo texto.

export const PRIMEIROS_PASSOS = [
  "Crie sua conta na tela inicial, informando nome, e-mail e uma senha com 6 ou mais caracteres.",
  "Em Gerar atividade, escolha a disciplina, a série, o número de questões (de 1 a 10) e escreva o tema ou a habilidade.",
  "Escolha o tipo de questão (mistas, só alternativas ou só abertas) e, se quiser, cole um material de apoio ou anexe um arquivo .txt ou .md.",
  "Marque os níveis que deseja (reforço, padrão, avançado e adaptada) e clique em Gerar atividade.",
  "Confira cada nível nas abas, junto com o gabarito, e revise o conteúdo.",
  "Clique em Salvar atividade para guardá-la na sua conta. Para consultar depois, abra Minhas atividades.",
];

export const NIVEIS_AJUDA = [
  { nome: "Reforço", texto: "Linguagem simples, enunciados curtos e passo a passo, para quem precisa retomar o conteúdo." },
  { nome: "Padrão", texto: "Atividade no nível esperado para a série." },
  { nome: "Avançado", texto: "Questões que pedem análise e aplicação em situações novas, para quem já domina o conteúdo." },
  { nome: "Adaptada", texto: "Frases curtas, uma ideia por questão e instruções claras, com no máximo 3 questões. É um ponto de partida que você ajusta conforme a necessidade de cada estudante." },
];

export const DICAS = [
  "Seja específico no tema. “Soma de frações com denominadores iguais” rende mais do que “frações”.",
  "Use o material de apoio para a IA seguir o que você ensinou em aula.",
  "Comece com poucas questões, confira o resultado e gere de novo, se precisar.",
  "Revise sempre. A IA escreve um rascunho, e a palavra final é sua.",
];

export const PERGUNTAS = [
  { p: "A IA errou uma questão ou o gabarito. E agora?", r: "Isso pode acontecer. Revise o conteúdo antes de usar e, se precisar, gere de novo com um tema mais específico ou com material de apoio." },
  { p: "Por que a geração demora?", r: "A IA leva alguns segundos para escrever. No primeiro acesso do dia, o servidor gratuito também pode levar até 1 minuto para acordar. Aguarde e tente de novo, se aparecer uma mensagem de erro." },
  { p: "Posso enviar um PDF como material de apoio?", r: "Ainda não. Hoje você pode colar o texto na caixa ou anexar um arquivo .txt ou .md, com até 8000 caracteres. Para um PDF, copie o trecho e cole o texto." },
  { p: "Posso editar a atividade no sistema?", r: "Ainda não. Nesta versão, selecione e copie o texto para o seu editor. Para imprimir, use Ctrl + P no navegador." },
  { p: "Onde ficam as atividades que salvei?", r: "Na sua conta, em Minhas atividades. Só você as vê, e elas continuam lá depois que você sai." },
  { p: "Esqueci minha senha.", r: "Esta versão ainda não tem recuperação de senha. Você pode criar uma nova conta com outro e-mail." },
  { p: "Posso colocar nomes ou dados de alunos?", r: "Não. Use apenas o conteúdo da aula. O sistema não foi feito para guardar dados pessoais de estudantes." },
  { p: "A atividade adaptada serve para qualquer estudante com deficiência?", r: "Ela é um ponto de partida, com linguagem mais simples e menos questões. Cada estudante tem necessidades diferentes, então ajuste o material conforme o seu conhecimento do caso." },
];
