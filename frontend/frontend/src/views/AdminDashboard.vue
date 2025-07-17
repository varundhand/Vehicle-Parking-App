<template>
  <div>
    <h2>Admin Dashboard</h2>

    <section>
      <h3>Users</h3>
      <ul>
        <li v-for="user in users" :key="user.id">
          {{ user.email }} - {{ user.role }}
        </li>
      </ul>
    </section>

    <section>
      <h3>Parking Lots</h3>
      <ul>
        <li v-for="lot in parkingLots" :key="lot.id">
          {{ lot.name }} ({{ lot.location }})
          <button @click="selectLot(lot)">Add Spot</button>
        </li>
      </ul>
    </section>

    <section v-if="selectedLot">
      <h4>Add Spot to {{ selectedLot.name }}</h4>
      <button @click="addSpot">+ Add Spot</button>
      <p v-if="addMessage">{{ addMessage }}</p>
    </section>

    <div class="logoutButtonWrapper">
         <button @click="logout">Logout</button>
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

// Fetch all users and parking lots when component loads
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
      addMessage.value = 'Spot added successfully!'
    } else {
      addMessage.value = data.message || 'Failed to add spot'
    }
  } catch (err) {
    addMessage.value = 'Something went wrong'
    console.error(err)
  }
}

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
