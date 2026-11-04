export default function ActivityVersion({ versao }) {
  return (
    <div className="space-y-4">
      <p className="text-sm text-slate-600">{versao.instrucoes}</p>

      <ol className="space-y-3">
        {versao.questoes.map((questao) => (
          <li key={questao.numero} className="rounded-lg border border-slate-200 p-4">
            <p>
              <span className="font-bold">Questão {questao.numero}.</span> {questao.enunciado}
            </p>
            {questao.alternativas && (
              <ul className="mt-2 space-y-1 text-sm">
                {questao.alternativas.map((alternativa, i) => (
                  <li key={alternativa}>
                    {String.fromCharCode(97 + i)}) {alternativa}
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ol>

      <div className="rounded-lg bg-teal-50 p-4 text-sm">
        <p className="font-bold">Gabarito</p>
        <ul className="mt-1 space-y-1">
          {versao.gabarito.map((item) => (
            <li key={item.numero}>
              {item.numero}) {item.resposta}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
