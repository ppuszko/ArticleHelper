import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  withCredentials: true, // needed if you use cookie-based auth
})

// ── Auth endpoints (fastapi-users defaults) ────────────────────────────────

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export async function register({ email, password, name }) {
  const { data } = await api.post('/auth/register', { email, password, name })
  return data
}

export async function login({ email, password }) {
  // fastapi-users login expects form data, not JSON
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)

  const { data } = await api.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data  // { access_token, token_type }
}

export async function logout() {
  const { data } = await api.post('/auth/jwt/logout')
  return data
}

export async function forgotPassword({ email }) {
  const { data } = await api.post('/auth/forgot-password', { email })
  return data
}

export async function resetPassword({ token, password }) {
  const { data } = await api.post('/auth/reset-password', { token, password })
  return data
}

export default api
