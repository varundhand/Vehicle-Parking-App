<template>
  <div class="users-view p-4">
    <div class="clay-card">
      <h2 class="text-light fs-4 fw-bold mb-4">👥 All Users</h2>
      <table class="table table-dark table-bordered table-hover">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'

const token = localStorage.getItem('token')
const users = ref([])

const fetchUsers = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/admin/users', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  users.value = await res.json()
}

onMounted(() => {
  fetchUsers()
})
</script>


<style scoped>
.clay-card {
  background: #2b2b3c;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 10px 10px 20px #1c1c2b, -10px -10px 20px #3a3a4a;
}
</style>
