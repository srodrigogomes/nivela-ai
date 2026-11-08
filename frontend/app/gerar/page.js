"use client";

import { useState } from "react";
import { useApp } from "../../context/AppContext";
import useRequireAuth from "../../hooks/useRequireAuth";
import { gerarAtividade } from "../../services/mockApi";
import { NIVEIS } from "../../data/levels";
import { DISCIPLINAS, MATERIAL_MAX, SERIES, TIPOS_QUESTAO } from "../../data/options";
import Alert from "../../components/Alert";
import Button from "../../components/Button";
import LevelTabs from "../../components/LevelTabs";
import MaterialField from "../../components/MaterialField";
import { FormField, SelectInput, TextInput } from "../../components/FormField";

const FORM_INICIAL = {
  disciplina: DISCIPLINAS[0],
  serie: SERIES[0],
  tema: "",
  quantidade: 3,
  niveis: NIVEIS.map((n) => n.id),
  tipo: "mista",
  material: "",
};

export default function GerarPage() {
  const user = useRequireAuth();
  const { addActivity } = useApp();
  const [form, setForm] = useState(FORM_INICIAL);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [erroApi, setErroApi] = useState("");
  const [resultado, setResultado] = useState(null);
  const [salva, setSalva] = useState(false);
  const [baseadoEmMaterial, setBaseadoEmMaterial] = useState(false);

  if (!user) return null;

  function atualizar(campo, valor) {
    setForm((atual) => ({ ...atual, [campo]: valor }));
  }

  function alternarNivel(id) {
    setForm((atual) => ({
      ...atual,
      niveis: atual.niveis.includes(id) ? atual.niveis.filter((n) => n !== id) : [...atual.niveis, id],
    }));
  }

  function validar() {
    const novosErros = {};
    if (form.tema.trim().length < 3) novosErros.tema = "Informe o tema com pelo menos 3 caracteres.";
    const quantidade = Number(form.quantidade);
    if (!Number.isInteger(quantidade) || quantidade < 1 || quantidade > 10) {
      novosErros.quantidade = "Use um número de 1 a 10.";
    }
    if (form.niveis.length === 0) novosErros.niveis = "Selecione ao menos um nível.";
    if (form.material.length > MATERIAL_MAX) novosErros.material = `O material pode ter no máximo ${MATERIAL_MAX} caracteres.`;
    return novosErros;
  }

  async function handleSubmit(evento) {
    evento.preventDefault();
    const novosErros = validar();
    setErrors(novosErros);
    if (Object.keys(novosErros).length > 0) return;

    setLoading(true);
    setSalva(false);
    setErroApi("");
    setBaseadoEmMaterial(form.material.trim().length > 0);
    try {
      const atividade = await gerarAtividade({
        ...form,
        tema: form.tema.trim(),
        quantidade: Number(form.quantidade),
        material: form.material.trim(),
        niveis: NIVEIS.map((n) => n.id).filter((id) => form.niveis.includes(id)),
      });
      setResultado(atividade);
    } catch {
      setErroApi("Não foi possível gerar a atividade. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  function handleSalvar() {
    addActivity(resultado);
    setSalva(true);
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Gerar atividade</h1>
        <p className="mt-1 text-sm text-slate-600">
          Informe os dados e receba a mesma atividade em vários níveis. Nesta versão, o resultado é simulado.
        </p>
      </div>

      <form onSubmit={handleSubmit} noValidate className="space-y-4 rounded-xl border border-slate-200 bg-white p-6">
        <div className="grid gap-4 sm:grid-cols-3">
          <FormField label="Disciplina" id="disciplina">
            <SelectInput id="disciplina" options={DISCIPLINAS} value={form.disciplina} onChange={(e) => atualizar("disciplina", e.target.value)} />
          </FormField>
          <FormField label="Série" id="serie">
            <SelectInput id="serie" options={SERIES} value={form.serie} onChange={(e) => atualizar("serie", e.target.value)} />
          </FormField>
          <FormField label="Nº de questões" id="quantidade" error={errors.quantidade}>
            <TextInput id="quantidade" type="number" min="1" max="10" value={form.quantidade} error={errors.quantidade} onChange={(e) => atualizar("quantidade", e.target.value)} />
          </FormField>
        </div>

        <FormField label="Tema ou habilidade" id="tema" error={errors.tema}>
          <TextInput id="tema" placeholder="Ex.: soma de frações com denominadores iguais" value={form.tema} error={errors.tema} onChange={(e) => atualizar("tema", e.target.value)} />
        </FormField>

        <div className="max-w-sm">
          <FormField label="Tipo de questão" id="tipo">
            <SelectInput id="tipo" options={TIPOS_QUESTAO} value={form.tipo} onChange={(e) => atualizar("tipo", e.target.value)} />
          </FormField>
        </div>

        <MaterialField value={form.material} error={errors.material} onChange={(texto) => atualizar("material", texto)} />

        <fieldset>
          <legend className="text-sm font-semibold">Níveis</legend>
          <div className="mt-2 flex flex-wrap gap-x-6 gap-y-2">
            {NIVEIS.map((nivel) => (
              <label key={nivel.id} className="flex items-center gap-2 text-sm">
                <input type="checkbox" className="h-4 w-4 accent-teal-700" checked={form.niveis.includes(nivel.id)} onChange={() => alternarNivel(nivel.id)} />
                {nivel.label}
              </label>
            ))}
          </div>
          {errors.niveis && <p className="mt-1.5 text-sm text-red-700">{errors.niveis}</p>}
        </fieldset>

        <Button type="submit" loading={loading}>
          {loading ? "Gerando..." : "Gerar atividade"}
        </Button>
      </form>

      {erroApi && <Alert type="error">{erroApi}</Alert>}

      {resultado && (
        <section className="space-y-4 rounded-xl border border-slate-200 bg-white p-6">
          <div>
            <h2 className="text-xl font-bold">{resultado.titulo}</h2>
            <p className="text-sm text-slate-600">
              {resultado.disciplina}, {resultado.serie}
            </p>
          </div>
          {baseadoEmMaterial && <p className="text-sm text-teal-800">Atividade baseada no material de apoio informado.</p>}
          <LevelTabs key={resultado.gerada} versoes={resultado.versoes} />
          {salva && <Alert type="success">Atividade salva em Minhas atividades.</Alert>}
          <Button onClick={handleSalvar} disabled={salva}>
            Salvar atividade
          </Button>
        </section>
      )}
    </div>
  );
}
