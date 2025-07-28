<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="left-pane">
        <img src="@/assets/parkmate.png" alt="Logo" class="logo-img" />
      </div>
      <div class="right-pane clay-card">
        <h2 class="mb-4 font-italic">Login</h2>
        <form @submit.prevent="login">
          <input v-model="email" type="email" class="form-input" placeholder="Email" required />
          <input v-model="password" type="password" class="form-input" placeholder="Password" required />
          <button class="form-button">Login</button>
          <div class="pt-2">Dont have an account? 
            <RouterLink to="/register" class="text-decoration-underline text-info ms-1">Register Now</RouterLink>
            </div>
          <p v-if="error" class="error-text mt-2">{{ error }}</p>
        </form>
      </div>
    </div>
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
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value }),
      credentials: 'include'
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message)
    auth.setToken(data.access_token)
    auth.setUser(data)
    router.push({ path: data.role === 'admin' ? '/admin' : '/user' })
  } catch (err) {
    error.value = err.message
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.login-container {
  display: flex;
  width: 800px;
  height: 400px;
  background: rgba(94, 94, 119, 0.85);
  border-radius: 2rem;
  box-shadow: 8px 8px 15px #1a1a28, -8px -8px 15px #3a3a4c;
  overflow: hidden;
}

.left-pane {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  padding: 1rem;
}

.right-pane {
  flex: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.logo-img {
  max-width: 80%;
  filter: drop-shadow(0px 0px 6px #fff);
}

.form-input {
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #1e1e2f;
  color: #fff;
  border: 1px solid #444;
  border-radius: 10px;
}

.form-button {
  width: 100%;
  background-color: #3b82f6;
  padding: 0.75rem;
  border-radius: 10px;
  color: white;
  border: none;
  cursor: pointer;
  margin-top: 1rem;
}

.error-text {
  color: #f87171;
  text-align: center;
}
</style>
