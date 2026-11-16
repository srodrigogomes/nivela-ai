"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { ApiError, buscarUsuario, cadastrar as cadastrarNaApi, entrar } from "../services/api";

const CHAVE_TOKEN = "nivela_token";
const AppContext = createContext(null);

function lerToken() {
  try {
    return window.localStorage.getItem(CHAVE_TOKEN);
  } catch {
    return null;
  }
}

function guardarToken(token) {
  try {
    if (token) window.localStorage.setItem(CHAVE_TOKEN, token);
    else window.localStorage.removeItem(CHAVE_TOKEN);
  } catch {
    // sem acesso ao armazenamento do navegador: a sessão vale só até recarregar a página
  }
}

export function AppProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [iniciando, setIniciando] = useState(true);

  // Ao abrir o site, tenta retomar a sessão com o token guardado.
  useEffect(() => {
    const salvo = lerToken();
    if (!salvo) {
      setIniciando(false);
      return;
    }
    buscarUsuario(salvo)
      .then((usuario) => {
        setToken(salvo);
        setUser(usuario);
      })
      .catch((erro) => {
        if (erro instanceof ApiError && erro.status === 401) guardarToken(null);
      })
      .finally(() => setIniciando(false));
  }, []);

  const login = useCallback(async (email, senha) => {
    const { access_token: novoToken } = await entrar(email, senha);
    const usuario = await buscarUsuario(novoToken);
    guardarToken(novoToken);
    setToken(novoToken);
    setUser(usuario);
  }, []);

  const cadastrar = useCallback(
    async (nome, email, senha) => {
      await cadastrarNaApi(nome, email, senha);
      await login(email, senha);
    },
    [login]
  );

  const logout = useCallback(() => {
    guardarToken(null);
    setToken(null);
    setUser(null);
  }, []);

  return (
    <AppContext.Provider value={{ user, token, iniciando, login, cadastrar, logout }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const contexto = useContext(AppContext);
  if (!contexto) throw new Error("useApp deve ser usado dentro de AppProvider");
  return contexto;
}
