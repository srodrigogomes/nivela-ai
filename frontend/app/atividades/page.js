"use client";

import { useState } from "react";
import Link from "next/link";
import { useApp } from "../../context/AppContext";
import useRequireAuth from "../../hooks/useRequireAuth";
import ActivityCard from "../../components/ActivityCard";

export default function AtividadesPage() {
  const user = useRequireAuth();
  const { activities, removeActivity } = useApp();
  const [abertaId, setAbertaId] = useState(null);

  if (!user) return null;

  function excluir(atividade) {
    if (window.confirm(`Excluir a atividade "${atividade.titulo}"?`)) {
      removeActivity(atividade.id);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Minhas atividades</h1>
        <p className="mt-1 text-sm text-slate-600">Atividades salvas para reutilizar.</p>
      </div>

      {activities.length === 0 ? (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center">
          <p className="font-semibold">Você ainda não salvou nenhuma atividade.</p>
          <Link href="/gerar" className="mt-2 inline-block text-sm font-semibold text-teal-700 underline underline-offset-4">
            Gerar a primeira atividade
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {activities.map((atividade) => (
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
