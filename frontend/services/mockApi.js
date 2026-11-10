// Serviço simulado. Na Sprint 3 estas funções passam a chamar a API FastAPI.

const esperar = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const INSTRUCOES = {
  reforco: "Leia com calma e siga as dicas de cada questão.",
  padrao: "Responda com suas palavras e justifique quando pedido.",
  avancado: "Analise cada situação e justifique suas escolhas.",
  adaptada: "Leia uma questão por vez, com calma. Responda no espaço indicado.",
};

function enunciados(nivel, tema) {
  const modelos = {
    reforco: [
      `Com suas palavras, explique o que é ${tema}. Use uma frase curta.`,
      `Dê um exemplo simples de ${tema} e explique por que ele é um bom exemplo.`,
      `Complete: "${tema} é importante porque ______."`,
    ],
    padrao: [
      `Explique o conceito de ${tema} e cite um exemplo do dia a dia.`,
      `Resolva a situação-problema sobre ${tema} apresentada em aula, justificando cada etapa.`,
      `Compare dois exemplos de ${tema} e aponte uma diferença entre eles.`,
    ],
    avancado: [
      `Analise uma situação nova em que ${tema} se aplica e proponha uma solução.`,
      `Elabore um problema original sobre ${tema} e resolva-o.`,
      `Aponte uma limitação de ${tema} e discuta como contorná-la.`,
    ],
    adaptada: [
      `Escreva uma frase sobre ${tema}.`,
      `Dê um exemplo de ${tema}. Escreva em uma linha.`,
      `Escreva uma palavra que você lembra sobre ${tema}.`,
    ],
  };
  return modelos[nivel];
}

function montarQuestao(numero, enunciado, nivel, tipo, material) {
  const multipla = tipo === "multipla_escolha" || (tipo === "mista" && numero % 2 === 1);
  const texto = material ? `${enunciado} (com base no material do professor)` : enunciado;
  if (!multipla) return { numero, enunciado: texto };
  const alternativas = ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"];
  return { numero, enunciado: texto, alternativas: nivel === "adaptada" ? alternativas.slice(0, 3) : alternativas };
}

export async function gerarAtividade({ disciplina, serie, tema, quantidade, niveis, tipo = "mista", material = "" }) {
  await esperar(1500);

  const versoes = niveis.map((nivel) => {
    const total = nivel === "adaptada" ? Math.min(quantidade, 3) : quantidade;
    const modelos = enunciados(nivel, tema);
    const questoes = Array.from({ length: total }, (_, i) =>
      montarQuestao(i + 1, modelos[i % modelos.length], nivel, tipo, material)
    );
    return {
      nivel,
      instrucoes: INSTRUCOES[nivel],
      questoes,
      gabarito: questoes.map((q) => ({
        numero: q.numero,
        resposta: q.alternativas
          ? "Alternativa B (exemplo)"
          : `Resposta pessoal. Espera-se que o aluno mencione os pontos principais de ${tema}.`,
      })),
    };
  });

  return { gerada: Date.now(), titulo: tema, disciplina, serie, versoes };
}
