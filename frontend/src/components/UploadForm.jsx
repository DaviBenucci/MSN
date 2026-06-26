import { FileSpreadsheet, Loader2, Upload } from 'lucide-react'

const acceptedExtensions = '.xlsx,.csv'

function UploadForm({ canSubmit, files, isProcessing, onFileChange, onSubmit }) {
  return (
    <form className="space-y-5" onSubmit={onSubmit}>
      <div className="grid gap-4 md:grid-cols-2">
        <FileInput
          description="Exportacao usada como base de importacao."
          file={files.wordpress}
          id="wordpress-file"
          label="Planilha WordPress"
          name="wordpress"
          disabled={isProcessing}
          onFileChange={onFileChange}
        />
        <FileInput
          description="Estoque e precos enviados pelo cliente."
          file={files.cliente}
          id="cliente-file"
          label="Planilha do cliente"
          name="cliente"
          disabled={isProcessing}
          onFileChange={onFileChange}
        />
      </div>

      <div className="flex flex-col gap-3 border-t border-zinc-200 pt-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="text-sm text-zinc-600">
          Formatos aceitos: <span className="font-medium text-zinc-900">CSV</span> e{' '}
          <span className="font-medium text-zinc-900">XLSX</span>
        </div>
        <button
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-msn-green px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-zinc-300"
          disabled={!canSubmit || isProcessing}
          type="submit"
        >
          {isProcessing ? (
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          ) : (
            <Upload className="h-4 w-4" aria-hidden="true" />
          )}
          {isProcessing ? 'Processando...' : 'Processar conciliacao'}
        </button>
      </div>
    </form>
  )
}

function FileInput({ description, disabled, file, id, label, name, onFileChange }) {
  return (
    <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-4">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-white text-msn-blue ring-1 ring-zinc-200">
          <FileSpreadsheet className="h-5 w-5" aria-hidden="true" />
        </div>
        <div className="min-w-0 flex-1">
          <label className="block text-sm font-semibold text-zinc-950" htmlFor={id}>
            {label}
          </label>
          <p className="mt-1 text-sm leading-5 text-zinc-600">{description}</p>
          <input
            accept={acceptedExtensions}
            className="mt-4 block w-full cursor-pointer rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-700 file:mr-3 file:rounded-md file:border-0 file:bg-zinc-900 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:border-zinc-400 focus:border-msn-blue focus:outline-none focus:ring-2 focus:ring-blue-100"
            disabled={disabled}
            id={id}
            name={name}
            onChange={(event) => onFileChange(name, event.target.files?.[0] ?? null)}
            type="file"
          />
          <p className="mt-3 min-h-5 truncate text-sm font-medium text-zinc-800">
            {file ? file.name : 'Nenhum arquivo selecionado'}
          </p>
        </div>
      </div>
    </div>
  )
}

export default UploadForm
