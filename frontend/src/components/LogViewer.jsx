import { CheckCircle2, CircleAlert, Clock3, Terminal } from 'lucide-react'

const iconByType = {
  ok: CheckCircle2,
  error: CircleAlert,
  wait: Clock3,
  info: Terminal,
}

const toneByType = {
  ok: 'text-msn-green',
  error: 'text-msn-red',
  wait: 'text-msn-amber',
  info: 'text-msn-blue',
}

function LogViewer({ logs, status = 'standby' }) {
  return (
    <section className="rounded-lg border border-zinc-200 bg-zinc-950 p-5 text-zinc-100 shadow-panel">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Terminal className="h-5 w-5 text-emerald-300" aria-hidden="true" />
          <h2 className="text-base font-semibold">Logs</h2>
        </div>
        <span className="rounded-lg bg-zinc-800 px-3 py-1 text-xs font-medium text-zinc-300">
          {status}
        </span>
      </div>

      <div className="space-y-3">
        {logs.map((log, index) => {
          const Icon = iconByType[log.type] ?? Terminal
          const tone = toneByType[log.type] ?? toneByType.info
          return (
            <div className="flex gap-3 text-sm" key={`${log.type}-${index}-${log.message}`}>
              <Icon className={`mt-0.5 h-4 w-4 shrink-0 ${tone}`} aria-hidden="true" />
              <p className="whitespace-pre-wrap leading-6 text-zinc-300">{log.message}</p>
            </div>
          )
        })}
      </div>
    </section>
  )
}

export default LogViewer
