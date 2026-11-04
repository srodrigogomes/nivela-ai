import Spinner from "./Spinner";

const VARIANTES = {
  primary: "border-teal-700 bg-teal-700 text-white hover:bg-teal-800",
  secondary: "border-slate-300 bg-white text-slate-800 hover:bg-slate-50",
  danger: "border-red-300 bg-white text-red-700 hover:bg-red-50",
};

export default function Button({ variant = "primary", loading = false, disabled = false, className = "", children, ...props }) {
  return (
    <button
      disabled={loading || disabled}
      className={`inline-flex h-11 items-center justify-center gap-2 rounded-lg border px-4 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-teal-700/40 disabled:cursor-not-allowed disabled:opacity-60 ${VARIANTES[variant]} ${className}`}
      {...props}
    >
      {loading && <Spinner />}
      {children}
    </button>
  );
}
