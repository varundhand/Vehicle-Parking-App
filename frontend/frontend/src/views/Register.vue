<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />
      <input v-model="name" placeholder="Full Name">
      <input v-model="address" placeholder="Address">
      <input v-model="pin_code" placeholder="Pin Code">
      <button>Register</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'


const email = ref('')
const password = ref('')
const name = ref('')
const address = ref('')
const pin_code = ref('')
const error = ref('')
const auth = useAuthStore()
const router = useRouter()

const register = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value, full_name: name.value, address: address.value, pin_code: pin_code.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message)
    auth.setToken(data.access_token)
    auth.setUser(data)

    router.push({path: data.role === 'admin' ? 'admin' : 'user'})
  } catch (err) {
    error.value = err.message
  }
}
</script>
