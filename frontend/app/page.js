"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useApp } from "../context/AppContext";
import { ApiError } from "../services/api";
import Alert from "../components/Alert";
import Button from "../components/Button";
import { FormField, TextInput } from "../components/FormField";

export default function LoginPage() {
  const router = useRouter();
  const { user, iniciando, login, cadastrar } = useApp();
  const [modo, setModo] = useState("entrar");
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [errors, setErrors] = useState({});
  const [erroApi, setErroApi] = useState("");
  const [loading, setLoading] = useState(false);

  const criandoConta = modo === "cadastro";

  useEffect(() => {
    if (!iniciando && user) router.replace("/gerar");
  }, [iniciando, user, router]);

  function trocarModo() {
    setModo(criandoConta ? "entrar" : "cadastro");
    setErrors({});
    setErroApi("");
  }

  function validar() {
    const novosErros = {};
    if (criandoConta && nome.trim().length < 2) novosErros.nome = "Informe seu nome.";
    if (!/^\S+@\S+\.\S+$/.test(email)) novosErros.email = "Informe um e-mail válido.";
    if (senha.length < 6) novosErros.senha = "A senha deve ter pelo menos 6 caracteres.";
    return novosErros;
  }

  async function handleSubmit(evento) {
    evento.preventDefault();
    const novosErros = validar();
    setErrors(novosErros);
    setErroApi("");
    if (Object.keys(novosErros).length > 0) return;

    setLoading(true);
    try {
      if (criandoConta) await cadastrar(nome.trim(), email.trim(), senha);
      else await login(email.trim(), senha);
      router.push("/gerar");
    } catch (erro) {
      setErroApi(erro instanceof ApiError ? erro.message : "Não foi possível concluir. Tente novamente.");
      setLoading(false);
    }
  }

  if (iniciando) {
    return <p className="text-center text-sm text-slate-600">Carregando...</p>;
  }

  return (
    <div className="mx-auto max-w-sm space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-teal-700">nivela-ai</h1>
        <p className="mt-1 text-sm text-slate-600">Atividades para todos os níveis da sua turma.</p>
      </div>

      <form onSubmit={handleSubmit} noValidate className="space-y-4 rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-bold">{criandoConta ? "Criar conta" : "Entrar"}</h2>

        {criandoConta && (
          <FormField label="Nome" id="nome" error={errors.nome}>
            <TextInput id="nome" placeholder="Seu nome" value={nome} error={errors.nome} onChange={(e) => setNome(e.target.value)} />
          </FormField>
        )}
        <FormField label="E-mail" id="email" error={errors.email}>
          <TextInput id="email" type="email" placeholder="professor@escola.com" value={email} error={errors.email} onChange={(e) => setEmail(e.target.value)} />
        </FormField>
        <FormField label="Senha" id="senha" error={errors.senha}>
          <TextInput id="senha" type="password" placeholder="Mínimo de 6 caracteres" value={senha} error={errors.senha} onChange={(e) => setSenha(e.target.value)} />
        </FormField>

        {erroApi && <Alert type="error">{erroApi}</Alert>}

        <Button type="submit" loading={loading} className="w-full">
          {loading ? "Aguarde..." : criandoConta ? "Criar conta" : "Entrar"}
        </Button>
        {loading && (
          <p className="text-center text-xs text-slate-500">
            No primeiro acesso do dia, o servidor gratuito pode levar até 1 minuto para acordar.
          </p>
        )}
        <button type="button" onClick={trocarModo} className="w-full text-center text-sm font-semibold text-teal-700 underline underline-offset-4">
          {criandoConta ? "Já tenho conta. Entrar" : "Ainda não tenho conta. Criar conta"}
        </button>
      </form>
    </div>
  );
}
