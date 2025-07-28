<template>
  <div class="user-dashboard-wrapper p-4">
    <h2 class="text-light fs-4 fw-bold mb-4">👋 Welcome, {{ user.name }}!</h2>

    <!-- Active Reservation -->
    <div v-if="reservation" class="clay-card mb-4">
      <h4 class="mb-2">🅿️ Your Active Reservation</h4>
      <p>Lot: {{ reservation.lot_name }}<br />Spot ID: {{ reservation.spot_id }}<br />Status: {{ reservation.status }}</p>
      <button @click="cancelReservation" class="btn btn-danger mt-2">Cancel Reservation</button>
    </div>

    <!-- Parking History -->
    <div class="clay-card mb-4">
      <h4 class="mb-3">📜 Parking History</h4>
      <div v-if="reservationHistory.length">
        <table class="table table-dark table-bordered table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Location</th>
              <th>Vehicle #</th>
              <th>Timestamp</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in reservationHistory" :key="entry.id">
              <td>{{ entry.id }}</td>
              <td>{{ entry.location }}</td>
              <td>{{ entry.vehicle_number || '-' }}</td>
              <td>{{ entry.timestamp }}</td>
              <td>
                <span class="badge" :class="entry.is_active ? 'bg-danger' : 'bg-success'">
                  {{ entry.is_active ? 'Release' : 'Parked Out' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>No Parking History</p>
    </div>

    <!-- Search + Results -->
<div class="clay-card mb-4">
  <h4 class="mb-3">🔍 Search Parking @location/pin code</h4>
  <form @submit.prevent="searchLots" class="mb-3 d-flex align-items-center gap-2">
    <input v-model="searchQuery" type="text" class="form-control form-control-dark" placeholder="Enter location or pin" />
    <button class="btn btn-outline-info">Search</button>
  </form>

  <div v-if="searchResults.length">
    <h5 class="mb-3">Parking Lots @ "{{ searchQuery }}"</h5>
    <ul class="list-group">
      <li
        v-for="lot in searchResults"
        :key="lot.id"
        class="list-group-item bg-dark text-light d-flex justify-content-between align-items-center"
      >
        <span><strong>{{ lot.name }}</strong> - {{ lot.location }} | Available: {{ lot.available_spots }}</span>
        <button @click="reserveSpot(lot.id)" :disabled="reservation" class="btn btn-outline-primary btn-sm">Book</button>
      </li>
    </ul>
  </div>
  <p v-else-if="searchPerformed">No results found for "{{ searchQuery }}"</p>
</div>


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
const token = localStorage.getItem('token')
// console.log("token->",token)

const parkingLots = ref([])
const reservation = ref(null)
const reservationHistory = ref([])

const searchQuery = ref('')
const searchResults = ref([])
const searchPerformed = ref(false)

const searchLots = async () => {
  if (!searchQuery.value.trim()) return

  try {
    const queryParam = encodeURIComponent(searchQuery.value)
    const res = await fetch(
      `http://127.0.0.1:5000/api/user/search-lots?location=${queryParam}&name=${queryParam}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (res.ok) {
      const data = await res.json()
      searchResults.value = data
      searchPerformed.value = true
    } else {
      searchResults.value = []
      searchPerformed.value = true
    }
  } catch (error) {
    console.error("Search failed", error)
    searchResults.value = []
    searchPerformed.value = true
  }
}



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
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

//     const data = await res.json()
//     console.log("data 1", data)

//     if (res.ok) {
//       if (!data.reservation) {
//         reservation.value = data // Update the value here, not the ref itself
//         console.log("data 2", reservation.value.reservation)
//       } else {
//         reservation.value = null // Set the value to null if there's no reservation
//       }
//     }
//   } catch (error) {
//     console.error("Failed to fetch reservation", error)
//     reservation.value = null // Set the value to null in case of an error
//   }
    if (res.ok){
        const data = await res.json()
        // console.log("data",data)
        reservation.value = data.reservation
        // reservation.
        // console.log("reservation ref",reservation)
    }else{
        reservation.value=null
    }
    }catch(error){
        console.error("Failed to fetch reservation", error)
        reservation.value = null
    }
}
const fetchReservationHistory = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/user/reservations/history', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (res.ok) {
      reservationHistory.value = await res.json()
    //   console.log("reservationHistory",reservationHistory.value)
    } else {
      reservationHistory.value = []
    }
  } catch (error) {
    console.error("Failed to fetch reservation history", error)
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
      await fetchReservationHistory()
    //   await
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
      await fetchReservationHistory()
    } else {
      alert(`❌ ${data.message}`)
    }
  } catch (error) {
    console.error("Error cancelling reservation", error)
  }
}

// console.log("auth-> ", auth,"user:", user)

onMounted(() => {
  if (!auth.token) {
    auth.token = localStorage.getItem('token')
  }
  fetchParkingLots()
  fetchReservation()
  fetchReservationHistory()
})

// functions
const isEmpty = (obj) => {
    return Object.keys(obj).length === 0;
}

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>


<style scoped>
.user-dashboard-wrapper {
  color: #e0e0e0;
}

.clay-card {
  background: #2c2c3c;
  border-radius: 20px;
  box-shadow: 8px 8px 15px #1a1a28, -8px -8px 15px #3a3a4c;
  padding: 1.5rem;
}
</style>
