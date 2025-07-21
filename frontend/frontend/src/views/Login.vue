<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />
      <button>Login</button>
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
const error = ref('')
const auth = useAuthStore()
const router = useRouter()

const login = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/auth/login', {
        // mode: 'no-cors',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value }),
      credentials: 'include'
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message)
// console.log('data.accesstoken', data.access_token)
    auth.setToken(data.access_token)
    // console.log("this is the data from login function -> ",data);
    
    auth.setUser(data)

    // router.push(data.role === 'admin' ? '/admin' : '/user')
    router.push({path: data.role === 'admin' ? 'admin' : 'user'})
  } catch (err) {
    error.value = err.message
  }
}
</script>
