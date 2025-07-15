<template>
  <div>
    <h2>Welcome, {{ user?.email || 'User' }}!</h2>
    <button @click="logout">Logout</button>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
const auth = useAuthStore()
const router = useRouter()
const user = auth.user

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
