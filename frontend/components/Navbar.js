"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useApp } from "../context/AppContext";

const LINKS_LOGADO = [
  { href: "/gerar", label: "Gerar atividade" },
  { href: "/atividades", label: "Minhas atividades" },
];

export default function Navbar() {
  const { user, logout } = useApp();
  const pathname = usePathname();
  const router = useRouter();
  const links = [...(user ? LINKS_LOGADO : []), { href: "/ajuda", label: "Ajuda" }];

  function sair() {
    logout();
    router.push("/");
  }

  return (
    <header className="border-b border-slate-200 bg-white">
      <nav className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
        <Link href={user ? "/gerar" : "/"} className="text-xl font-bold text-teal-700">
          nivela-ai
        </Link>
        <div className="flex items-center gap-4 text-sm">
          {user && <span className="hidden text-slate-500 sm:inline">{user.nome}</span>}
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`font-semibold ${
                pathname === link.href
                  ? "text-teal-700 underline underline-offset-4"
                  : "text-slate-700 hover:text-teal-700"
              }`}
            >
              {link.label}
            </Link>
          ))}
          {user && (
            <button onClick={sair} className="text-slate-600 hover:text-slate-900">
              Sair
            </button>
          )}
        </div>
      </nav>
    </header>
  );
}
