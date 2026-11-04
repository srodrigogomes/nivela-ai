"use client";

import { useState } from "react";
import { NIVEIS } from "../data/levels";
import ActivityVersion from "./ActivityVersion";

export default function LevelTabs({ versoes }) {
  const [ativo, setAtivo] = useState(versoes[0].nivel);
  const versao = versoes.find((v) => v.nivel === ativo) ?? versoes[0];

  return (
    <div>
      <div role="tablist" className="mb-4 flex flex-wrap gap-2">
        {versoes.map((v) => {
          const nivel = NIVEIS.find((n) => n.id === v.nivel);
          const selecionado = v.nivel === versao.nivel;
          return (
            <button
              key={v.nivel}
              role="tab"
              aria-selected={selecionado}
              onClick={() => setAtivo(v.nivel)}
              className={`h-10 rounded-lg border px-4 text-sm font-semibold ${
                selecionado
                  ? "border-teal-700 bg-teal-700 text-white"
                  : "border-slate-300 bg-white text-slate-800 hover:bg-slate-50"
              }`}
            >
              {nivel ? nivel.label : v.nivel}
            </button>
          );
        })}
      </div>
      <ActivityVersion versao={versao} />
    </div>
  );
}
