<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    await store.register(username.value, password.value)
    success.value = 'Registration successful! Redirecting to login...'
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    error.value = err || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h1>Register</h1>
    <input v-model="username" placeholder="Username" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button :disabled="loading" @click="handleRegister">
      {{ loading ? 'Registering...' : 'Register' }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>

    <p>Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>