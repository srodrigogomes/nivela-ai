"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useApp } from "../../context/AppContext";
import useRequireAuth from "../../hooks/useRequireAuth";
import { ApiError, excluirAtividade, listarAtividades } from "../../services/api";
import ActivityCard from "../../components/ActivityCard";
import Alert from "../../components/Alert";
import Button from "../../components/Button";
import Spinner from "../../components/Spinner";

export default function AtividadesPage() {
  const user = useRequireAuth();
  const { token, logout } = useApp();
  const [atividades, setAtividades] = useState(null); // null = ainda carregando
  const [erro, setErro] = useState("");
  const [tentativa, setTentativa] = useState(0);
  const [abertaId, setAbertaId] = useState(null);

  useEffect(() => {
    if (!token) return;
    let cancelado = false;
    setErro("");
    setAtividades(null);
    listarAtividades(token)
      .then((dados) => {
        if (!cancelado) setAtividades(dados);
      })
      .catch((e) => {
        if (cancelado) return;
        if (e instanceof ApiError && e.status === 401) {
          logout();
          return;
        }
        setErro(e instanceof ApiError ? e.message : "Não foi possível carregar as atividades.");
      });
    return () => {
      cancelado = true;
    };
  }, [token, tentativa, logout]);

  if (!user) return null;

  async function excluir(atividade) {
    if (!window.confirm(`Excluir a atividade "${atividade.titulo}"?`)) return;
    try {
      await excluirAtividade(token, atividade.id);
      setAtividades((atuais) => atuais.filter((a) => a.id !== atividade.id));
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        logout();
        return;
      }
      setErro(e instanceof ApiError ? e.message : "Não foi possível excluir a atividade.");
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Minhas atividades</h1>
        <p className="mt-1 text-sm text-slate-600">Atividades salvas para reutilizar.</p>
      </div>

      {erro && (
        <div className="space-y-3">
          <Alert type="error">{erro}</Alert>
          <Button variant="secondary" onClick={() => setTentativa((n) => n + 1)}>
            Tentar de novo
          </Button>
        </div>
      )}

      {!erro && atividades === null && (
        <p className="flex items-center gap-2 text-sm text-slate-600">
          <Spinner /> Carregando atividades... No primeiro acesso do dia, pode levar até 1 minuto.
        </p>
      )}

      {atividades && atividades.length === 0 && (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center">
          <p className="font-semibold">Você ainda não salvou nenhuma atividade.</p>
          <Link href="/gerar" className="mt-2 inline-block text-sm font-semibold text-teal-700 underline underline-offset-4">
            Gerar a primeira atividade
          </Link>
        </div>
      )}

      {atividades && atividades.length > 0 && (
        <div className="space-y-4">
          {atividades.map((atividade) => (
            <ActivityCard
              key={atividade.id}
              atividade={atividade}
              aberta={abertaId === atividade.id}
              onToggle={() => setAbertaId(abertaId === atividade.id ? null : atividade.id)}
              onDelete={() => excluir(atividade)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
