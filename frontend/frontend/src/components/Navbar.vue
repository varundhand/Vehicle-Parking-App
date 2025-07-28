<template>
  <nav class="bg-gray-800 text-white px-6 py-3 flex justify-between items-center">
    <div class="text-xl font-bold">🚗 Parking App</div>
    
    <ul class="flex space-x-4 items-center">

      <!-- Admin Links -->
      <template v-if="role === 'admin'">
        <li><RouterLink to="/admin" class="hover:underline">Home</RouterLink></li>
        <li><RouterLink to="/admin/users" class="hover:underline">Users</RouterLink></li>
        <li><RouterLink to="/admin/search" class="hover:underline">Search</RouterLink></li>
        <li><RouterLink to="/admin/summary" class="hover:underline">Summary</RouterLink></li>
        <li><RouterLink to="/admin/profile" class="hover:underline">Edit Profile</RouterLink></li>
      </template>

      <!-- User Links -->
      <template v-if="role === 'user'">
        <li><RouterLink to="/user" class="hover:underline">Home</RouterLink></li>
        <li><RouterLink to="/user/summary" class="hover:underline">Summary</RouterLink></li>
        <li><RouterLink to="/user/profile" class="hover:underline">Edit Profile</RouterLink></li>
      </template>

      <!-- Logout -->
      <li><button @click="logout" class="bg-red-600 px-3 py-1 rounded">Logout</button></li>
    </ul>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { computed } from 'vue'


const router = useRouter()
const auth = useAuthStore()

// const user = JSON.parse(localStorage.getItem('user') || '{}')
const role = computed(() => auth.user?.role || '')

// console.log('user:', user, 'role:', role)

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
