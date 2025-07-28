<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-6">Admin Dashboard</h2>

    <!-- ✅ Create New Parking Lot -->
    <section class="mb-8">
      <h3 class="text-xl font-semibold mb-2">Create New Parking Lot</h3>
      <div class="flex flex-col gap-2 max-w-md">
        <input v-model="newLotName" placeholder="Lot Name" class="border p-2 rounded" />
        <input v-model="newLotLocation" placeholder="Location" class="border p-2 rounded" />
        <input v-model.number="newLotPrice" type="number" placeholder="Price per Hour" class="border p-2 rounded" />
        <input v-model.number="newLotSpots" type="number" placeholder="Number of Spots" class="border p-2 rounded" />
        <button @click="createLot" class="bg-green-600 text-white px-4 py-2 rounded w-fit">+ Create Lot</button>
      </div>
    </section>

    <!-- ✅ List of Users -->
    <section class="mb-8">
      <h3 class="text-xl font-semibold mb-2">Users</h3>
      <ul>
        <li v-for="user in users" :key="user.id" class="mb-1">
          {{ user.email }} — <span class="text-gray-600">{{ user.role }}</span>
        </li>
      </ul>
    </section>

    <!-- ✅ Parking Lots + Add Spot -->
    <section>
      <h3 class="text-xl font-semibold mb-2">Parking Lots</h3>
      <ul>
        <li v-for="lot in parkingLots" :key="lot.id" class="mb-2">
          <strong>{{ lot.name }}</strong> ({{ lot.location }}) — ₹{{ lot.price }}/hr
          <button @click="selectLot(lot)" class="ml-2 px-2 py-1 bg-blue-500 text-white rounded">Add Spot</button>
        </li>
      </ul>
    </section>

    <!-- ✅ Add Spot UI -->
    <section v-if="selectedLot" class="mt-6">
      <h4 class="text-lg font-semibold mb-2">Add Spot to {{ selectedLot.name }}</h4>
      <button @click="addSpot" class="bg-purple-600 text-white px-3 py-1 rounded">+ Add Spot</button>
      <p v-if="addMessage" class="text-green-700 mt-2">{{ addMessage }}</p>
    </section>

    <!-- 🔓 Logout -->
    <div class="mt-8">
      <button @click="logout" class="bg-gray-800 text-white px-4 py-2 rounded">Logout</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const users = ref([])
const parkingLots = ref([])
const selectedLot = ref(null)
const addMessage = ref('')

// For create lot
const newLotName = ref('')
const newLotLocation = ref('')
const newLotPrice = ref(10)
const newLotSpots = ref(0)

onMounted(() => {
  fetchUsers()
  fetchLots()
})

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://127.0.0.1:5000/api/admin/users', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    users.value = await res.json()
  } catch (err) {
    console.error('Failed to fetch users', err)
  }
}

const fetchLots = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://127.0.0.1:5000/api/admin/parking-lots', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    parkingLots.value = await res.json()
    console.log("parkingLots", parkingLots)
  } catch (err) {
    console.error('Failed to fetch lots', err)
  }
}

const selectLot = (lot) => {
  selectedLot.value = lot
  addMessage.value = ''
}

const addSpot = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(`http://127.0.0.1:5000/api/admin/parking-spots`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        lot_id: selectedLot.value.id,
        count: 1
      })
    })
    const data = await res.json()
    if (res.ok) {
      addMessage.value = '✅ Spot added successfully!'
    } else {
      addMessage.value = data.message || '❌ Failed to add spot'
    }
  } catch (err) {
    addMessage.value = '❌ Something went wrong'
    console.error(err)
  }
}

const createLot = async () => {
  try {
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
  } catch (err) {
    console.error('Error creating lot:', err)
  }
}

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
