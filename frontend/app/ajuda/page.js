import Link from "next/link";
import { DICAS, NIVEIS_AJUDA, PERGUNTAS, PRIMEIROS_PASSOS } from "../../data/ajuda";

export const metadata = { title: "Ajuda | nivela-ai" };

export default function AjudaPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Central de ajuda</h1>
        <p className="mt-1 text-sm text-slate-600">
          Tire suas dúvidas sobre como criar e organizar atividades no nivela-ai.
        </p>
      </div>

      <section className="rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-bold">Primeiros passos</h2>
        <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm">
          {PRIMEIROS_PASSOS.map((passo) => (
            <li key={passo}>{passo}</li>
          ))}
        </ol>
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-bold">Entendendo os níveis</h2>
        <dl className="mt-3 space-y-3 text-sm">
          {NIVEIS_AJUDA.map((nivel) => (
            <div key={nivel.nome}>
              <dt className="font-semibold">{nivel.nome}</dt>
              <dd className="text-slate-700">{nivel.texto}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-bold">Dicas para um bom resultado</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm">
          {DICAS.map((dica) => (
            <li key={dica}>{dica}</li>
          ))}
        </ul>
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-bold">Perguntas frequentes</h2>
        <div className="mt-3 divide-y divide-slate-200">
          {PERGUNTAS.map((item) => (
            <details key={item.p} className="py-3">
              <summary className="cursor-pointer text-sm font-semibold">{item.p}</summary>
              <p className="mt-2 text-sm text-slate-700">{item.r}</p>
            </details>
          ))}
        </div>
      </section>

      <p className="text-sm">
        <Link href="/" className="font-semibold text-teal-700 underline underline-offset-4">
          Voltar ao nivela-ai
        </Link>
      </p>
    </div>
  );
}
