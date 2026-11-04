const BASE =
  "h-11 w-full rounded-lg border bg-white px-3 text-sm focus:border-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-700/30";

export function FormField({ label, id, error, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-semibold">
        {label}
      </label>
      {children}
      {error && <p className="text-sm text-red-700">{error}</p>}
    </div>
  );
}

export function TextInput({ id, error, ...props }) {
  return (
    <input
      id={id}
      aria-invalid={Boolean(error)}
      className={`${BASE} ${error ? "border-red-500" : "border-slate-300"}`}
      {...props}
    />
  );
}

export function SelectInput({ id, options, ...props }) {
  return (
    <select id={id} className={`${BASE} border-slate-300`} {...props}>
      {options.map((opcao) => (
        <option key={opcao} value={opcao}>
          {opcao}
        </option>
      ))}
    </select>
  );
}
