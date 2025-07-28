<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">👥 All Users</h2>
    <table class="w-full border border-gray-300">
      <thead class="bg-gray-100">
        <tr>
          <th class="px-4 py-2">ID</th>
          <th class="px-4 py-2">Email</th>
          <th class="px-4 py-2">Role</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id" class="border-t text-center">
          <td class="px-4 py-2">{{ user.id }}</td>
          <td class="px-4 py-2">{{ user.email }}</td>
          <td class="px-4 py-2">{{ user.role }}</td>
        </tr>
      </tbody>
    </table>
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
