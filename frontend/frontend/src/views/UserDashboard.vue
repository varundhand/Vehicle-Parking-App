<template>
  <div class="p-4">
    <h2>Welcome, {{ user.name}}!</h2>

    <!-- 🟦 Current Reservation (if any) -->
    <section v-if="reservation">
      <h3>🅿️ Your Active Reservation</h3>
      <p>
        Lot: {{ reservation.lot_name }}<br />
        Spot ID: {{ reservation.spot_id }}<br />
        Status: {{ reservation.status }}
      </p>
      <button @click="cancelReservation" class="bg-red-500 text-white px-3 py-1 rounded">Cancel Reservation</button>
    </section>

    <!-- 🟦 Available Lots -->
    <section class="mt-6">
      <h3>🅿️ Available Parking Lots</h3>
      <ul v-if="parkingLots.length > 0">
        <li v-for="lot in parkingLots" :key="lot.id" class="my-2">
          <strong>{{ lot.name }}</strong> - {{ lot.location }} (₹{{ lot.price || 'N/A' }})
          <button
            @click="reserveSpot(lot.id)"
            :disabled="reservation !== null"
            class="ml-4 bg-blue-500 text-white px-3 py-1 rounded"
          >
            Book
          </button>
        </li>
      </ul>
      <p v-else>No parking lots available.</p>
    </section>

    <!-- 🔓 Logout -->
    <button @click="logout" class="mt-8 bg-gray-800 text-white px-4 py-2 rounded">Logout</button>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'

const auth = useAuthStore()
const router = useRouter()
// const user = localStorage.getItem('')
const user = JSON.parse(localStorage.getItem('user') || '{}' )
console.log(user.name)
const token = localStorage.getItem('token')

const parkingLots = ref([])
const reservation = ref(null)

const fetchParkingLots = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/user/parking-lots', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    parkingLots.value = await res.json()
  } catch (err) {
    console.error('Failed to fetch parking lots', err)
  }
}

const fetchReservation = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/user/reservation', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (res.ok) {
      reservation.value = await res.json()
    } else {
      reservation.value = null
    }
  } catch (error) {
    console.error("Failed to fetch reservation", error)
    reservation.value = null
  }
}

const reserveSpot = async (lotId) => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/user/reserve', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ lot_id: lotId })
    })

    const data = await res.json()
    if (res.ok) {
      alert('✅ Reservation successful')
      await fetchReservation()
    } else {
      alert(`❌ ${data.message}`)
    }
  } catch (error) {
    console.error("Error reserving spot", error)
  }
}

const cancelReservation = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/user/reservation', {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const data = await res.json()
    if (res.ok) {
      alert('✅ Reservation cancelled')
      reservation.value = null
      await fetchParkingLots()
    } else {
      alert(`❌ ${data.message}`)
    }
  } catch (error) {
    console.error("Error cancelling reservation", error)
  }
}

console.log("auth-> ", auth,"user:", user)

onMounted(() => {
  if (!auth.token) {
    auth.token = localStorage.getItem('token')
  }
  fetchParkingLots()
  fetchReservation()
})

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
