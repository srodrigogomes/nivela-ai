"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useApp } from "../context/AppContext";
import Button from "../components/Button";
import { FormField, TextInput } from "../components/FormField";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useApp();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  function handleSubmit(evento) {
    evento.preventDefault();
    const novosErros = {};
    if (!/^\S+@\S+\.\S+$/.test(email)) novosErros.email = "Informe um e-mail válido.";
    if (senha.length < 6) novosErros.senha = "A senha deve ter pelo menos 6 caracteres.";
    setErrors(novosErros);
    if (Object.keys(novosErros).length > 0) return;

    setLoading(true);
    setTimeout(() => {
      login(email);
      router.push("/gerar");
    }, 800);
  }

  return (
    <div className="mx-auto max-w-sm space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-teal-700">nivela-ai</h1>
        <p className="mt-1 text-sm text-slate-600">Atividades para todos os níveis da sua turma.</p>
      </div>

      <form onSubmit={handleSubmit} noValidate className="space-y-4 rounded-xl border border-slate-200 bg-white p-6">
        <FormField label="E-mail" id="email" error={errors.email}>
          <TextInput id="email" type="email" placeholder="professor@escola.com" value={email} error={errors.email} onChange={(e) => setEmail(e.target.value)} />
        </FormField>
        <FormField label="Senha" id="senha" error={errors.senha}>
          <TextInput id="senha" type="password" placeholder="Mínimo de 6 caracteres" value={senha} error={errors.senha} onChange={(e) => setSenha(e.target.value)} />
        </FormField>
        <Button type="submit" loading={loading} className="w-full">
          {loading ? "Entrando..." : "Entrar"}
        </Button>
        <p className="text-center text-xs text-slate-500">
          Versão de demonstração: qualquer e-mail válido e senha com 6 ou mais caracteres funcionam.
        </p>
      </form>
    </div>
  );
}
