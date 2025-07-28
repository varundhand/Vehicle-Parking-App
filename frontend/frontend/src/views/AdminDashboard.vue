<template>
  <div class="container py-4">
    <h2 class="display-6 text-white mb-4 shadow-text">🛠️ Admin Dashboard</h2>

    <!-- Create Lot -->
    <div class="clay-card mb-5 p-4">
      <h4 class="mb-3">Create New Parking Lot</h4>
      <div class="row g-3">
        <div class="col-md-6">
          <input v-model="newLotName" class="form-control" placeholder="Lot Name" />
        </div>
        <div class="col-md-6">
          <input v-model="newLotLocation" class="form-control" placeholder="Location" />
        </div>
        <div class="col-md-6">
          <input v-model.number="newLotPrice" type="number" class="form-control" placeholder="Price per Hour" />
        </div>
        <div class="col-md-6">
          <input v-model.number="newLotSpots" type="number" class="form-control" placeholder="Number of Spots" />
        </div>
        <div class="col-12 text-end">
          <button class="btn btn-success mt-2" @click="createLot">+ Create Lot</button>
        </div>
      </div>
    </div>

    <!-- Users -->
    <div class="clay-card mb-5 p-4">
      <h4>👥 All Users</h4>
      <ul class="list-group mt-2">
        <li class="list-group-item bg-dark text-white" v-for="user in users" :key="user.id">
          {{ user.email }} <span class="badge bg-secondary ms-2">{{ user.role }}</span>
        </li>
      </ul>
    </div>

    <!-- Parking Lots -->
    <div class="clay-card mb-4 p-4">
      <h4>🏢 Parking Lots</h4>
      <ul class="list-group mt-2">
        <li class="list-group-item bg-dark text-white" v-for="lot in parkingLots" :key="lot.id">
          <strong>{{ lot.name }}</strong> — {{ lot.location }} (₹{{ lot.price }}/hr)
          <button class="btn btn-sm btn-primary float-end" @click="selectLot(lot)">+ Add Spot</button>
        </li>
      </ul>
    </div>

    <!-- Add Spot -->
    <div v-if="selectedLot" class="clay-card p-4">
      <h5>Add Spot to <span class="text-info">{{ selectedLot.name }}</span></h5>
      <button class="btn btn-purple mt-2" @click="addSpot">+ Add Spot</button>
      <p v-if="addMessage" class="mt-2 text-success">{{ addMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const users = ref([])
const parkingLots = ref([])
const selectedLot = ref(null)
const addMessage = ref('')

const newLotName = ref('')
const newLotLocation = ref('')
const newLotPrice = ref(10)
const newLotSpots = ref(0)

onMounted(() => {
  fetchUsers()
  fetchLots()
})

const fetchUsers = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/admin/users', {
    headers: { Authorization: `Bearer ${token}` }
  })
  users.value = await res.json()
}

const fetchLots = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/admin/parking-lots', {
    headers: { Authorization: `Bearer ${token}` }
  })
  parkingLots.value = await res.json()
}

const selectLot = (lot) => {
  selectedLot.value = lot
  addMessage.value = ''
}

const addSpot = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/admin/parking-spots', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ lot_id: selectedLot.value.id, count: 1 })
  })
  const data = await res.json()
  addMessage.value = res.ok ? '✅ Spot added successfully!' : `❌ ${data.message}`
}

const createLot = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/admin/parking-lots', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: newLotName.value,
      location: newLotLocation.value,
      price: newLotPrice.value,
      spots: newLotSpots.value
    })
  })

  const data = await res.json()
  if (res.ok) {
    alert('✅ Parking lot created')
    fetchLots()
    newLotName.value = ''
    newLotLocation.value = ''
    newLotPrice.value = 10
  } else {
    alert(`❌ ${data.message || 'Failed to create lot'}`)
  }
}
</script>

<style scoped>
.clay-card {
  background: #2b2b2b;
  border-radius: 16px;
  box-shadow: 8px 8px 20px #1c1c1c, -8px -8px 20px #3c3c3c;
  color: white;
}
.btn-purple {
  background-color: #7c3aed;
  color: white;
}
.shadow-text {
  text-shadow: 2px 2px 5px #000;
}
</style>
