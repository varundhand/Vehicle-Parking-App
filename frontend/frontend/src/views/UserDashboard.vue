<template>
  <div class="user-dashboard-wrapper p-4">
    <h2 class="text-light fs-4 fw-bold mb-4">👋 Welcome, {{ user.name }}!</h2>

    <!-- Active Reservation -->
    <div v-if="reservation" class="clay-card mb-4">
      <h4 class="mb-2">🅿️ Your Active Reservation</h4>
      <p>Lot: {{ reservation.lot_name }}<br />Spot ID: {{ reservation.spot_id }}<br />Status: {{ reservation.status }}</p>
      <button @click="cancelReservation" class="btn btn-danger mt-2">Cancel Reservation</button>
    </div>

    <!-- Data Export Section -->
    <div class="clay-card mb-4">
      <h4 class="mb-3">📊 Export Your Data</h4>
      <div class="export-section">
        <div class="export-item d-flex justify-content-between align-items-center mb-3">
          <div class="export-info">
            <h5 class="mb-1">📄 CSV Export</h5>
            <p class="mb-0 text-muted">Download your complete parking history as CSV via email</p>
          </div>
          <button 
            @click="exportCSV" 
            :disabled="exportLoading"
            class="btn btn-outline-info"
          >
            <span v-if="exportLoading">
              🔄 Sending...
            </span>
            <span v-else>
              📧 Email CSV
            </span>
          </button>
        </div>
        
        <!-- Export Status -->
        <div v-if="exportStatus" class="alert" :class="exportStatusClass">
          {{ exportStatus.message }}
        </div>
      </div>
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
import { onMounted, ref, computed } from 'vue'

const auth = useAuthStore()
const router = useRouter()
const user = JSON.parse(localStorage.getItem('user') || '{}' )
const token = localStorage.getItem('token')

const parkingLots = ref([])
const reservation = ref(null)
const reservationHistory = ref([])

const searchQuery = ref('')
const searchResults = ref([])
const searchPerformed = ref(false)

// CSV Export data
const exportLoading = ref(false)
const exportStatus = ref(null)
const taskId = ref(null)

// Computed property for export status styling
const exportStatusClass = computed(() => {
  if (!exportStatus.value) return ''
  return {
    'alert-success': exportStatus.value.type === 'success',
    'alert-danger': exportStatus.value.type === 'error',
    'alert-info': exportStatus.value.type === 'info'
  }
})

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

// CSV Export functionality
const exportCSV = async () => {
  exportLoading.value = true
  exportStatus.value = null
  
  try {
    const response = await fetch('http://127.0.0.1:5000/api/user/export-csv', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    
    if (response.ok) {
      taskId.value = data.task_id
      exportStatus.value = {
        type: 'success',
        message: `✅ CSV export initiated! Check your email in a few minutes.`
      }
      
      // Check status after 5 seconds
      setTimeout(() => checkExportStatus(), 5000)
    } else {
      exportStatus.value = {
        type: 'error',
        message: `❌ Export failed: ${data.error || 'Unknown error'}`
      }
    }
  } catch (error) {
    exportStatus.value = {
      type: 'error',
      message: `❌ Network error: ${error.message}`
    }
  } finally {
    exportLoading.value = false
  }
}

const checkExportStatus = async () => {
  if (!taskId.value) return
  
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/user/email-status/${taskId.value}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    const data = await response.json()
    
    if (data.state === 'SUCCESS') {
      exportStatus.value = {
        type: 'success',
        message: '✅ CSV export completed! Check your email inbox.'
      }
    } else if (data.state === 'FAILURE') {
      exportStatus.value = {
        type: 'error',
        message: `❌ Export failed: ${data.error}`
      }
    } else {
      exportStatus.value = {
        type: 'info',
        message: '⏳ Export in progress...'
      }
      // Check again in 3 seconds
      setTimeout(() => checkExportStatus(), 3000)
    }
  } catch (error) {
    console.error('Error checking export status:', error)
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

    if (res.ok){
        const data = await res.json()
        reservation.value = data.reservation
    }else{
        reservation.value=null
    }
    } catch(error){
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

onMounted(() => {
  if (!auth.token) {
    auth.token = localStorage.getItem('token')
  }
  fetchParkingLots()
  fetchReservation()
  fetchReservationHistory()
})

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

.export-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 1rem;
}

.export-info h5 {
  color: #fff;
}

.export-info p {
  font-size: 0.9rem;
}
</style>