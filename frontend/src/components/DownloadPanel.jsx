import { Download, FileSpreadsheet } from 'lucide-react'

import { toDownloadUrl } from '../api/conciliador'

const outputLabels = {
  wordpress_atualizado: 'Planilha WordPress atualizada',
  relatorio: 'Relatorio de conciliacao',
}

function DownloadPanel({ result }) {
  if (!result?.outputs) {
    return null
  }

  return (
    <section className="rounded-lg border border-emerald-200 bg-white p-5 shadow-panel">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-emerald-50 text-msn-green ring-1 ring-emerald-200">
          <FileSpreadsheet className="h-5 w-5" aria-hidden="true" />
        </div>
        <div className="min-w-0">
          <h2 className="text-base font-semibold text-zinc-950">Downloads prontos</h2>
          <p className="mt-1 text-sm text-zinc-600">
            Job <span className="font-mono text-xs text-zinc-800">{result.job_id}</span>
          </p>
        </div>
      </div>

      <div className="mt-4 space-y-3">
        {Object.entries(result.outputs).map(([key, artifact]) => (
          <a
            className="flex items-center justify-between gap-3 rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm font-medium text-zinc-900 transition hover:border-emerald-300 hover:bg-emerald-50"
            download={artifact.filename}
            href={toDownloadUrl(artifact.download_url)}
            key={key}
          >
            <span className="min-w-0 truncate">{outputLabels[key] || artifact.filename}</span>
            <Download className="h-4 w-4 shrink-0 text-msn-green" aria-hidden="true" />
          </a>
        ))}
      </div>
    </section>
  )
}

export default DownloadPanel
