import Button from "./Button";
import LevelTabs from "./LevelTabs";
import { NIVEIS } from "../data/levels";

function formatarData(iso) {
  return new Date(iso).toLocaleDateString("pt-BR", { timeZone: "UTC" });
}

export default function ActivityCard({ atividade, aberta, onToggle, onDelete }) {
  const niveis = atividade.versoes
    .map((v) => NIVEIS.find((n) => n.id === v.nivel)?.label)
    .filter(Boolean)
    .join(", ");

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-bold">{atividade.titulo}</h2>
          <p className="text-sm text-slate-600">
            {atividade.disciplina}, {atividade.serie}. Níveis: {niveis}. Criada em {formatarData(atividade.criadaEm)}.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={onToggle}>
            {aberta ? "Fechar" : "Abrir"}
          </Button>
          <Button variant="danger" onClick={onDelete}>
            Excluir
          </Button>
        </div>
      </div>

      {aberta && (
        <div className="mt-5 border-t border-slate-200 pt-5">
          <LevelTabs versoes={atividade.versoes} />
        </div>
      )}
    </article>
  );
}
