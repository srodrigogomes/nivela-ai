// Chamadas à API (FastAPI). A URL vem da variável NEXT_PUBLIC_API_URL.
const BASE_URL = (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const TIMEOUT_MS = 90000; // o servidor gratuito pode levar cerca de 1 minuto para acordar

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

function montarMensagem(status, detalhe) {
  if (typeof detalhe === "string") return detalhe;
  if (Array.isArray(detalhe) && detalhe.length > 0) return detalhe.map((d) => d.msg).join(" ");
  return `Erro ${status} ao falar com o servidor.`;
}

async function requisicao(caminho, { metodo = "GET", corpo, token } = {}) {
  const controlador = new AbortController();
  const temporizador = setTimeout(() => controlador.abort(), TIMEOUT_MS);
  try {
    const resposta = await fetch(`${BASE_URL}${caminho}`, {
      method: metodo,
      headers: {
        ...(corpo ? { "Content-Type": "application/json" } : {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: corpo ? JSON.stringify(corpo) : undefined,
      signal: controlador.signal,
    });
    if (resposta.status === 204) return null;

    let dados = null;
    try {
      dados = await resposta.json();
    } catch {
      dados = null;
    }
    if (!resposta.ok) throw new ApiError(resposta.status, montarMensagem(resposta.status, dados?.detail));
    return dados;
  } catch (erro) {
    if (erro instanceof ApiError) throw erro;
    if (erro.name === "AbortError") throw new ApiError(0, "A API demorou demais para responder. Tente novamente.");
    throw new ApiError(0, "Não foi possível conectar à API. Verifique a internet e tente de novo.");
  } finally {
    clearTimeout(temporizador);
  }
}

export const cadastrar = (nome, email, senha) => requisicao("/auth/cadastro", { metodo: "POST", corpo: { nome, email, senha } });
export const entrar = (email, senha) => requisicao("/auth/login", { metodo: "POST", corpo: { email, senha } });
export const buscarUsuario = (token) => requisicao("/auth/eu", { token });

export const gerarAtividade = (token, dados) => requisicao("/atividades/gerar", { metodo: "POST", corpo: dados, token });
export const listarAtividades = (token) => requisicao("/atividades", { token });
export const salvarAtividade = (token, atividade) => requisicao("/atividades", { metodo: "POST", corpo: atividade, token });
export const excluirAtividade = (token, id) => requisicao(`/atividades/${id}`, { metodo: "DELETE", token });
