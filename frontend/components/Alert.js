const ESTILOS = {
  success: "border-green-300 bg-green-50 text-green-900",
  error: "border-red-300 bg-red-50 text-red-900",
};

export default function Alert({ type = "error", children }) {
  return (
    <div role="alert" className={`rounded-lg border px-4 py-3 text-sm ${ESTILOS[type]}`}>
      {children}
    </div>
  );
}
