<template>
  <div class="p-4 max-w-xl mx-auto">
    <h2 class="text-xl font-bold mb-4">🔎 Search</h2>

    <div class="mb-4">
      <label class="block font-semibold mb-1">Search Type:</label>
      <select v-model="searchType" class="border p-2 rounded w-full">
        <option value="email" v-if="role === 'admin'">User by Email</option>
        <option value="location" v-if="role === 'user'">Parking by Location</option>
        <option value="lot_name" v-if="role === 'user'">Parking by Lot Name</option>
      </select>
    </div>

    <div class="mb-4">
      <input v-model="query" placeholder="Enter search text..." class="border p-2 rounded w-full" />
    </div>

    <button @click="search" class="bg-blue-500 text-white px-4 py-2 rounded">Search</button>

    <!-- Admin Result -->
    <div v-if="role === 'admin' && result" class="mt-6">
      <h3 class="font-bold mb-2">User Found:</h3>
      <p><strong>Email:</strong> {{ result.email }}</p>
      <p><strong>Role:</strong> {{ result.role }}</p>
      <p><strong>Name:</strong> {{ result.name }}</p>
      <p><strong>Address:</strong> {{ result.address }}</p>
      <p><strong>Pincode:</strong> {{ result.pincode }}</p>
    </div>

    <!-- User Result -->
    <div v-if="role === 'user' && parkingResults.length" class="mt-6">
      <h3 class="font-bold mb-2">Matching Lots:</h3>
      <ul>
        <li v-for="lot in parkingResults" :key="lot.id" class="border p-2 mb-2 rounded">
          <strong>{{ lot.name }}</strong> - {{ lot.location }}<br />
          Available: {{ lot.available_spots }} / {{ lot.total_spots }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const token = localStorage.getItem('token')
const user = JSON.parse(localStorage.getItem('user') || '{}')
const role = user.role || 'user'

const searchType = ref(role === 'admin' ? 'email' : 'location')
const query = ref('')
const result = ref(null)
const parkingResults = ref([])

const search = async () => {
  if (!query.value.trim()) return alert('Please enter a search value.')

  if (role === 'admin' && searchType.value === 'email') {
    const res = await fetch(`http://127.0.0.1:5000/api/admin/search-user?email=${query.value}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (res.ok) {
      result.value = await res.json()
    } else {
      result.value = null
      alert('❌ User not found')
    }
  }

  if (role === 'user') {
  let endpoint = ''
  if (searchType.value === 'location') {
        endpoint = `http://127.0.0.1:5000/api/user/search-lots?location=${query.value}`
    } else if (searchType.value === 'lot_name') {
        endpoint = `http://127.0.0.1:5000/api/user/search-lots?name=${query.value}`
    }

    const res = await fetch(endpoint, {
        headers: {
        Authorization: `Bearer ${token}`
        }
    })

    if (res.ok) {
        parkingResults.value = await res.json()
    } else {
        parkingResults.value = []
        alert('❌ No lots found')
    }
    }

}
</script>
