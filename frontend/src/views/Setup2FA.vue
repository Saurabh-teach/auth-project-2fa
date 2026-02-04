<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'   // or '../stores/auth' if alias issue

const store = useAuthStore()
const router = useRouter()

const qrCode = ref('')
const secret = ref('')
const code = ref('')
const error = ref('')
const loading = ref(false)
const step = ref(1) // 1: show QR, 2: enter code

onMounted(async () => {
  loading.value = true
  try {
    const data = await store.enable2FA()
    qrCode.value = data.qr_code
    secret.value = data.secret
  } catch (err) {
    error.value = err || 'Failed to load 2FA setup'
  } finally {
    loading.value = false
  }
})

const confirm = async () => {
  if (!code.value || code.value.length !== 6) {
    error.value = 'Please enter a valid 6-digit code'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await store.confirm2FA(code.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = err || 'Invalid code or server error'
    console.error('Confirm 2FA error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h1>Enable 2FA</h1>

    <div v-if="step === 1">
      <p>Scan this QR code with your authenticator app (Google Authenticator, Authy, etc.)</p>
      <img v-if="qrCode" :src="qrCode" alt="2FA QR Code" style="max-width: 200px;" />
      <p v-if="secret">Or enter manually: <strong>{{ secret }}</strong></p>
      <button @click="step = 2">I scanned it → Next</button>
    </div>

    <div v-else>
      <p>Enter the 6-digit code from your app to confirm</p>
      <input v-model="code" placeholder="6-digit code" maxlength="6" />
      <button :disabled="loading" @click="confirm">
        {{ loading ? 'Confirming...' : 'Confirm' }}
      </button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<style scoped>
.error {
  color: red;
  text-align: center;
}
</style>