import { useMemo, useState } from 'react'
import {
  ArrowRight,
  CircleAlert,
  CheckCircle2,
  Clock3,
  FileSpreadsheet,
  Images,
  PackageCheck,
  ShieldCheck,
} from 'lucide-react'
import { API_BASE_URL, conciliarPlanilhas } from './api/conciliador'
import DownloadPanel from './components/DownloadPanel'
import LogViewer from './components/LogViewer'
import UploadForm from './components/UploadForm'

function App() {
  const [files, setFiles] = useState({
    wordpress: null,
    cliente: null,
  })
  const [status, setStatus] = useState('idle')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [runtimeLogs, setRuntimeLogs] = useState([])

  const logs = useMemo(() => {
    const baseLogs = [
      {
        type: 'ok',
        message: `Backend configurado em ${API_BASE_URL}/api/v1/conciliar.`,
      },
      {
        type: 'info',
        message: 'Selecione as duas planilhas e inicie a conciliacao.',
      },
    ]

    if (runtimeLogs.length > 0) {
      baseLogs.push(...runtimeLogs)
    } else {
      baseLogs.push({
        type: 'wait',
        message: 'Aguardando arquivos para processar.',
      })
    }

    return baseLogs
  }, [runtimeLogs])

  const isProcessing = status === 'loading'
  const canSubmit = Boolean(files.wordpress && files.cliente)

  const steps = [
    {
      title: 'Conciliacao',
      status: getConciliacaoStepStatus(status),
      icon: FileSpreadsheet,
      tone: getConciliacaoTone(status),
    },
    {
      title: 'Busca de imagens',
      status: 'Proxima fase',
      icon: Images,
      tone: 'text-msn-amber bg-amber-50 border-amber-200',
    },
    {
      title: 'Tratamento final',
      status: 'Aguardando',
      icon: PackageCheck,
      tone: 'text-msn-green bg-emerald-50 border-emerald-200',
    },
  ]

  function handleFileChange(field, file) {
    setFiles((current) => ({
      ...current,
      [field]: file,
    }))
    setError('')
    if (status !== 'loading') {
      setStatus('idle')
      setResult(null)
      setRuntimeLogs([])
    }
  }

  async function handleSubmit(event) {
    event.preventDefault()
    if (!canSubmit || isProcessing) {
      return
    }

    setStatus('loading')
    setError('')
    setResult(null)
    setRuntimeLogs([
      {
        type: 'info',
        message: 'Enviando planilhas para validacao segura...',
      },
      {
        type: 'wait',
        message: 'Executando conciliador Python. Esta etapa pode levar alguns instantes.',
      },
    ])

    try {
      const payload = await conciliarPlanilhas(files)
      setResult(payload)
      setStatus('success')
      setRuntimeLogs(buildSuccessLogs(payload))
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : 'Erro inesperado.'
      setError(message)
      setStatus('error')
      setRuntimeLogs([
        {
          type: 'error',
          message,
        },
      ])
    }
  }

  return (
    <div className="min-h-screen bg-zinc-100 text-ink">
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto flex w-full max-w-7xl flex-col gap-4 px-4 py-5 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-msn-green text-sm font-bold text-white">
              MSN
            </div>
            <div>
              <h1 className="text-xl font-semibold text-zinc-950">Automacao MSN</h1>
              <p className="text-sm text-zinc-600">Esteira de planilhas e imagens</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 text-sm text-zinc-600">
            <span className="inline-flex items-center gap-2 rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-msn-green">
              <ShieldCheck className="h-4 w-4" aria-hidden="true" />
              Backend seguro
            </span>
            <span className="inline-flex items-center gap-2 rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2">
              <Clock3 className="h-4 w-4" aria-hidden="true" />
              Etapa 5
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto grid w-full max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[minmax(0,1fr)_380px] lg:px-8">
        <section className="space-y-6">
          <div className="rounded-lg border border-zinc-200 bg-white p-5 shadow-panel">
            <div className="grid gap-3 md:grid-cols-3">
              {steps.map((step, index) => {
                const Icon = step.icon
                return (
                  <div
                    className={`flex min-h-24 items-center gap-3 rounded-lg border p-4 ${step.tone}`}
                    key={step.title}
                  >
                    <Icon className="h-5 w-5 shrink-0" aria-hidden="true" />
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-zinc-950">
                        {index + 1}. {step.title}
                      </p>
                      <p className="mt-1 text-sm text-zinc-600">{step.status}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          <section className="rounded-lg border border-zinc-200 bg-white p-5 shadow-panel">
            <div className="mb-5 flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h2 className="text-lg font-semibold text-zinc-950">Conciliacao de estoque</h2>
                <p className="mt-1 text-sm text-zinc-600">
                  Selecione a exportacao do WordPress e a planilha atualizada do cliente.
                </p>
              </div>
              <span className="inline-flex w-fit items-center gap-2 rounded-lg border border-blue-200 bg-blue-50 px-3 py-2 text-sm font-medium text-msn-blue">
                <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
                API conectada
              </span>
            </div>

            <UploadForm
              canSubmit={canSubmit}
              files={files}
              isProcessing={isProcessing}
              onFileChange={handleFileChange}
              onSubmit={handleSubmit}
            />

            {isProcessing && (
              <div className="mt-5 overflow-hidden rounded-full bg-zinc-200">
                <div className="h-2 w-1/2 animate-pulse rounded-full bg-msn-green" />
              </div>
            )}

            {error && (
              <div className="mt-5 flex gap-3 rounded-lg border border-orange-200 bg-orange-50 p-4 text-sm text-orange-900">
                <CircleAlert className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                <p className="leading-6">{error}</p>
              </div>
            )}
          </section>
        </section>

        <aside className="space-y-6">
          <LogViewer logs={logs} status={status} />

          <DownloadPanel result={result} />

          <section className="rounded-lg border border-zinc-200 bg-white p-5 shadow-panel">
            <h2 className="text-base font-semibold text-zinc-950">Proximo marco</h2>
            <p className="mt-2 text-sm leading-6 text-zinc-600">
              Depois da conciliacao, a proxima fase vai acionar a busca de imagens usando a planilha gerada.
            </p>
            <button
              className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-zinc-300 px-4 py-3 text-sm font-semibold text-zinc-600"
              disabled
              type="button"
            >
              Aguardando busca de imagens
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </button>
          </section>
        </aside>
      </main>
    </div>
  )
}

function buildSuccessLogs(payload) {
  const logs = [
    {
      type: 'ok',
      message: payload.message || 'Conciliacao finalizada.',
    },
  ]

  if (payload.logs?.stdout) {
    logs.push({
      type: 'info',
      message: payload.logs.stdout.trim(),
    })
  }
  if (payload.logs?.stderr) {
    logs.push({
      type: 'error',
      message: payload.logs.stderr.trim(),
    })
  }
  logs.push({
    type: 'ok',
    message: 'Downloads liberados no painel lateral.',
  })

  return logs
}

function getConciliacaoStepStatus(status) {
  if (status === 'loading') {
    return 'Processando'
  }
  if (status === 'success') {
    return 'Concluida'
  }
  if (status === 'error') {
    return 'Revisar erro'
  }
  return 'Pronta'
}

function getConciliacaoTone(status) {
  if (status === 'success') {
    return 'text-msn-green bg-emerald-50 border-emerald-200'
  }
  if (status === 'error') {
    return 'text-msn-red bg-orange-50 border-orange-200'
  }
  if (status === 'loading') {
    return 'text-msn-blue bg-blue-50 border-blue-200'
  }
  return 'text-msn-blue bg-blue-50 border-blue-200'
}

export default App
