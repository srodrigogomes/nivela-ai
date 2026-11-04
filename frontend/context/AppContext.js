"use client";

import { createContext, useCallback, useContext, useState } from "react";
import { mockActivities } from "../data/mockActivities";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [activities, setActivities] = useState(mockActivities);

  const login = useCallback((email) => {
    setUser({ email, nome: email.split("@")[0] });
  }, []);

  const logout = useCallback(() => setUser(null), []);

  const addActivity = useCallback((atividade) => {
    setActivities((anteriores) => [
      { ...atividade, id: Date.now(), criadaEm: new Date().toISOString() },
      ...anteriores,
    ]);
  }, []);

  const removeActivity = useCallback((id) => {
    setActivities((anteriores) => anteriores.filter((a) => a.id !== id));
  }, []);

  return (
    <AppContext.Provider value={{ user, login, logout, activities, addActivity, removeActivity }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const contexto = useContext(AppContext);
  if (!contexto) throw new Error("useApp deve ser usado dentro de AppProvider");
  return contexto;
}
