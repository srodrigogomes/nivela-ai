import "./globals.css";
import { AppProvider } from "../context/AppContext";
import Navbar from "../components/Navbar";

export const metadata = {
  title: "nivela-ai",
  description: "Atividades em diferentes níveis de aprendizagem para professores da educação básica.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        <AppProvider>
          <Navbar />
          <main className="mx-auto max-w-4xl px-4 py-8">{children}</main>
        </AppProvider>
      </body>
    </html>
  );
}
