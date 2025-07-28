<template>
  <div class="search-container container py-5">
    <div class="clay-card shadow-lg p-4 mx-auto">
      <h2 class="text-white mb-4">🔎 Smart Search</h2>

      <!-- 🔘 Search Type -->
      <div class="mb-3">
        <label class="form-label text-light">Search Type</label>
        <select v-model="searchType" class="form-select custom-select-dark">
          <option value="email" v-if="role === 'admin'">User by Email</option>
          <option value="location" v-if="role === 'user'">Parking by Location</option>
          <option value="lot_name" v-if="role === 'user'">Parking by Lot Name</option>
        </select>
      </div>

      <!-- 🔍 Search Input -->
      <div class="mb-3">
        <input v-model="query" type="text" placeholder="Enter search text..." class="form-control custom-input-dark" />
      </div>

      <!-- 🔎 Button -->
      <button @click="search" class="btn btn-primary w-100">Search</button>

      <!-- 📄 Admin Results -->
      <div v-if="role === 'admin' && result" class="mt-5 text-light">
        <h4 class="mb-3">👤 User Found</h4>
        <ul class="list-group list-group-flush">
          <li class="list-group-item bg-transparent border-secondary text-light"><strong>Email:</strong> {{ result.email }}</li>
          <li class="list-group-item bg-transparent border-secondary text-light"><strong>Role:</strong> {{ result.role }}</li>
          <li class="list-group-item bg-transparent border-secondary text-light"><strong>Name:</strong> {{ result.name }}</li>
          <li class="list-group-item bg-transparent border-secondary text-light"><strong>Address:</strong> {{ result.address }}</li>
          <li class="list-group-item bg-transparent border-secondary text-light"><strong>Pincode:</strong> {{ result.pincode }}</li>
        </ul>
      </div>

      <!-- 📦 User Results -->
      <div v-if="role === 'user' && parkingResults.length" class="mt-5 text-light">
        <h4 class="mb-3">🚗 Matching Parking Lots</h4>
        <div class="row g-3">
          <div v-for="lot in parkingResults" :key="lot.id" class="col-md-6">
            <div class="card custom-lot-card text-light">
              <div class="card-body">
                <h5 class="card-title">{{ lot.name }}</h5>
                <p class="card-text mb-1"><strong>Location:</strong> {{ lot.location }}</p>
                <p class="card-text"><strong>Available:</strong> {{ lot.available_spots }} / {{ lot.total_spots }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

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
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) result.value = await res.json()
    else {
      result.value = null
      alert('❌ User not found')
    }
  }

  if (role === 'user') {
    let endpoint = searchType.value === 'location'
      ? `http://127.0.0.1:5000/api/user/search-lots?location=${query.value}`
      : `http://127.0.0.1:5000/api/user/search-lots?name=${query.value}`

    const res = await fetch(endpoint, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) parkingResults.value = await res.json()
    else {
      parkingResults.value = []
      alert('❌ No lots found')
    }
  }
}
</script>

<style scoped>
.search-container {
  /* min-height: 100vh;
  background-color: #1a1a2e; */
}

.clay-card {
  background: #2b2b3c;
  border-radius: 20px;
  box-shadow: 10px 10px 25px #141421, -10px -10px 25px #38384b;
}

.custom-input-dark,
.custom-select-dark {
  background-color: #1f1f2f;
  border: 1px solid #444;
  color: #e0e0e0;
}

.custom-input-dark::placeholder,
.custom-select-dark option {
  color: #888;
}

.custom-lot-card {
  background-color: #232334;
  border-radius: 15px;
  border: 1px solid #444;
  box-shadow: inset 4px 4px 10px #1a1a28, inset -4px -4px 10px #2f2f44;
}
</style>
