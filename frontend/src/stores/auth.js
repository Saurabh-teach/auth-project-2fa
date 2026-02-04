import { defineStore } from 'pinia'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

// Global error logging (very useful for debugging)
axios.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    requires2FA: false,
    tempUserId: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async register(username, password) {
      try {
        await axios.post('/auth/register', { username, password })
        return { success: true }
      } catch (err) {
        throw err.response?.data?.detail || 'Registration failed'
      }
    },

    async login(username, password) {
      try {
        const res = await axios.post(
          '/auth/token',
          new URLSearchParams({ username, password }),
          { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
        )

        if (res.data.requires_2fa) {
          this.requires2FA = true
          this.tempUserId = res.data.temp_user_id
          return { requires2FA: true }
        }

        this.token = res.data.access_token
        localStorage.setItem('token', this.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        return { success: true }
      } catch (err) {
        throw err.response?.data?.detail || 'Login failed'
      }
    },

    async verify2FA(code) {
      try {
        const res = await axios.post('/auth/token/2fa', {
          user_id: this.tempUserId,
          code
        })

        this.token = res.data.access_token
        localStorage.setItem('token', this.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        this.requires2FA = false
        this.tempUserId = null

        return { success: true }
      } catch (err) {
        throw err.response?.data?.detail || 'Invalid 2FA code'
      }
    },

    // ────────────────────────────────────────────────
    // FIXED & IMPROVED enable2FA – with debug log
    // ────────────────────────────────────────────────
    async enable2FA() {
      if (!this.token) {
        throw new Error('You must be logged in to enable 2FA')
      }

      try {
        const res = await axios.post('/auth/2fa/enable', {}, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })

        // Store temp_user_id from backend response
        if (res.data.temp_user_id) {
          this.tempUserId = res.data.temp_user_id
          console.log('Stored tempUserId from enable2FA:', this.tempUserId) // ← debug
        } else {
          console.warn('Warning: Backend did NOT return temp_user_id in enable2FA response')
        }

        return res.data // { secret, qr_code, uri, temp_user_id? }
      } catch (err) {
        console.error('enable2FA failed:', err)
        throw err.response?.data?.detail || 'Failed to enable 2FA'
      }
    },

    // ────────────────────────────────────────────────
    // FIXED confirm2FA – sends user_id + code + token
    // ────────────────────────────────────────────────
    async confirm2FA(code) {
      if (!this.token) {
        throw new Error('You must be logged in')
      }
      if (!this.tempUserId) {
        throw new Error('User ID not set – enable 2FA first')
      }

      try {
        await axios.post('/auth/2fa/confirm', {
          user_id: this.tempUserId,
          code
        }, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })

        console.log('2FA confirm successful – user_id sent:', this.tempUserId) // ← debug

        return { success: true }
      } catch (err) {
        console.error('confirm2FA failed:', err)
        throw err.response?.data?.detail || 'Invalid confirmation code'
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.requires2FA = false
      this.tempUserId = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})