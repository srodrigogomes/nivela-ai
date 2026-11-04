export const mockActivities = [
  {
    id: 1,
    titulo: "Soma de frações com denominadores iguais",
    disciplina: "Matemática",
    serie: "6º ano",
    criadaEm: "2026-11-04T12:00:00Z",
    versoes: [
      {
        nivel: "reforco",
        instrucoes: "Siga o passo a passo: mantenha o denominador e some os numeradores.",
        questoes: [
          { numero: 1, enunciado: "Some 1/4 + 2/4. Passo 1: mantenha o denominador 4. Passo 2: some os numeradores 1 + 2." },
          { numero: 2, enunciado: "Calcule 3/8 + 2/8." },
        ],
        gabarito: [
          { numero: 1, resposta: "3/4" },
          { numero: 2, resposta: "5/8" },
        ],
      },
      {
        nivel: "padrao",
        instrucoes: "Resolva as questões e simplifique o resultado quando possível.",
        questoes: [
          { numero: 1, enunciado: "Calcule 5/9 + 2/9." },
          { numero: 2, enunciado: "Ana comeu 2/6 de uma pizza e Bruno comeu 3/6. Que fração da pizza foi comida?" },
        ],
        gabarito: [
          { numero: 1, resposta: "7/9" },
          { numero: 2, resposta: "5/6" },
        ],
      },
      {
        nivel: "avancado",
        instrucoes: "Resolva e justifique cada etapa do raciocínio.",
        questoes: [
          { numero: 1, enunciado: "Ana e Bruno comeram, juntos, 5/6 de uma pizza de 12 fatias. Que fração Carla comeu, se ela comeu o que restou? Quantas fatias foram?" },
          { numero: 2, enunciado: "Escreva uma situação do dia a dia que envolva 3/10 + 4/10 e resolva-a." },
        ],
        gabarito: [
          { numero: 1, resposta: "1/6, ou seja, 2 fatias" },
          { numero: 2, resposta: "7/10 (a situação criada é pessoal)" },
        ],
      },
      {
        nivel: "adaptada",
        instrucoes: "Leia uma questão por vez, com calma. Responda no espaço indicado.",
        questoes: [
          { numero: 1, enunciado: "Some 2/5 + 1/5. Escreva o resultado." },
          { numero: 2, enunciado: "Marque a resposta certa: 1/3 + 1/3 = ?", alternativas: ["1/6", "2/3", "2/6"] },
        ],
        gabarito: [
          { numero: 1, resposta: "3/5" },
          { numero: 2, resposta: "2/3" },
        ],
      },
    ],
  },
  {
    id: 2,
    titulo: "Simple Present",
    disciplina: "Língua Inglesa",
    serie: "8º ano",
    criadaEm: "2026-10-28T12:00:00Z",
    versoes: [
      {
        nivel: "padrao",
        instrucoes: "Complete as frases com a forma correta do verbo.",
        questoes: [
          { numero: 1, enunciado: "She ____ (work) in a hospital." },
          { numero: 2, enunciado: "They ____ (not / like) pizza." },
        ],
        gabarito: [
          { numero: 1, resposta: "works" },
          { numero: 2, resposta: "don't like" },
        ],
      },
      {
        nivel: "adaptada",
        instrucoes: "Escolha a opção certa e complete a frase.",
        questoes: [
          { numero: 1, enunciado: "He ____ soccer.", alternativas: ["play", "plays"] },
          { numero: 2, enunciado: "I ____ music. (like)" },
        ],
        gabarito: [
          { numero: 1, resposta: "plays" },
          { numero: 2, resposta: "like" },
        ],
      },
    ],
  },
  {
    id: 3,
    titulo: "Fotossíntese",
    disciplina: "Ciências",
    serie: "7º ano",
    criadaEm: "2026-10-21T12:00:00Z",
    versoes: [
      {
        nivel: "reforco",
        instrucoes: "Responda com frases curtas.",
        questoes: [
          { numero: 1, enunciado: "Em que parte da planta acontece a fotossíntese?" },
          { numero: 2, enunciado: "Que tipo de energia a planta usa na fotossíntese?" },
        ],
        gabarito: [
          { numero: 1, resposta: "Nas folhas, principalmente nos cloroplastos." },
          { numero: 2, resposta: "A energia da luz solar." },
        ],
      },
      {
        nivel: "padrao",
        instrucoes: "Responda com suas palavras.",
        questoes: [
          { numero: 1, enunciado: "Explique o papel da luz solar na fotossíntese." },
          { numero: 2, enunciado: "Cite dois produtos da fotossíntese." },
        ],
        gabarito: [
          { numero: 1, resposta: "A luz fornece a energia para transformar água e gás carbônico em glicose." },
          { numero: 2, resposta: "Glicose e gás oxigênio." },
        ],
      },
    ],
  },
];
