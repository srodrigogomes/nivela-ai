"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useApp } from "../context/AppContext";

// Envia para o login quando não há professor autenticado (depois de tentar retomar a sessão).
export default function useRequireAuth() {
  const { user, iniciando } = useApp();
  const router = useRouter();

  useEffect(() => {
    if (!iniciando && !user) router.replace("/");
  }, [iniciando, user, router]);

  return user;
}
