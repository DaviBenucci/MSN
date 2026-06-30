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
  const [currentStep, setCurrentStep] = useState(0)
  const [phase2Status, setPhase2Status] = useState('idle')
  const [phase3Status, setPhase3Status] = useState('idle')
  const [productSummary, setProductSummary] = useState([])

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
      status:
        phase2Status === 'running'
          ? 'Em progresso'
          : phase2Status === 'completed'
          ? 'Concluida'
          : status === 'success'
          ? 'Pronta'
          : 'Bloqueada',
      icon: Images,
      tone:
        phase2Status === 'running'
          ? 'text-msn-blue bg-blue-50 border-blue-200'
          : phase2Status === 'completed'
          ? 'text-msn-green bg-emerald-50 border-emerald-200'
          : 'text-msn-amber bg-amber-50 border-amber-200',
    },
    {
      title: 'Tratamento final',
      status:
        phase3Status === 'running'
          ? 'Em progresso'
          : phase3Status === 'completed'
          ? 'Concluida'
          : phase2Status === 'completed'
          ? 'Pronta'
          : 'Aguardando',
      icon: PackageCheck,
      tone:
        phase3Status === 'running'
          ? 'text-msn-blue bg-blue-50 border-blue-200'
          : phase3Status === 'completed'
          ? 'text-msn-green bg-emerald-50 border-emerald-200'
          : 'text-msn-green bg-emerald-50 border-emerald-200',
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
      setCurrentStep(0)
      setPhase2Status('idle')
      setPhase3Status('idle')
      setProductSummary([])
    }
  }

  function canNavigateToStep(index) {
    if (index === 0) {
      return true
    }
    if (index === 1) {
      return status === 'success' || phase2Status !== 'idle'
    }
    if (index === 2) {
      return phase2Status === 'completed' || phase3Status !== 'idle'
    }
    return false
  }

  function handleStepClick(index) {
    if (!canNavigateToStep(index)) {
      setError('Conclua a etapa anterior antes de avançar.')
      return
    }
    setError('')
    setCurrentStep(index)
    if (index === 1 && phase2Status === 'idle') {
      startPhase2()
    }
    if (index === 2 && phase3Status === 'idle' && phase2Status === 'completed') {
      startPhase3()
    }
  }

  function startPhase2() {
    if (status !== 'success') {
      return
    }
    setPhase2Status('running')
    setCurrentStep(1)
    setRuntimeLogs((current) => [
      ...current,
      { type: 'info', message: 'Fase 2 iniciada: buscando imagens para os SKUs gerados.' },
    ])
  }

  function completePhase2() {
    setPhase2Status('completed')
    setRuntimeLogs((current) => [
      ...current,
      { type: 'ok', message: 'Busca de imagens concluída.' },
    ])
  }

  function startPhase3() {
    if (phase2Status !== 'completed') {
      return
    }
    setPhase3Status('running')
    setCurrentStep(2)
    setRuntimeLogs((current) => [
      ...current,
      { type: 'info', message: 'Fase 3 iniciada: tratamento final das imagens.' },
    ])
  }

  function completePhase3() {
    setPhase3Status('completed')
    setRuntimeLogs((current) => [
      ...current,
      { type: 'ok', message: 'Tratamento final concluído.' },
    ])
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
      setProductSummary(payload.summary ?? [])
      setPhase2Status('idle')
      setPhase3Status('idle')
      setCurrentStep(0)
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
                const isActive = index === currentStep
                return (
                  <button
                    key={step.title}
                    type="button"
                    onClick={() => handleStepClick(index)}
                    className={`flex min-h-24 items-center gap-3 rounded-lg border p-4 text-left ${step.tone} ${isActive ? 'ring-2 ring-blue-300' : ''} focus:outline-none`}
                  >
                    <Icon className="h-5 w-5 shrink-0" aria-hidden="true" />
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-zinc-950">
                        {index + 1}. {step.title}
                      </p>
                      <p className="mt-1 text-sm text-zinc-600">{step.status}</p>
                    </div>
                  </button>
                )
              })}
            </div>
          </div>

          <section className="rounded-lg border border-zinc-200 bg-white p-5 shadow-panel">
            {currentStep === 0 && (
              <>
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

                {status === 'success' && (
                  <div className="mt-5 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-900">
                    Conciliacao concluida. Avance para a fase 2 para buscar imagens.
                  </div>
                )}

                {status === 'error' && (
                  <div className="mt-5 rounded-lg border border-orange-200 bg-orange-50 px-4 py-3 text-sm text-orange-900">
                    Erro na conciliacao. Verifique os logs e tente novamente.
                  </div>
                )}
              </>
            )}

            {currentStep === 1 && (
              <>
                <div className="mb-5">
                  <h2 className="text-lg font-semibold text-zinc-950">Busca de imagens</h2>
                  <p className="mt-1 text-sm text-zinc-600">
                    Esta fase indica o progresso de busca das imagens para os SKUs gerados na planilha.
                  </p>
                </div>

                <div className="space-y-4">
                  <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-4 text-sm text-zinc-700">
                    <p className="font-semibold">Status</p>
                    <p className="mt-1">{phase2Status === 'running' ? 'Em andamento' : phase2Status === 'completed' ? 'Concluida' : 'Aguardando inicio'}</p>
                  </div>

                  {productSummary.length > 0 ? (
                    <div className="rounded-lg border border-zinc-200 bg-white p-4 text-sm text-zinc-800">
                      <p className="font-semibold">Produtos informados</p>
                      <div className="mt-3 overflow-x-auto">
                        <table className="min-w-full divide-y divide-zinc-200 text-left text-sm">
                          <thead className="bg-zinc-50 text-zinc-600">
                            <tr>
                              <th className="px-3 py-2">SKU / Produto</th>
                              <th className="px-3 py-2">Quantidade</th>
                              <th className="px-3 py-2">Status</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-zinc-200">
                            {productSummary.map((item, index) => (
                              <tr key={`${item.sku}-${index}`}>
                                <td className="px-3 py-2 font-medium text-zinc-900">{item.sku || item.product_name}</td>
                                <td className="px-3 py-2">{item.quantity || '—'}</td>
                                <td className="px-3 py-2 text-zinc-600">{item.status || 'Não definido'}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  ) : (
                    <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-4 text-sm text-zinc-700">
                      Nenhum resumo de produtos disponível ainda. Execute a conciliacao para gerar o relatório.
                    </div>
                  )}

                  <div className="flex flex-col gap-3 sm:flex-row">
                    <button
                      className="inline-flex flex-1 items-center justify-center gap-2 rounded-lg bg-msn-green px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-zinc-300"
                      disabled={phase2Status !== 'idle'}
                      onClick={startPhase2}
                      type="button"
                    >
                      {phase2Status === 'idle' ? 'Iniciar busca de imagens' : 'Busca de imagens em andamento'}
                    </button>
                    <button
                      className="inline-flex flex-1 items-center justify-center gap-2 rounded-lg border border-zinc-200 bg-white px-4 py-3 text-sm font-semibold text-zinc-900 shadow-sm transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:border-zinc-200 disabled:text-zinc-400"
                      disabled={phase2Status !== 'running'}
                      onClick={completePhase2}
                      type="button"
                    >
                      Marcar busca como concluída
                    </button>
                  </div>
                </div>
              </>
            )}

            {currentStep === 2 && (
              <>
                <div className="mb-5">
                  <h2 className="text-lg font-semibold text-zinc-950">Tratamento final</h2>
                  <p className="mt-1 text-sm text-zinc-600">
                    Esta fase foca no tratamento do resultado das imagens e finalizacao do processo.
                  </p>
                </div>

                <div className="space-y-4">
                  <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-4 text-sm text-zinc-700">
                    <p className="font-semibold">Status</p>
                    <p className="mt-1">{phase3Status === 'running' ? 'Em andamento' : phase3Status === 'completed' ? 'Concluida' : 'Aguardando inicio'}</p>
                  </div>

                  <div className="rounded-lg border border-zinc-200 bg-white p-4 text-sm text-zinc-800">
                    <p className="font-semibold">Resumo de etapas</p>
                    <p className="mt-2 text-zinc-600">A fase 3 avalia os produtos já conciliados e prepara o conjunto final de imagens.</p>
                  </div>

                  <button
                    className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-msn-green px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-zinc-300"
                    disabled={phase3Status !== 'idle'}
                    onClick={startPhase3}
                    type="button"
                  >
                    {phase3Status === 'idle' ? 'Iniciar tratamento final' : 'Tratamento em andamento'}
                  </button>
                  <button
                    className="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-zinc-200 bg-white px-4 py-3 text-sm font-semibold text-zinc-900 shadow-sm transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:border-zinc-200 disabled:text-zinc-400"
                    disabled={phase3Status !== 'running'}
                    onClick={completePhase3}
                    type="button"
                  >
                    Marcar tratamento como concluído
                  </button>
                </div>
              </>
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
            <h2 className="text-base font-semibold text-zinc-950">Fase atual</h2>
            <p className="mt-2 text-sm leading-6 text-zinc-600">
              Selecione a etapa ou avance para ver detalhes de busca e tratamento de imagens.
            </p>
            <div className="mt-4 space-y-3">
              <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-700">
                <p className="font-semibold">Etapa 1</p>
                <p>Conciliacao de planilhas.</p>
              </div>
              <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-700">
                <p className="font-semibold">Etapa 2</p>
                <p>Busca de imagens {phase2Status === 'running' ? 'em andamento' : phase2Status === 'completed' ? 'concluida' : 'aguardando' }.</p>
              </div>
              <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-700">
                <p className="font-semibold">Etapa 3</p>
                <p>Tratamento final {phase3Status === 'running' ? 'em andamento' : phase3Status === 'completed' ? 'concluida' : 'aguardando'}.</p>
              </div>
            </div>
            <button
              className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-msn-green px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-zinc-300"
              disabled={status !== 'success' || phase2Status !== 'idle'}
              onClick={startPhase2}
              type="button"
            >
              Iniciar busca de imagens
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </button>
            <button
              className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-lg border border-zinc-200 bg-white px-4 py-3 text-sm font-semibold text-zinc-900 shadow-sm transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:border-zinc-200 disabled:text-zinc-400"
              disabled={phase2Status !== 'completed' || phase3Status !== 'idle'}
              onClick={startPhase3}
              type="button"
            >
              Iniciar tratamento final
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
