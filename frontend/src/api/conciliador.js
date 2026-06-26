const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8000'

export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL
).replace(/\/$/, '')

export async function conciliarPlanilhas({ cliente, wordpress }) {
  const formData = new FormData()
  formData.append('cliente', cliente)
  formData.append('wordpress', wordpress)

  const response = await fetch(`${API_BASE_URL}/api/v1/conciliar`, {
    method: 'POST',
    body: formData,
  })
  const payload = await readJsonResponse(response)

  if (!response.ok) {
    throw new Error(formatApiError(payload))
  }

  return payload
}

export function toDownloadUrl(path) {
  if (!path) {
    return '#'
  }
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  return `${API_BASE_URL}${path}`
}

async function readJsonResponse(response) {
  try {
    return await response.json()
  } catch {
    return null
  }
}

function formatApiError(payload) {
  if (!payload) {
    return 'Nao foi possivel ler a resposta da API.'
  }
  if (typeof payload.detail === 'string') {
    return payload.detail
  }
  if (payload.detail?.message) {
    const stderr = payload.detail.stderr ? ` ${payload.detail.stderr}` : ''
    return `${payload.detail.message}${stderr}`.trim()
  }
  return payload.message || 'A API retornou um erro inesperado.'
}
