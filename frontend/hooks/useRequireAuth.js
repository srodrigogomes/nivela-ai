"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useApp } from "../context/AppContext";

// Redireciona para o login quando não há professor autenticado.
export default function useRequireAuth() {
  const { user } = useApp();
  const router = useRouter();

  useEffect(() => {
    if (!user) router.replace("/");
  }, [user, router]);

  return user;
}
