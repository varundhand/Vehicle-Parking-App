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

    <!-- 🟦 Recent Parking History -->
    <section class="mt-4">
    <h3 class="text-lg font-semibold mb-2">📜 Recent Parking History</h3>
    <table class="table-auto w-full border border-gray-300">
        <thead>
            <tr class="bg-gray-100">
                <th class="px-4 py-2">ID</th>
                <th class="px-4 py-2">Location</th>
                <th class="px-4 py-2">Vehicle #</th>
                <th class="px-4 py-2">Timestamp</th>
                <th class="px-4 py-2">Action</th>
            </tr>
        </thead>
        <div v-if="!isEmpty(reservationHistory)">
            <tbody v-if="!isEmpty(reservationHistory)">
                <tr v-for="entry in reservationHistory" :key="entry.id" class="text-center border-t">
                    <td class="px-4 py-2">{{ entry.id }}</td>
                    <td class="px-4 py-2">{{ entry.location }}</td>
                    <td class="px-4 py-2">{{ entry.vehicle_number || '-' }}</td>
                    <td class="px-4 py-2">{{ entry.timestamp }}</td>
                    <td class="px-4 py-2">
                    <span v-if="entry.is_active" class="bg-red-300 text-white px-2 py-1 rounded">Release</span>
                    <span v-else class="bg-green-300 text-black px-2 py-1 rounded">Parked Out</span>
                    </td>
                </tr>
            </tbody>
        </div>
        <div v-else>No Parking History</div>
    </table>
    </section>


    <!-- 🟦 Available Lots -->
    <section class="mt-6">
      <h3>🅿️ Available Parking Lots</h3>
      <ul v-if="parkingLots.length > 0">
        <li v-for="lot in parkingLots" :key="lot.id" class="my-2">
          <strong>{{ lot.name }}</strong> - {{ lot.location }} (₹{{ lot.price || 'N/A' }})
          <button
            @click="reserveSpot(lot.id)"
            :disabled="reservation"
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
const token = localStorage.getItem('token')
// console.log("token->",token)

const parkingLots = ref([])
const reservation = ref(null)
const reservationHistory = ref([])

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
