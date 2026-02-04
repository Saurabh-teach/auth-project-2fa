<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const code = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const result = await store.login(username.value, password.value)
    if (result.requires2FA) {
      // Stay on page, show 2FA input
    } else {
      router.push('/dashboard')
    }
  } catch (err) {
    error.value = err || 'Login failed'
  } finally {
    loading.value = false
  }
}

const handleVerify2FA = async () => {
  loading.value = true
  error.value = ''

  try {
    await store.verify2FA(code.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = err || 'Invalid code'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h1>Login</h1>

    <div v-if="!store.requires2FA">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button :disabled="loading" @click="handleLogin">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
    </div>

    <div v-else>
      <h2>Enter 2FA Code</h2>
      <input v-model="code" placeholder="6-digit code" maxlength="6" />
      <button :disabled="loading" @click="handleVerify2FA">
        {{ loading ? 'Verifying...' : 'Verify' }}
      </button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <p>Don't have an account? <router-link to="/register">Register</router-link></p>
  </div>
</template>