<template>
  <nav class="navbar navbar-expand-lg vp-navbar-dark glass-shadow-dark px-4 py-3">
    <div class="container-fluid">
      <span class="navbar-brand fw-bold text-white">🚗 Parking App</span>

      <div class="collapse navbar-collapse justify-content-end">
        <ul class="navbar-nav gap-3">
          <!-- Admin Links -->
          <template v-if="role === 'admin'">
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/admin">Home</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/admin/users">Users</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/admin/search">Search</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/admin/summary">Summary</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/admin/profile">Edit Profile</RouterLink></li>
          </template>

          <!-- User Links -->
          <template v-else-if="role === 'user'">
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/user">Home</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/user/summary">Summary</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/user/profile">Edit Profile</RouterLink></li>
          </template>

          <!-- Logout -->
          <li class="nav-item">
            <button @click="logout" class="btn btn-danger btn-sm rounded-pill shadow-sm">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { computed } from 'vue'

const router = useRouter()
const auth = useAuthStore()
const role = computed(() => auth.user?.role || '')

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Claymorphism Glass Effect */
.vp-navbar-dark {
  background: rgba(30, 30, 30, 0.75);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  margin: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Shadow effect for claymorphism */
.glass-shadow-dark {
  box-shadow:
    4px 4px 12px rgba(0, 0, 0, 0.5),
    -4px -4px 8px rgba(255, 255, 255, 0.05);
}
</style>
