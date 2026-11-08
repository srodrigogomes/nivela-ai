"use client";

import { useState } from "react";
import { FormField, TextArea } from "./FormField";
import { MATERIAL_MAX } from "../data/options";

const TAMANHO_MAX_ARQUIVO = 200000; // bytes

export default function MaterialField({ value, onChange, error }) {
  const [aviso, setAviso] = useState("");

  async function handleArquivo(evento) {
    const arquivo = evento.target.files?.[0];
    evento.target.value = "";
    if (!arquivo) return;
    setAviso("");

    if (!/\.(txt|md)$/i.test(arquivo.name)) {
      setAviso("Use um arquivo .txt ou .md. Para PDF, copie e cole o texto na caixa.");
      return;
    }
    if (arquivo.size > TAMANHO_MAX_ARQUIVO) {
      setAviso("Arquivo muito grande (máximo de 200 KB).");
      return;
    }

    const texto = await arquivo.text();
    if (texto.length > MATERIAL_MAX) {
      setAviso(`O arquivo tem ${texto.length} caracteres. Só os primeiros ${MATERIAL_MAX} serão usados.`);
    }
    onChange(texto.slice(0, MATERIAL_MAX));
  }

  return (
    <FormField label="Material de apoio (opcional)" id="material" error={error}>
      <TextArea
        id="material"
        rows={5}
        placeholder="Cole aqui o texto ou o resumo que você usou em aula. A IA vai se basear nele."
        value={value}
        error={error}
        onChange={(e) => onChange(e.target.value)}
      />
      <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-slate-600">
        <label className="cursor-pointer font-semibold text-teal-700 underline underline-offset-4">
          Anexar arquivo (.txt ou .md)
          <input type="file" accept=".txt,.md,text/plain,text/markdown" className="sr-only" onChange={handleArquivo} />
        </label>
        <span>
          {value.length} / {MATERIAL_MAX} caracteres
        </span>
      </div>
      {aviso && <p className="text-xs text-amber-800">{aviso}</p>}
    </FormField>
  );
}
