<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
const router = useRouter()

const goTo2FA = () => router.push('/2fa-setup')

const handleLogout = () => {
  store.logout()
  router.push('/login')
}
</script>

<template>
  <div>
    <h1>Dashboard</h1>
    <p>Welcome, you are logged in!</p>

    <button @click="goTo2FA">Enable 2FA</button>
    <button @click="handleLogout" style="margin-left: 10px; background: #e74c3c;">
      Logout
    </button>
  </div>
</template>